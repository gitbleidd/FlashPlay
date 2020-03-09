#!/usr/bin/env python3

"""
  Скрипт, запускающий с флешки первый найденный mp3 или wav файл по нажатию кнопки
  Страница проекта (полное описание, установка): https://github.com/gitbleidd/FlashPlay
  Автор: gitBleidd, 2020
"""

import RPi.GPIO as GPIO
import pygame
import os, glob, time
import eyed3

BUTTON1 = 10 #GPIO пин кнопки
STD_BOUNCE_T = 2500 #Задержка после нажатия

def find_sound(): #Возвращает путь к первому найденному файлу на первой найденной флешке
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

    print('Error, no usb with mp3 or wav')
    return None

def button_callback(channel): #Функция, выполняющая действие при нажатии на кнопку
    print('Button pushed')
    sound_path = find_sound()
    if sound_path is not None:
        pygame.mixer.quit()
        song = eyed3.load(sound_path) #Загружаем файл в eyed3
        frq = song.info.sample_freq #Определяем частоту файла
        pygame.mixer.init(frequency=frq, size=-16, channels=2, buffer=4096)
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.set_volume(1) #0-min, 1-max
        pygame.mixer.music.play(0)

#Инициализация GPIO пинов
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(BUTTON1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(BUTTON1, GPIO.RISING, callback=button_callback, bouncetime=STD_BOUNCE_T)
print('GPIO inited')

try:
  while True:
    time.sleep(0.1)

finally:
  print ("cleanup() GPIOs")
  GPIO.cleanup()