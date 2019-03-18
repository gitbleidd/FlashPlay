#!/usr/bin/env python3

import RPi.GPIO as GPIO
import pygame
import os, glob, time
import eyed3

def find_sound(): #Song search function
    a=[]
    tree = os.walk('/media/pi')
    for t in tree:
        a.append(t)
        break
        
    for fl_num in range(0, len(a[0][1])):
        if len(a[0][1]) > 0:
            flash_name = a[0][1][fl_num]
            print("flash drive found: " + flash_name)
            for file in os.listdir("/media/pi/" + flash_name):
                if file.endswith(".mp3") or file.endswith(".wav"):
                    sound_path = os.path.join("/media/pi/" + flash_name, file)
                    print("sound found at: " + sound_path)
                    print(sound_path)
                    return sound_path

    print('Error, no usb with mp3')
    return None

def button_callback(channel): #Check button status function
    print('button pushed')
    sound_path = find_sound()
    if sound_path is not None:
        pygame.mixer.quit()
        song = eyed3.load(sound_path)
        frq = song.info.sample_freq
        pygame.mixer.init(frequency=frq, size=-16, channels=2, buffer=4096)
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.set_volume(2)
        pygame.mixer.music.play(0)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(10, GPIO.RISING, callback=button_callback, bouncetime=2500)
print('GPIO inited')

try:
  while True:
    time.sleep(0.1)

finally:
  print ("cleanup() GPIOs")
  GPIO.cleanup()