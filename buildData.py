import csv
import numpy as np


classes = ["NoPunch", "Punch"]
features = ["AccelXLow", "AccelYLow", "AccelZLow", "AccelMLow",
            "GyroXLow", "GyroYLow", "GyroZLow", "GyroMLow",
            "AccelXTop", "AccelYTop", "AccelZTop", "AccelMTop",
            "GyroXTop", "GyroYTop", "GyroZTop", "GyroMTop",
            "SoundLow"]

files = [1,2,3]
TESTOFFSETS = [0, 2.4, 1.5]
featuren = len(features)

def getSensorDataFromFile(filen):
    filename = f'Data/data{filen}.csv'
    timestamps = []
    rows = [] 
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        init_time = float(next(reader)[0])  # Read the first line, convert to float
        for row in reader:
            timestamps.append(init_time + float(row[0]))  # Add to initial timestamp
            rows.append([round(float(value), 3) for value in row[1:]])
            
    return (timestamps, rows)

def getPunchDataFromFile(filen):
    filename = f'Labels/labels{filen}.txt'

    truth = []

    with open(filename, 'r') as label_file:
        for line in label_file:
            label_time = float(line.split(',')[0])
            truth.append(label_time+TESTOFFSETS[filen-1])
    
    return truth

def labelData(targetfile, fileindexes, gap=0.5):
    with open(targetfile, 'w') as file:
        labels = ','.join(features)
        file.write(f'Punch, {labels}\n')

        for i in fileindexes:
            data_time, data_values = getSensorDataFromFile(i)
            truth = getPunchDataFromFile(i)

            for i in range(len(data_values)):
                row = data_values[i]
                time = data_time[i]

                label = 0
                for t in truth:
                    if t-gap <= time <= t+gap: #Punch Detected
                        label = 1
                        break 
                
                data = ','.join(map(str, row))
                file.write(f'{label},{data}\n') #No Punch Detected


data_time, data_values = getSensorDataFromFile(1)
truth = getPunchDataFromFile(1)
labelData('constructedData/binPunches.csv', files)