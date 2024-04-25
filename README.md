# BarbellTrackingProgram
 Using custom algorithms, Linear Regression models and charts, this set of Python scripts works together to track a user's Velocity to Load Profile

## Please Note
 Please start all scripts from the main directory, else errors will occur.

### Script Order
1. **'resize_videos.py'**
    - **Purpose**: Pre-process videos by removing unnecessary seconds and paring down to 720p format.
    - **Details**: This script keeps all videos into a more digestible size, opencv does not work well with 4k videos. An added bonus is that the videos play at several times the speed, with the addition of an algorithm in the contour_track_21.py script, this does not affect the accuracy of the captured m/s repetition data. It does mean that video_analysis_factory works through videos quicker.

2. **'contour_track_21.py'**
    - **Purpose**: Primary script, processes a singular video to get the metres per second during the barbell bench press
    - **Details**: This class creates videoprocessor objects, these objects can process videos to derive the average speed of the barbell and return in a list

3. **'starting_pos.py'**
    - **Purpose**: Gets the starting position of the barbell and sends back the co-ordinates of this in the form of a bounding box.
    - **Details**: Keeping this separate from the contour tracking gives an early indication that the tracking algorithm does not work, also keeps the primary script clearer and easier to read and keep bounding boxes separate from one another.

4. **'video_analysis_factory.py'**
    - **Purpose**: This script processes all videos held in the video folder and creates a csv file of speeds, repetitions and camera details based on captured and processed video data.
    - **Details**: This script means that the the contour_track_21.py processing script can be automated, multiple videos can be processed in minutes. A videoprocessing object is created for each video to process, information is received and written to csv file.

5. **'initialize_regression_model.py'**
    - **Purpose**: This script is primarily used to verify the accuracy of estimations derived from the Linear Regression models for the initial testing day and to get p-values etc. 
    - **Details**: The primary drawback is the lack of data for this initial data, 5 data points restricts how accurate any model is.

6. **'model_analysis.py'**
    - **Purpose**: This script is a Class version of the initialize_regression_model.py script with the added functionality of being able to make predictions based on data fed from successive days.
    - **Details**: This script creates Linear Regression models of speed vs rir, speed vs percentage and etc. from the testing day at the gym. Predictions can be made by passing a list to the class and are returned to the user in a tuple.

7. **'model_analysis_factory.py'**
    - **Purpose**: Script takes the average speed data from the video_info_sorted.csv file for each of the days of the study (1-4) A model_analysis object is created with the specific study day speed data passed to it, estimated RIR, Estimated 1RM, Estimated % of 1RM are written to a csv file. Additionally, the speed data originally derived from video_analysis_factory.py is added to the csv files. Each of the analysis files is separated by day.
    - **Details**: This script stores all estimations in 4 different analysis of each of the days. This final step prior to the creation of charts sorts data into a nicely formatted csv file that is easily accessed by the charting scripts. 

8. **'singular_day_charts.py'**
    - **Purpose**: This script shows a breakdown of all the repetitions within a singular day and their respective Estimated 1rm, Estimated % of 1RM, Estimated RIR and their average speeds. 
    - **Details**: This script attempts to show the accumulation of fatigue during a session and allows a breakdown of how each of the sets performed during a single day across different estimations. The script goes through each of the analysis results files.

9. **'comparative_day_charts.py'**
    -  **Purpose**: In comparison to the singular_day_charts.py script, this script attempts to compare each of the 4 days against eachother by selecting a singular repetition out of each of the 5 sets and comparing them. The variables used include Estimated 1rm, Estimated % of 1RM, Estimated RIR and average speeds
    - **Details**: This script attempts to show the accumulation of fatigue between sessions and allowing for comparisons. In order to keep it easy to view and compare, a single repetition is selected by the researcher.

### CSV Files
1. **'video_info_sorted.csv'**
    - **Information**: This contains the average speed data captured from the video_analysis_factory.py script. 
2. **'day_x_analysis.csv'**
    - **Information**: Each of these csv files has sorted estimated data derived from Linear Regression model estimation being used on the average speed data derived from the video_info_sorted.csv. These files can then be used to create the singular and comparative charts.