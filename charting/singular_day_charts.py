import pandas as pd
import ast
import matplotlib.pyplot as plt


for i in range(1,5):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(f'~/Downloads/main_functionalityv4/analysis_results/day_{i}_analysis.csv')

    # Function to convert string representation of list to list
    def convert_to_list(s):
        return ast.literal_eval(s)

    # Apply the conversion function to relevant columns
    df[f'Day {i} Speeds'] = df['Speeds'].apply(convert_to_list)
    df[f'Day {i} Predicted RIR'] = df['Predicted RIR'].apply(convert_to_list)
    df[f'Day {i} Predicted Percentages'] = df['Predicted Percentages'].apply(convert_to_list)
    df[f'Day {i} Predicted Weights'] = df['Predicted Weights'].apply(convert_to_list)

    # Create a single figure and a set of subplots
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))  # 2x2 grid of plots, adjust size as needed

    # Flatten the array of axes for easier iteration
    axs = axs.flatten()

    # Titles for each subplot
    titles = [f'Day {i} Speeds', f'Day {i} Predicted RIR', f'Day {i} Predicted Percentages', f'Day {i} Predicted Weights']

    # Loop through each subplot and plot the corresponding data
    for ax, title in zip(axs, titles):
        for index, row in df.iterrows():
            ax.plot(row[title][:10], label=f'Set {index+1}')  # plot first 10 repetitions only
        ax.set_title(title)
        ax.set_xlabel('Repetitions')
        ax.legend()

    # Adjust layout to prevent overlap
    plt.tight_layout()

    # Display the plots
    plt.show()
