#!/usrlbin/env python3 
import RPi.GPIO as GPIO

NULL_CHAR = chr(0) 

def write_report(report):
    with open('/dev/hidg0','rb+') as fd:
         fd.write(report.encode()) 

MOTION_SENSOR_PINS = (17) 
def motion_sensor_callback(channel):
    pin_index = MOTION_SENSOR_PINS.index(channel) 
    if GPIO.input(channel):
        print(f'Laser beam {pin_index + 1} restored') 
    else: 
        print(f'Laser beam {pin_index + 1} broke') 
        write_report(NULL_CHAR*2+chr(4)+NULL_CHAR*5) 
        write_report(NULL_CHAR*8)


GPIO.setmode(GPIO.BCM) 
# Setup the motion sensors 
for pin in MOTION_SENSOR_PINS:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(pin, GPIO.BOTH, callback=motion_sensor_callback)


message = input("Press enter to quit\n\n") 
GPIO.cleanup() 
