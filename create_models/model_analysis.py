'''
This script uses most of the functionality derived from the initialize_regression_model.py script.
On top of that it tries to compare the results of days 1 - 4 against the regression models created by day 0 (test day)

The results of this script are sent back in the form of a tuple of 4 lists, Estimated RIR, Estimated 1RM, Estimated % and speed. 
'''

import statsmodels.api as sm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings

class ModelAnalysis:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.video_df = None
        self.day_0_results = None
        self.model_s_vs_percentage = None
        self.model_s_vs_rir = None
        self.model_rir_vs_percentage = None
        self.load_and_prepare_data()
        self.train_models()

    def load_and_prepare_data(self):
        self.video_df = pd.read_csv(self.csv_file)
        self.video_df['AverageSpeeds'] = self.video_df['AverageSpeeds'].apply(
            lambda x: [float(speed) for speed in x.strip('[]').split(', ')])
        self.day_0_results = self.video_df[self.video_df['SessionNumber'] == 0]

        # Original dataset speeds, weights, and percentages for model training
        self.original_speeds = np.array([speeds[0] for speeds in self.day_0_results['AverageSpeeds']])
        weights = np.array([70, 90, 100, 112.5, 120])
        self.rirs = np.array([abs(1 - reps) for reps in [22, 10, 6, 2, 1]])
        self.percentages = np.array([(weight / 120) * 100 for weight in weights])

    def train_models(self):
        speeds_with_const = sm.add_constant(self.original_speeds)
        rirs_with_const = sm.add_constant(self.rirs)
        self.model_s_vs_rir = sm.OLS(self.rirs, speeds_with_const).fit()
        self.model_rir_vs_percentage = sm.OLS(self.percentages, rirs_with_const).fit()
        self.model_s_vs_percentage = sm.OLS(self.percentages, speeds_with_const).fit()

    def predict_rir_from_speed(self, speed):
        speed_with_const = sm.add_constant(np.array([speed]), has_constant='add')
        predicted_rir = self.model_s_vs_rir.predict(speed_with_const)[0]
        return predicted_rir
    
    def predict_percentage_from_speed(self, speed):
        speed_with_const = sm.add_constant(np.array([speed]), has_constant='add')
        predicted_percentage = self.model_s_vs_percentage.predict(speed_with_const)[0]
        return predicted_percentage

    def predict_percentage_from_rir(self, rir):
        rir_with_const = sm.add_constant(np.array([rir]), has_constant='add')
        predicted_percentage = self.model_rir_vs_percentage.predict(rir_with_const)[0]
        return predicted_percentage

    def calculate_weight_from_percentage(self, percentage, weight=100):
        print(weight/percentage)
        return weight * (weight/percentage)

    def analyze_new_speeds(self, new_speeds):
        speeds = []
        predicted_rirs = []
        predicted_percentages = []
        predicted_weights = []
        for speed in new_speeds:
            predicted_rir = self.predict_rir_from_speed(speed)
            predicted_percentage = self.predict_percentage_from_speed(speed)
            estimated_weight = self.calculate_weight_from_percentage(predicted_percentage)
            speeds.append(speed)
            predicted_rirs.append(predicted_rir)
            predicted_percentages.append(predicted_percentage)
            predicted_weights.append(estimated_weight)

        return speeds, predicted_rirs, predicted_percentages, predicted_weights

        
# Example of using the class with new speeds
if __name__ == "__main__":
    analysis = ModelAnalysis("video_info_sorted.csv")
    # Read the CSV file into a DataFrame
    video_df = pd.read_csv("video_info_sorted.csv")

    # Convert 'AverageSpeeds' string to a list of floats
    video_df['AverageSpeeds'] = video_df['AverageSpeeds'].apply(lambda x: [float(speed) for speed in x.strip('[]').split(', ')])

    # Filter results for day 0
    day_1_results = video_df[video_df['SessionNumber'] == 1]
    # Extract the first value from the list of average speeds for each set
    average_speeds = [speeds[4] for speeds in day_1_results['AverageSpeeds']]
    analysis.analyze_new_speeds(average_speeds)
