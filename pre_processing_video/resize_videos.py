import cv2
import os

# Directory containing the videos
video_directory = './videos/unedited'

# Desired resolution
new_width = 1280
new_height = 720

# Iterate over each video file in the directory
for filename in os.listdir(video_directory):
    # Check if the file is a video (for simplicity, checking by extension)
    if filename.lower().endswith(('.mov', '.webm', '.avi')):  # Add or remove extensions as needed
        input_video_path = os.path.join(video_directory, filename)
        output_video_path = os.path.join(video_directory, os.path.splitext(filename)[0] + 'E.MOV')

        # Capture the input video
        cap = cv2.VideoCapture(input_video_path)

        # Get the original video's frame rate
        fps = cap.get(cv2.CAP_PROP_FPS)
        print(f"Original FPS: {fps} for {filename}")  # Verify the detected frame rateR

        # Calculate the number of frames to skip (13 seconds)
        frames_to_skip = int(fps * 1)

        # Define the codec and create a VideoWriter object to write the video
        fourcc = cv2.VideoWriter_fourcc(*'avc1')
        out = cv2.VideoWriter(output_video_path, fourcc, fps, (new_width, new_height))

        # Initialize a counter for frames processed
        frame_count = 0

        while True:
            # Read frame-by-frame
            ret, frame = cap.read()

            if not ret:
                break  # Break the loop if there are no frames left

            # Increment frame count
            frame_count += 1

            # Skip the first 13 seconds of frames
            if frame_count <= frames_to_skip:
                continue

            # Resize the frame
            resized_frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)

            # Write the resized frame to the output video
            out.write(resized_frame)

        # Release everything when the job is finished
        cap.release()
        out.release()

        print(f"Processed {filename}")
