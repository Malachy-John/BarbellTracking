'''
Using the analysis_factory.py script, this script predicts each of the results from day's 1 - 4 against
the regression model as created from the day0 results. 

The Predicted RIR, Speed & percentages are then stored in analysis files for each day.

'''

from create_models.model_analysis import ModelAnalysis
import pandas as pd

analysis = ModelAnalysis("video_info_sorted.csv")
# Read the CSV file into a DataFrame
video_df = pd.read_csv("video_info_sorted.csv")

# Convert 'AverageSpeeds' string to a list of floats
video_df['AverageSpeeds'] = video_df['AverageSpeeds'].apply(lambda x: [float(speed) for speed in x.strip('[]').split(', ')])

# Filter results for day 0
for i in range(1, 5):
    day_results = video_df[video_df['SessionNumber'] == i]
    # Extract the first value from the list of average speeds for each set
    average_speeds = day_results['AverageSpeeds']

    sets_dict = {f"Set {i+1}": speed for i, speed in enumerate(average_speeds)}

    # Find the length of the longest list
    max_length = max(len(lst) for lst in sets_dict.values())

    # Fill missing values with NaN
    for key in sets_dict:
        if len(sets_dict[key]) < max_length:
            sets_dict[key].extend([None] * (max_length - len(sets_dict[key])))

    # Convert dictionary to DataFrame
    df = pd.DataFrame(sets_dict)

    new_column_names = {old_col: f'Rep {i+1}' for i, old_col in enumerate(df.columns)}
    df.rename(columns=new_column_names, inplace=True)

    sets_dict_modified = df.to_dict()
    def remove_nan_values_nested(d):
        return {k: {k2: v2 for k2, v2 in v.items() if v2 == v2} for k, v in d.items()}

    # Apply function to remove NaN values
    sets_dict_modified = remove_nan_values_nested(sets_dict_modified)

    # Convert to desired format
    desired_data = {key: list(value.values()) for key, value in sets_dict_modified.items()}
    upper_dict = {}
    dict_of_vals = {}
    t_list = []

    for v in desired_data:
        speeds, predicted_rirs, predicted_percentages, predicted_weights = analysis.analyze_new_speeds(desired_data[v])
        print(v.split(" ")[1])
        rep_value = f"Set {v.split(' ')[1]}"

        dict_of_vals = {
                        'Speeds': speeds,
                        'Predicted RIR': predicted_rirs,
                        'Predicted Percentages': predicted_percentages,
                        'Predicted Weights': predicted_weights,

                    }
        
        upper_dict[rep_value]= dict_of_vals

    df = pd.DataFrame(upper_dict)
    df.T.to_csv(f"day_{i}_analysis.csv")