from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
from time import sleep
import json

reader = SimpleMFRC522()

try:
    while True:
        id, text = reader.read()
        print(id, text)
        str = input("Overwrite the text content?(yes/no)")
        if str == "yes":
            info_n = input("New data:") 
            reader.write(info_n)
            sleep(5)
except KeyboardInterrupt:
    GPIO.cleanup()
    raise
