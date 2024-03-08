import sensors
import csv
import time
from time import sleep as zzz

POLLSIZE = 100
# accelerometer and magnetometer on any i2c pin
sensor_pins={ "accel":3,"gyro":3,"sound":0, "button":2}
sensors.set_pins(sensor_pins)

bx, by, bz = 0, 0 ,0
bgx, bgy, bgz = 0, 0 ,0
ss = 0

poll = POLLSIZE
take = False

timeinit = time.time()

def save_to_file(filename, vars):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        stamp = time.time() - timeinit
        writer.writerow([stamp] + vars)

while True:        

    # acceleration in x,y,z axes
    ax,ay,az=sensors.accel.get_xyz()
    # magnitude of acceleration
    am = sensors.accel.get_magnitude()
    # magnetic field strength in x,y,z axes
    rx,ry,rz=sensors.gyro.get_xyz() 
    # magnitude of magnetic field
    rm = sensors.gyro.get_magnitude()

    s=sensors.sound.get_level()
    

    if poll != 10:
        bx += ax
        by += ay
        bz += az

        bgx += rx
        bgy += ry
        bgz += rz

        ss += s

        poll +=1

    if poll == 10 and take == False:
        bx /= 10
        by /= 10
        bz /= 10

        bgx /= 10
        bgy /= 10
        bgz /= 10

        ss /= 10

        take = True
        

    #Set baseline
    if sensors.button.get_level() == 1:
        poll = 0
        take = False
        
    if poll == 0:
        save_to_file('data.csv', [round(x, 2) for x in [ax,ay,az,am,rx,ry,rz,rm,s]])
        print("PUNCH")
        print(f"Acceleration: {round(ax-bx,2)},{round(ay-by,2)},{round(az-bz,2)}, {round(am, 2)}")
        print(f"Gyro: {round(rx-bgx,2)},{round(ry-bgy,2)},{round(rz-bgz,2)},{round(rm,2)}")
        print(f"Sound: {s-ss}")
    
    zzz(0.05)