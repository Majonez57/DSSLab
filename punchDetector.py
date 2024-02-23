import sensors
from time import sleep as zzz

# accelerometer and magnetometer on any i2c pin
sensor_pins={ "accel":3,"gyro":3, "button":2}
sensors.set_pins(sensor_pins)

bx, by, bz = 0, 0 ,0
bgx, bgy, bgz = 0, 0 ,0

poll = 10
take = False

while True:        

    # acceleration in x,y,z axes
    ax,ay,az=sensors.accel.get_xyz()
    # magnitude of acceleration
    am = sensors.accel.get_magnitude()
    # magnetic field strength in x,y,z axes
    rx,ry,rz=sensors.gyro.get_xyz() 
    # magnitude of magnetic field
    rm = sensors.gyro.get_magnitude()
    

    if poll != 10:
        bx += ax
        by += ay
        bz += az

        bgx += rx
        bgy += ry
        bgz += rz

        poll +=1

    if poll == 10 and take == False:
        bx /= 10
        by /= 10
        bz /= 10

        bgx /= 10
        bgy /= 10
        bgz /= 10
        take = True
        

    #Set baseline
    if sensors.button.get_level() == 1:
        poll = 0
        take = False
        
    if (ax-bx)**2 + (ay-by)**2 + (az-bz)**2 > 1:
        print("PUNCH")
        print(f"Acceleration: {round(ax-bx,2)},{round(ay-by,2)},{round(az-bz,2)}, {round(am, 2)}")
        print(f"Gyro: {round(rx-bgx,2)},{round(ry-bgy,2)},{round(rz-bgz,2)},{round(rm,2)}")
    zzz(0.05)