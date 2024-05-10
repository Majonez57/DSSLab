import sensors
import csv
import time
from time import sleep as zzz
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from joblib import load

POLLSIZE = 100
# accelerometer and magnetometer on any i2c pin
sensor_pins={ "accel":3,"gyro":3, "accel2":2,"gyro2":2,"sound":0, "button":2}
sensors.set_pins(sensor_pins)

timeinit = time.time()

num = str(input("EnterTestNum: "))

FILE = f"Data/data{num}.csv"

model = load('pkls/finalized_model_mlp.bin')
model.verbose = False
pca = load('pkls/pca_tr_mlp.bin')
scaler = load('pkls/stdscl_tr_mlp.bin')

last_5 = []

def combine_dataframes(last_5):
    combined_df = pd.concat(last_5, axis=1)
    
    combined_series = combined_df.stack()
    
    combined_df_long = combined_series.reset_index(drop=True)
    
    return combined_df_long.to_frame()

while True:        

    # acceleration in x,y,z axes
    ax,ay,az=sensors.accel.get_xyz()
    ax2,ay2,az2=sensors.accel2.get_xyz()
    # magnitude of acceleration
    am = sensors.accel.get_magnitude()
    am2 = sensors.accel.get_magnitude()
    # magnetic field strength in x,y,z axes
    rx,ry,rz=sensors.gyro.get_xyz()
    rx2,ry2,rz2=sensors.gyro.get_xyz() 
    # magnitude of magnetic field
    rm = sensors.gyro.get_magnitude()
    rm2 = sensors.gyro.get_magnitude()
        
    #rawData = rawData.reshape(1,-1)

    last_5.extend([round(x,3) for x in [ax,ay,az,am,rx,ry,rz,rm,ax2,ay2,az2,am2,rx2,ry2,rz2,rm2]])

    if len(last_5) > 80:
        last_5 = last_5[16:]   
        print(last_5)
        rawData = np.array(last_5)
        rawData = pd.DataFrame(data=[rawData])
        inData = pca.transform(scaler.transform(rawData))
        out = model.predict(inData)


        if out == 1:
            print("LIGHT HIT")
        elif out == 2:
            print("MEDIUM HIT")
        elif out == 3:
            print("STRONG HIT")

        if out == 0:
            zzz(0.05)
        else:
            zzz(0.3)
    else:
        zzz(0.05)