import os
import glob
import time
import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
from time import sleep
import datetime


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

#Sensors
relay_cold = 15
relay_hot = 16
#temp_probe = 13

def blink(pin):
    GPIO.setwarnings(False)    # Ignore warning for now
    GPIO.setmode(GPIO.BOARD)   # Use physical pin numbering
    GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
    #while True: # Run forever
    GPIO.output(pin, GPIO.HIGH) # Turn on
    sleep(1)                  # Sleep for 1 second
    GPIO.output(pin, GPIO.LOW)  # Turn off
    sleep(1) 

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c

#Relays
def relays(relay_change, state):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(relay_change, GPIO.OUT)
    GPIO.output(relay_change, state)

now = datetime.datetime.now().replace(second=0, microsecond=0)

try:
    while True:
        print(read_temp())
        print(now)
        if read_temp() < float(30):
            relays(relay_cold, True)
            #time.sleep(3)
        #while read_temp() < float(30) and read_temp() > float(1):
         #   relays(relay_cold, True)
            #time.sleep(3)
        #if read_temp() < float(1) and read_temp() > float(1):
         #   relays(relay_cold, True)
          #  time.sleep(300)
          #  relays(relay_cold, False)
           # time.sleep(2)
            #relays(relay_hot, True)
            #time.sleep(300)
            #if read_temp() > float(1) and read_temp() < float(10):
            #    relays(relay_hot, True)
            #else:
             #   relays(relay_hot, False)
        #else:
            #relays(relay_hot, False)
            #relays(relay_cold, False)
except KeyboardInterrupt:
    GPIO.cleanup()
