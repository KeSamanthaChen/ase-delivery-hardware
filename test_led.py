import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
gpio_pin = 17
GPIO.setup(gpio_pin,GPIO.OUT,initial=GPIO.LOW)

#sleep(3)
GPIO.output(gpio_pin,GPIO.HIGH)
sleep(3)
GPIO.output(gpio_pin,GPIO.LOW)


