'''
This script picks up all contained videos stored in each of the video folders and uses
the VideoProcessor class to create processor objects, a loop occurs and all details derived
from the processing are stored to the "video_info_sorted.csv" file for further processing

Prior to starting this, it is suggested you change the "wait_time_ms" variable to 1 in the "contour_track_21.py" script
As this will speed up processing. 

'''

import contour_track_21 as vp
import os
import pprint
import pandas as pd

# Initialize variables
video_info_list = []
rep_check_results = []  # To store results of the rep checks
pp = pprint.PrettyPrinter(indent=4)

# Loop from day0 to day4
for day in range(0,5):  # Generates numbers 0 through 4
    video_folder = f'./videos/day{day}'
    
    for filename in os.listdir(video_folder):
        if filename.endswith(('.mp4', '.avi', '.MOV')):  # Add other video formats as needed
            print(filename)
            parts = filename.split('_')
            camera = parts[0]
    
            video_path = os.path.join(video_folder, filename)
            processor = vp.VideoProcessor(video_path, camera == "R")
            average_speeds = processor.run()
    
            if len(parts) >= 3:  # Ensure the filename has at least 3 parts
                session_id = parts[1]
                set_id = parts[2].split('.')[0]  # Remove file extension for the set_id
                set_number = int(set_id[0:2]) # Convert set_id to an integer for comparison
                
                video_info = {
                    'Camera': camera,
                    'SessionNumber': session_id,
                    'SetNumber': set_id,
                    'Filename': filename,
                    'AverageSpeeds': average_speeds,
                    'set_size': len(average_speeds),
                }
                video_info_list.append(video_info)
                
                # Check for days 1 through 4 and sets 1 through 4
                if 1 <= day <= 4 and 1 <= set_number <= 4:
                    rep_count = len(average_speeds)
                    if rep_count != 5:
                        rep_check_results.append(f"Camera {camera} Day {day}, Set {set_number} in session {session_id} has {rep_count} reps, expected 5.")

# Sort and process the list after collection
sorted_video_info_list = sorted(video_info_list, key=lambda x: (x['Camera'], x['SessionNumber'], x['SetNumber']))

# Convert to DataFrame and save
video_df = pd.DataFrame(sorted_video_info_list)
video_df.to_csv("video_info_sorted.csv", index=False)

# Print sorted list and any rep check issues
pp.pprint(sorted_video_info_list)
if rep_check_results:
    print("Issues found with repetition counts:")
    for result in rep_check_results:
        print(result)
else:
    print("All checked sets have the correct number of repetitions.")
