import json
from time import sleep
import time

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

from api import *
from photon import box_closed


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(4, GPIO.IN, GPIO.PUD_UP)


reader = SimpleMFRC522()
token = getXSRFToken()
jwt = auth(token)


try:
    while True:
        id, text = reader.read()
        print("Card number read:")
        text = text.strip()
        print(text)
        cf = open('configuration.json')
        box_info = json.load(cf)
        cf.close()
        r = auth_box({'box_id': box_info['box_id'], 'rfid':text})
        if r == 'pass':
            print('green')
            GPIO.output(17, GPIO.HIGH)
            start_time = time.time()
            end_time = start_time + 10
            while time.time() < end_time:
                if box_closed():
                    GPIO.output(17, GPIO.LOW)
                    break
            GPIO.output(17, GPIO.LOW)
            content_closed = {'box_id': box_info['box_id'], 'box_state':'closed'}
            while not box_closed():
                GPIO.output(18, GPIO.HIGH)
                sleep(0.5)
                GPIO.output(18, GPIO.LOW)
                sleep(0.5)
            while update_state(content_closed) != 'box & deliveries updated':
                print("Update failure")
                pass
            print("Update success")
        else:
            print('red')
            GPIO.output(18, GPIO.HIGH)
            sleep(10)
            GPIO.output(18, GPIO.LOW)
except KeyboardInterrupt:
    GPIO.cleanup()
    raise
