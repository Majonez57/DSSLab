import sensors
import csv
import time
from time import sleep as zzz

POLLSIZE = 100
# accelerometer and magnetometer on any i2c pin
sensor_pins={ "accel":3,"gyro":3, "accel2":2,"gyro2":2,"sound":0, "button":2}
sensors.set_pins(sensor_pins)

timeinit = time.time()

def save_to_file(filename, vars):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        stamp = time.time() - timeinit
        writer.writerow([stamp] + vars)

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
        
    save_to_file('data.csv', [ax,ay,az,am,rx,ry,rz,rm,ax2,ay2,az2,am2,rx2,ry2,rz2,rm2,s])


    print(f"Acceleration: {round(ax,2)},{round(ay,2)},{round(az,2)}, {round(am, 2)}")
    print(f"Gyro: {round(rx, 2)},{round(ry,2)},{round(rz,2)},{round(rm,2)}")
    print(f"Sound: {s}")
    
    zzz(0.05)