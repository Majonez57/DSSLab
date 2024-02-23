import sensors


# accelerometer and magnetometer on any i2c pin
sensor_pins={ "accel":3,
"magnetometer":3}
sensors.set_pins(sensor_pins)
while True:
    # acceleration in x,y,z axes
    ax,ay,az=sensors.accel.get_xyz()
    # magnitude of acceleration
    am = sensors.accel.get_magnitude()
    # magnetic field strength in x,y,z axes
    mx,my,mz=sensors.magnetometer.get_xyz() 
    # magnitude of magnetic field
    mm = sensors.magnetometer.get_magnitude()
    print(x,y,z,am,mx,my,mz,mm) 