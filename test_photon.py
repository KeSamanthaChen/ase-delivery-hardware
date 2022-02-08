import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4, GPIO.IN, GPIO.PUD_UP)

while True:
    if GPIO.input(4) == 0:
        sleep(1)
        print("light status")
    else:
        sleep(1)
        print("dark status")