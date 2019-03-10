#!/usr/bin/env python3

import RPi.GPIO as GPIO
import pygame
import os, glob, time

def find_sound():
    a=[]
    tree = os.walk('/media/pi')
    for t in tree:
        a.append(t)
        break

    if len(a[0][1]) > 0:
        flash_name = a[0][1][0]
        print("flash drive found: " + flash_name)
        for file in os.listdir("/media/pi/" + flash_name):
            if file.endswith(".mp3") or file.endswith(".wav"):
                sound_path = os.path.join("/media/pi/" + flash_name, file)
                print("sound found at: " + sound_path)
                return sound_path
    else:
        print('Error, no usb folder')
        a.clear()
        tree = os.walk('/media/pi')
        for t in tree:
            a.append(t)
            break
    return None

def button_callback(channel):
    print('button pushed')
    sound_path = find_sound()
    if sound_path is not None:
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.set_volume(2)
        pygame.mixer.music.play(0)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(10, GPIO.RISING, callback=button_callback, bouncetime=1000)
print('GPIO inited')

try:
  while True:
    time.sleep(0.1)

finally:
  print ("cleanup() GPIOs")
  GPIO.cleanup()