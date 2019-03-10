#!/usr/bin/env python3

import RPi.GPIO as GPIO
import pygame
import os, glob, time
a=[]
mp3_directory=[] # Каталоги всех mp3 на флешке



def check(): # Проверка флешки
    check_status = False
    tree = os.walk('//media/pi')
    for t in tree:
        a.append(t)
        break


    if len(a[0][1]) > 0:
        #print(a[0][1][0])
        flash_name = a[0][1][0]
        check_status = True
        for file in os.listdir("//media/pi/" + flash_name):
            if file.endswith(".mp3"):
                #print(os.path.join("//media/pi/" + flash_name, file)) #Выводит полную директорию музыкальных файлов
                mp3_directory.append(os.path.join("//media/pi/" + flash_name, file))

    else:
        print('Error, no usb folder')
        a.clear()
        mp3_directory.clear()
        tree = os.walk('//media/pi')
        for t in tree:
            a.append(t)
            break



    return(check_status)


def button_callback(channel):
    print('button pushed')

    if check():

        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
        pygame.mixer.music.load(mp3_directory[0])
        pygame.mixer.music.set_volume(2)
        pygame.mixer.music.play(0)
'''
        while pygame.mixer.music.get_busy() == True:
            continue
        pygame.quit()
'''


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


GPIO.add_event_detect(10,GPIO.RISING,callback=button_callback, bouncetime=1000)
print('add_event_detect')

try:
  while True:
    time.sleep(0.1)

finally:
  print ("cleanup() GPIOs")
  GPIO.cleanup()