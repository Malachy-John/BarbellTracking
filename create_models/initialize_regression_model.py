'''
This gives the user the chance to view what the Day 0 Linear model is like
The analysis_factory.py script uses the same functionality detailed here to test predictions and build
models of successive days

This script allows us to verify the usefullness of various models derived here, such as
RIR vs Percentage, Percentage vs Speed, Speed vs RIR.

'''

import statsmodels.api as sm
import numpy as np
import pandas as pd
import warnings
import matplotlib.pyplot as plt

# Suppress all warnings
warnings.filterwarnings('ignore')

# Read the CSV file into a DataFrame
video_df = pd.read_csv("video_info_sorted.csv")

# Convert 'AverageSpeeds' string to a list of floats
video_df['AverageSpeeds'] = video_df['AverageSpeeds'].apply(lambda x: [float(speed) for speed in x.strip('[]').split(', ')])

# Filter results for day 0
day_0_results = video_df[video_df['SessionNumber'] == 0]

# Define weights for each set
weights = {1: [70, 22], 2: [90, 10], 3: [100, 6], 4: [112.5, 2], 5: [120, 1]}

# Calculate estimated one rep max for each set and print
print("\nEstimated One Rep Max and RIR:")
for set_number, (weight, reps) in weights.items():
    rir = abs(1 - reps)  # Reps in Reserve
    estimated_1rm = weight * reps * 0.0333 + weight

# Calculate percentage of each weight with respect to 120 kg
percentages = [(weight / 120) * 100 for weight, _ in weights.values()]

# Extract the first value from the list of average speeds for each set
average_speeds = [speeds[0] for speeds in day_0_results['AverageSpeeds']]

# Weights, rirs, and average_speeds are numpy arrays
weights = np.array([70, 90, 100, 112.5, 120])
rirs = np.array([abs(1 - 22), abs(1 - 10), abs(1 - 6), abs(1 - 2), abs(1 - 1)])

# Adding a constant to the independent variables for the intercept
average_speeds_with_const = sm.add_constant(average_speeds)

# Average Speed vs. RIR Model
model_s_vs_rir = sm.OLS(rirs, average_speeds_with_const).fit()

# Assuming percentages and average_speeds are numpy arrays and have the same length
percentages_np = np.array(percentages)
average_speeds_np = np.array(average_speeds)
percentages_with_const = sm.add_constant(percentages_np)

# Average Speed vs. RIR Model
model_s_vs_rir = sm.OLS(percentages_np, average_speeds_with_const).fit()

# RIR vs Percentage of 1rm
rirs_with_const = sm.add_constant(rirs)  
model_rir_vs_percentage = sm.OLS(percentages_np, rirs_with_const).fit()

# Percentages vs. Average Speed Model
model_p_vs_s = sm.OLS(average_speeds_np, percentages_with_const).fit()

# Fit the model
percentages_with_const = sm.add_constant(percentages)
model_rir_vs_s = sm.OLS(average_speeds_np, rirs_with_const).fit()

predictions = model_rir_vs_s.predict(rirs_with_const)

# Plotting the regression results
plt.figure(figsize=(10, 6))
plt.scatter(rirs, average_speeds_np, color='blue', label='Data Points')
plt.plot(rirs, predictions, color='red', label='Regression Line')
plt.text(np.mean(rirs), np.mean(average_speeds_np), f'Coefficient: {model_rir_vs_s.params[1]:.4f}', fontsize=12)
plt.title('RIR vs. Average Speed')
plt.xlabel('Reps in Reserve (RIR)')
plt.ylabel('Average Speed (m/s)')
plt.legend()
plt.grid(True)
plt.show()

# Assuming model_s_vs_rir and model_rir_vs_percentage are pre-defined and trained

def predict_rir_from_speed(speed):
    speed_with_const = sm.add_constant(np.array([speed]), has_constant='add')
    predicted_rir = model_s_vs_rir.predict(speed_with_const)
    return predicted_rir[0]

def predict_percentage_from_rir(rir):
    rir_with_const = sm.add_constant(np.array([rir]), has_constant='add')
    predicted_percentage = model_rir_vs_percentage.predict(rir_with_const)
    return predicted_percentage[0]

def calculate_weight_from_percentage(percentage, max_weight=120):
    return percentage * max_weight / 100

print(average_speeds)

# Example usage
for v in average_speeds:
    speed_example = v
    predicted_rir = predict_rir_from_speed(speed_example)
    predicted_percentage = predict_percentage_from_rir(predicted_rir)
    estimated_weight = calculate_weight_from_percentage(predicted_percentage)

    print()
    print(f"Predicted RIR: {predicted_rir}")
    print(f"Predicted Percentage of Max Weight: {predicted_percentage}%")
    print(f"Estimated Weight Lifted: {estimated_weight} kg")
    print()

print(model_s_vs_rir.summary())
print(model_rir_vs_percentage.summary())
print(model_rir_vs_s.summary())