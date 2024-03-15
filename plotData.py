import csv
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

varnames = ["AccelXLow", "AccelYLow", "AccelZLow", "AccelMLow",
            "GyroXLow", "GyroYLow", "GyroZLow", "GyroMLow",
            "AccelXTop", "AccelYTop", "AccelZTop", "AccelMTop",
            "GyroXTop", "GyroYTop", "GyroZTop", "GyroMTop",
            "SoundLow"]

def read_variables_from_file(filename):
    timestamps = []
    variables = [[] for _ in range(9)]  # List of lists for 9 variables
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            timestamps.append(row[0])
            for i, value in enumerate(row[1:]):
                variables[i].append(float(value))
    return [round(float(x), 3) for x in timestamps], variables

def plot_variables(timestamps, variables):
    fig, axs = plt.subplots(9, 1, figsize=(10, 20), sharex=True)

    for i, ax in enumerate(axs):
        # Round x-axis values
        timestamps_dt = [ts for ts in timestamps]
        x_values = np.arange(len(timestamps))
        ax.plot(timestamps_dt, variables[i], label=varnames[i])
        
        # Calculate sliding average
        window_size = 8 if i == len(variables)-1 else 4  # You can adjust the window size
        sliding_avg = np.convolve(variables[i], np.ones(window_size)/window_size, mode='same')
        ax.plot(timestamps_dt, sliding_avg, color='orange')
        
        ax.grid(True)
        ax.legend()
    
    axs[-1].set_xlabel('Time')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Example Usage
timestamps, variables = read_variables_from_file('data3.csv')
plot_variables(timestamps, variables)
