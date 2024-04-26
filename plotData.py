import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
import numpy as np
import pandas as pd
from datetime import datetime

varnames = ["AccelXLow", "AccelYLow", "AccelZLow", "AccelMLow",
            "GyroXLow", "GyroYLow", "GyroZLow", "GyroMLow",
            "AccelXTop", "AccelYTop", "AccelZTop", "AccelMTop",
            "GyroXTop", "GyroYTop", "GyroZTop", "GyroMTop",
            "SoundLow"]

varn = 17

TESTNUM = 4
TESTOFFSETS = [0,-2.4,-1.5,-30] # Reaction time offset for each hit

def read_variables_from_file(filename):
    timestamps = []
    variables = [[] for _ in range(varn)] 
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        init_time = float(next(reader)[0])  # Read the first line, convert to float
        for row in reader:
            timestamps.append(init_time + float(row[0])+TESTOFFSETS[TESTNUM-1])  # Add to initial timestamp
            for i, value in enumerate(row[1:]):
                variables[i].append(float(value))
    return timestamps, variables

def plot_variables(timestamps, variables, window_size=10):
    fig, axs = plt.subplots(varn, 1, figsize=(10, 20), sharex=True)

    for i, vars in enumerate(variables):
        ax = axs[i]
        
        x_values = timestamps
        
        ax.plot(x_values, vars, label=varnames[i])
        
        # Calculate sliding average
        sliding_avg = np.convolve(vars, np.ones(window_size)/window_size, mode='same')
        ax.plot(x_values, sliding_avg, color='orange', label='Sliding Avg')
        
        if "Accel" in varnames[i]:
            ax.set_ylim(-3, 3)
        elif "Gyro" in varnames[i]:
            ax.set_ylim(-500, 500)

        ax.grid(True)
        ax.xaxis.set_major_locator(MultipleLocator(1))
        ax.legend(loc='upper right')
        #ax.set_ylabel(varnames[i])  # Set y-labels for each variable
    
    axs[-1].set_xlabel('Time')
    plt.xticks(rotation=45)
    
    # Read labels file and plot vertical lines
    with open(f'Labels/labels{TESTNUM}.txt', 'r') as labels_file:
        for line in labels_file:
            label_time = float(line.split(',')[0])
            for ax in axs:
                ax.axvline(x=label_time+0.5, color='red', linestyle='--', linewidth=1)

    plt.tight_layout()
    plt.show()

# Example Usage


timestamps, variables = read_variables_from_file(f'Data/data{TESTNUM}.csv')
plot_variables(timestamps, variables)
