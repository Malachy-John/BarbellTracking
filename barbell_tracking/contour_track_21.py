import cv2
import numpy as np
import time
from starting_pos import find_initial_coordinates
from collections import deque

class VideoProcessor:
    def __init__(self, video_path,right):
        self.video_path = video_path # video path of video file
        self.cap = cv2.VideoCapture(video_path) # opencv capture object with passed video file
        self.start_x, self.start_y, self.start_w, self.start_h = find_initial_coordinates(video_path) # starting x, y, width & height co-ordinates of barbell
        self.lower_blue = np.array([90, 120, 120]) # np array for lower range of light-blue colour
        self.upper_blue = np.array([100, 255, 255]) # np array for upper range of light-blue colour
        self.prev_y = None # previous y position
        self.prev_x = None # previous x position
        self.y_positions = deque(maxlen=2000) # all y positions during repetition
        self.x_positions = [] # all x positions during repetition
        self.frame_count = 0 # number of frames during concentric phase
        self.rep_count = 0
        self.set_started = False
        self.concentric_started = False
        self.eccentric_started = False
        self.barbell_radius_mm = 50 
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frame_delay_ns = int(1_000_000_000 / self.fps) # frame delay required to play back in real time
        self.frame_width = 1280
        self.rep_start_time_ns = None
        self.bottom_x = None
        self.bottom_y = None
        self.top_finish_x = None
        self.top_finish_y = None
        self.rep_ending_y_pos = None
        self.metres_per_second = 0 # m/s variable for one rep
        self.metres_per_second_list = [] # m/s variable for all reps
        self.rep_starting_pos = None
        self.set_ended = False
        self.distance_check = 0
        self.right = right
        self.rep_duration_s = None
        

    def is_inside_bounding_box(self, x, y):
        '''
        Function checks to verify if the barbell is within the bounds of the starting position, 
        "Is set ended or started"
        '''
        return self.start_x <= x < self.start_x + self.start_w and self.start_y <= y < self.start_y + self.start_h

    def process_frame(self, frame):
        '''
        This is the primary function of the VideoProcessor class
        This function allows for the processing of the frame to derive distance, speed & repetitions from the video
        '''
        # Start the timer for performance measurement
        start_time_frame_ns = time.perf_counter_ns()

        # Convert frame to HSV color space to facilitate color masking
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Create a mask for blue colors defined by lower and upper thresholds
        mask = cv2.inRange(hsv, self.lower_blue, self.upper_blue)

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Calculate centroid of the initial bounding box for referenc
        centroid = (int(self.start_x + self.start_w / 2), int(self.start_y + self.start_h / 2))

        # Draw a circle at the centroid in yellow
        cv2.circle(frame, centroid, 5, (255, 255, 0), -1)

        # Process each contour detected in the mask
        for contour in contours:
            area = cv2.contourArea(contour)

            # Consider only contours with a significant area
            if area > 500:
                x, y, w, h = cv2.boundingRect(contour)

                # Skip non-square contours if specified by self.right flag
                if not self.right:
                    if abs(w - h) > 15:
                        continue

                # Calculate center of the bounding box
                center = (int(x + w / 2), int(y + h / 2))

                # Draw a rectangle and a circle at the center of the contour
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 255), 2)
                cv2.circle(frame, center, 5, (255, 255, 255), -1)

                # get radius of circle and draw on screen
                ref_radius = min(self.start_w, self.start_h) // 2
                concentric_end_position_1 = (center[0] + ref_radius, center[1])
                cv2.line(frame, center, concentric_end_position_1, (0, 0, 255), 2)

                # Additional check if center is within the initial bounding box
                if self.is_inside_bounding_box(center[0], center[1]):
                    cv2.rectangle(frame, (self.start_x, self.start_y), (self.start_x+self.start_w, self.start_y+self.start_h), (255, 0, 255), 2)

                # add x and y positions to list
                self.x_positions.append(center[0])
                self.y_positions.append(center[1])

                # if prev_x and prev_y not set, set them to very first x and y position
                if self.prev_x is None:
                    self.prev_x = self.x_positions[0]
                if self.prev_y is None:
                    self.prev_y = self.y_positions[0]

                # use second last value to become the prev x and prev y values
                if len(self.x_positions) > 1:
                    self.prev_x = self.x_positions[-2]
                if len(self.y_positions) > 1:
                    self.prev_y = self.y_positions[-2]

                # find the millimetre to per pixel value
                mmpp = self.barbell_radius_mm / ref_radius

                # find the level of displacement between frames for x and y values.
                y_disp = self.prev_y - center[1]
                x_disp = self.prev_x - center[0]
                y_distance_per_frame = y_disp * mmpp

                # find the end position of the eccentric phase to draw the line
                eccentric_end_position_0 = (0, self.rep_starting_pos)
                eccentric_end_position_1 = (self.frame_width - 1, self.rep_starting_pos)
                if self.rep_starting_pos is not None:
                    cv2.line(frame, eccentric_end_position_0, eccentric_end_position_1, (255, 255, 255), 2)

                # if the set isn't started, wait for significant movement
                if not self.set_started:
                    #if right handed camera check for movement from right to left, else left to right for left handed camera
                    if self.right:
                        if y_disp < -2 and x_disp > 2:
                            self.rep_ending_y_pos = min(self.y_positions) + ref_radius
                            self.set_started = True
                    else:
                        if y_disp < -2 and x_disp < -2:
                            self.rep_ending_y_pos = min(self.y_positions) + ref_radius
                            self.set_started = True

                # set has started if movement has occurred
                if self.set_started:
                    # this is the starting point of the overall repetition
                    concentric_end_position_0 = (0, self.rep_ending_y_pos)
                    concentric_end_position_1 = (self.frame_width - 1, self.rep_ending_y_pos)
                    cv2.line(frame, concentric_end_position_0, concentric_end_position_1, (255, 0, 0), 2)

                # checking to verify that a downward movement has begun
                if self.set_started and not self.concentric_started:
                    if y_disp < -4:
                        self.eccentric_started = True
                        self.distance_check  = ((center[1] - self.rep_ending_y_pos) * mmpp) / 1000
        
                    # eccentric movement has ended, concentric movement starts
                    if y_distance_per_frame > 4 and self.eccentric_started:
                        self.bottom_x, self.bottom_y = center[0], center[1]
                        self.rep_starting_pos = self.bottom_y
                        self.concentric_started = True
                        self.rep_start_time_ns = time.perf_counter_ns()

                # if the set has started and concentric has started, we track the number of frames to occur
                elif self.set_started and self.concentric_started:
                    self.frame_count += 1

                    # if current y position is above the end position of the set start, a repetition is counted
                    if center[1] <= self.rep_ending_y_pos:
                        self.concentric_started = False
                        self.eccentric_started = False   

                        if self.distance_check < 0.1:
                            continue
                        
                        # primary functionality keeping track of the distance, nanoseconds and adjustments based on frames
                        self.rep_count += 1
                        rep_duration_ns = time.perf_counter_ns() - self.rep_start_time_ns
                        self.rep_duration_s = rep_duration_ns / 1_000_000_000
                        actual_fps = self.frame_count / self.rep_duration_s
                        adjustment_percentage = (self.fps/actual_fps)
                        self.top_finish_x, self.top_finish_y = center[0], center[1]
                        distance_metres = (abs(self.bottom_y - self.top_finish_y) * mmpp) / 1000
                        if self.right:
                            self.metres_per_second = (distance_metres / self.rep_duration_s) * adjustment_percentage
                        self.metres_per_second_list.append(self.metres_per_second)
                        self.frame_count = 0

                # Performance based metrics displayed to screen for user
                cv2.putText(frame, f"FPS: {self.fps:.2f}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.putText(frame, f"Repetitions: {self.rep_count}", (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.putText(frame, f"Seconds: {self.rep_duration_s}", (20, 160), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.putText(frame, f"Metres/Second: {self.metres_per_second:.2f}", (20, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                # draw a green line between the top and bottom range of the repetition, showing bar path
                rep_start_path = (self.bottom_x, self.bottom_y)
                rep_end_path = (self.top_finish_x, self.top_finish_y)

                if self.top_finish_x is not None and self.top_finish_y is not None:
                    cv2.line(frame, rep_start_path, rep_end_path, (0, 255, 0), 2)

                if self.is_inside_bounding_box(x, y) and self.set_started:
                    break

        # these series of counters check to see the expected frames to actual frames and allows for video to be shown in 
        # real time
        end_time_frame_ns = time.perf_counter_ns()
        processing_time_ns = end_time_frame_ns - start_time_frame_ns
        wait_time_ms = max((self.frame_delay_ns - processing_time_ns) // 1_000_000, 1)
        cv2.imshow('Frame', frame)

        return wait_time_ms

    def run(self):

        while not self.set_ended:
            ret, frame = self.cap.read()
            if not ret:
                break
            wait_time_ms = self.process_frame(frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.cap.release()
        cv2.destroyAllWindows()

        return self.metres_per_second_list


if __name__ == "__main__":
    video_path = './videos/day3/R_03_01E.MOV'
    processor = VideoProcessor(video_path, True)
    mps_list = processor.run()

    print(mps_list)
