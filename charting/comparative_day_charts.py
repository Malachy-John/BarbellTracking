'''
This script builds comparative charts between the different days.

It does this by selecting a singular point from the 5 sets and compares them.

For Estimated 1RM calculations, it takes the first repetition of each set and it's respective estimated 1rm.
For Estimated RIR calculations it takes the second last rep of each set and its respective estimated RIR.
For Speeds it takes the final repetition of each set and its respective m/s variable.

Each of these variables are compared across successive days to attempt verification of fatigue build up.

'''

import pandas as pd
import ast
import matplotlib.pyplot as plt
import numpy as np

# Load the CSV file into a DataFrame
day_1_df = pd.read_csv('~/Downloads/main_functionalityv4/analysis_results/day_1_analysis.csv')
day_2_df = pd.read_csv('~/Downloads/main_functionalityv4/analysis_results/day_2_analysis.csv')
day_3_df = pd.read_csv('~/Downloads/main_functionalityv4/analysis_results/day_3_analysis.csv')
day_4_df = pd.read_csv('~/Downloads/main_functionalityv4/analysis_results/day_4_analysis.csv')

# Function to convert string representation of list to list
def convert_to_list(s):
    return ast.literal_eval(s)

# Apply the conversion function to relevant columns
for df in [day_1_df, day_2_df, day_3_df, day_4_df]:
    df['Speeds'] = df['Speeds'].apply(convert_to_list)
    df['Predicted RIR'] = df['Predicted RIR'].apply(convert_to_list)
    df['Predicted Percentages'] = df['Predicted Percentages'].apply(convert_to_list)
    df['Predicted Weights'] = df['Predicted Weights'].apply(convert_to_list)

# Function to compute estimated 1RM
def compute_estimated_1RM(df):
    estimated_1RM = []
    for index, row in df.iterrows():
        # Assuming 1RM is most accurate on the very first repetition
        estimated_1RM.append(row['Predicted Weights'][0])
    return estimated_1RM

# Function to compute estimated 1RM
def compute_estimated_rir(df):
    estimated_rir = []
    for index, row in df.iterrows():
        # Verifying the accuracy of the second last repetition's RIR
        estimated_rir.append(row['Predicted RIR'][-2])
    return estimated_rir

# Function to compute estimated 1RM
def compute_speeds(df):
    estimated_speed = []
    for index, row in df.iterrows():
        # Taking the speed of the last repetition
        estimated_speed.append(row['Speeds'][-1])
    return estimated_speed


# Compute estimated 1RM for each day
day_1_1RM = compute_estimated_1RM(day_1_df)
day_2_1RM = compute_estimated_1RM(day_2_df)
day_3_1RM = compute_estimated_1RM(day_3_df)
day_4_1RM = compute_estimated_1RM(day_4_df)


# Plotting estimated 1RM for each day
plt.figure(figsize=(10, 6))
plt.plot(day_1_1RM, label='Day 1')
plt.plot(day_2_1RM, label='Day 2')
plt.plot(day_3_1RM, label='Day 3')
plt.plot(day_4_1RM, label='Day 4')

plt.title('Estimated 1RM Comparison by Day')
plt.xlabel('Set')
plt.ylabel('Estimated 1RM')
plt.legend()

# Adjusting the x-ticks to ensure they represent sets in whole numbers
max_length = max(len(day_1_1RM), len(day_2_1RM), len(day_3_1RM), len(day_4_1RM))
plt.xticks(np.arange(max_length), np.arange(1, max_length + 1))

plt.show()


# Compute estimated 1RM for each day
day_1_rir = compute_estimated_rir(day_1_df)
day_2_rir = compute_estimated_rir(day_2_df)
day_3_rir = compute_estimated_rir(day_3_df)
day_4_rir = compute_estimated_rir(day_4_df)

# Plotting estimated RIR for each day
plt.figure(figsize=(10, 6))
plt.plot(day_1_rir, label='Day 1')
plt.plot(day_2_rir, label='Day 2')
plt.plot(day_3_rir, label='Day 3')
plt.plot(day_4_rir, label='Day 4')

plt.title('Estimated RIR Comparison by Day')
plt.xlabel('Set')
plt.ylabel('Estimated RIR')
plt.legend()

# Adjusting the x-ticks to ensure they represent sets in whole numbers
max_length = max(len(day_1_rir), len(day_2_rir), len(day_3_rir), len(day_4_rir))
plt.xticks(np.arange(max_length), np.arange(1, max_length + 1))

plt.show()

# Compute estimated 1RM for each day
day_1_rir = compute_speeds(day_1_df)
day_2_rir = compute_speeds(day_2_df)
day_3_rir = compute_speeds(day_3_df)
day_4_rir = compute_speeds(day_4_df)

# Plotting estimated RIR for each day
plt.figure(figsize=(10, 6))
plt.plot(day_1_rir, label='Day 1')
plt.plot(day_2_rir, label='Day 2')
plt.plot(day_3_rir, label='Day 3')
plt.plot(day_4_rir, label='Day 4')

plt.title('Estimated Speed Comparison by Day')
plt.xlabel('Set')
plt.ylabel('Estimated Speed')
plt.legend()

# Adjusting the x-ticks to ensure they represent sets in whole numbers
max_length = max(len(day_1_rir), len(day_2_rir), len(day_3_rir), len(day_4_rir))
plt.xticks(np.arange(max_length), np.arange(1, max_length + 1))

plt.show()