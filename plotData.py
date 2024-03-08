import csv
import matplotlib.pyplot as plt
from datetime import datetime

def read_variables_from_file(filename):
    timestamps = []
    variables = [[] for _ in range(9)]  # 9 variables
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            timestamps.append(row[0])
            for i, value in enumerate(row[1:]):
                variables[i].append(float(value))
    return [round(float(x),3) for x in timestamps], variables

def plot_variables(timestamps, variables):
    fig, ax1 = plt.subplots(figsize=(10, 6))

    color = 'tab:red'
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Variables 1-8', color=color)
    for i in range(8):
        ax1.plot(timestamps, variables[i], label=f'Variable {i+1}')
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('Variable 9', color=color)
    ax2.plot(timestamps, variables[8], label='Variable 9', color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()
    plt.title('9 Variables Over Time')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()

# Example Usage
timestamps, variables = read_variables_from_file('data.csv')
plot_variables(timestamps, variables)
