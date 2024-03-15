import csv
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

varnames = ["AccelXLow", "AccelYLow", "AccelZLow", "AccelMLow",
            "GyroXLow", "GyroYLow", "GyroZLow", "GyroMLow",
            "AccelXTop", "AccelYTop", "AccelZTop", "AccelMTop",
            "GyroXTop", "GyroYTop", "GyroZTop", "GyroMTop",
            "SoundLow"]

varn = 17

def read_variables_from_file(filename):
    timestamps = []
    variables = [[] for _ in range(varn)] 
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            timestamps.append(row[0])
            for i, value in enumerate(row[1:]):
                variables[i].append(float(value))
    return [round(float(x), 3) for x in timestamps], variables

def plot_variables(timestamps, variables):
    fig, axs = plt.subplots(17, 1, figsize=(8, 20), sharex=True)

    for i, vars in enumerate(variables):

        ax = axs[i]
        
        # Round x-axis values
        timestamps_dt = [ts for ts in timestamps]
        x_values = np.arange(len(timestamps))
        
        ax.plot(timestamps_dt, vars, label=varnames[i])
        
        # Calculate sliding average
        window_size = 5 if i == len(variables)-1 else 3  # You can adjust the window size
        sliding_avg = np.convolve(vars, np.ones(window_size)/window_size, mode='same')
        ax.plot(timestamps_dt, sliding_avg, color='orange')
        
        
        if "Accel" in varnames[i]:
            ax.set_ylim(-3, 3)
        if "Gyro" in varnames[i]:
            ax.set_ylim(-500, 500)

        ax.grid(True)
        ax.legend()
    
    axs[-1].set_xlabel('Time')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Example Usage
num = 1

timestamps, variables = read_variables_from_file(f'Data/data{num}.csv')
plot_variables(timestamps, variables)
