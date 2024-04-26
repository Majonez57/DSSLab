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

model = load('pkls/finalized_model.bin')
model.verbose = False
pca = load('pkls/pca_tr.bin')
scaler = load('pkls/stdscl_tr.bin')

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

    s =sensors.sound.get_level()
        
    rawData = pd.DataFrame(data=np.array([round(x,3) for x in [ax,ay,az,am,rx,ry,rz,rm,ax2,ay2,az2,am2,rx2,ry2,rz2,rm2,s]]),
                           columns = ["AccelXLow", "AccelYLow", "AccelZLow", "AccelMLow",
                                      "GyroXLow", "GyroYLow", "GyroZLow", "GyroMLow",
                                      "AccelXTop", "AccelYTop", "AccelZTop", "AccelMTop",
                                      "GyroXTop", "GyroYTop", "GyroZTop", "GyroMTop",
                                      "SoundLow"])
    rawData = rawData.reshape(1,-1)

    inData = pca.transform(scaler.transform(rawData))

    out = model.predict(inData)

    print(out)
    
    zzz(0.05)