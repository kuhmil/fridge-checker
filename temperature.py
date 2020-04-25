import os
import glob
import time
import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

#relay_cold = 15
#relay_hot = 16

def blink():
    GPIO.setwarnings(False)    # Ignore warning for now
    GPIO.setmode(GPIO.BOARD)   # Use physical pin numbering
    GPIO.setup(7, GPIO.OUT, initial=GPIO.LOW)
    #while True: # Run forever
    GPIO.output(7, GPIO.HIGH) # Turn on
    sleep(1)                  # Sleep for 1 second
    GPIO.output(7, GPIO.LOW)  # Turn off
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

def relays():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(relay_cold, GPIO.OUT)
    GPIO.setup(relay_hot, GPIO.OUT)

    GPIO.output(relay_cold, False)
    GPIO.output(relay_hot, False)


while True:
    print(read_temp())
    time.sleep(1)
    if read_temp() < float(25):
        blink()
