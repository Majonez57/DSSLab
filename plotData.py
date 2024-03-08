import csv
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

def read_variables_from_file(filename):
    timestamps = []
    variables = [[] for _ in range(17)]  # List of lists for 17 variables
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            timestamps.append(row[0])
            for i, value in enumerate(row[1:]):
                variables[i].append(float(value))
    return [round(float(x), 3) for x in timestamps], variables

def plot_variables(timestamps, variables):
    fig, axs = plt.subplots(17, 1, figsize=(10, 20), sharex=True)

    for i, ax in enumerate(axs):
        # Round x-axis values
        timestamps_dt = [ts for ts in timestamps]
        x_values = np.arange(len(timestamps))
        ax.plot(timestamps_dt, variables[i], label=f'Variable {i+1}')
        
        # Calculate sliding average
        window_size = 3  # You can adjust the window size
        sliding_avg = np.convolve(variables[i], np.ones(window_size)/window_size, mode='same')
        ax.plot(timestamps_dt, sliding_avg, label=f'Sliding Avg {i+1}', color='orange')
        
        ax.set_ylabel(f'Variable {i+1}')
        ax.grid(True)
        ax.legend()
    
    axs[-1].set_xlabel('Time')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Example Usage
timestamps, variables = read_variables_from_file('data2.csv')
plot_variables(timestamps, variables)
