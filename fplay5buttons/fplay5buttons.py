#!/usr/bin/env python3

"""
  Скрипт, запускающий mp3 файлы с флешки по нажатию одной из 5 кнопок
  Страница проекта (полное описание, установка): https://github.com/gitbleidd/FlashPlay
  Автор: gitBleidd, 2020
"""

import RPi.GPIO as GPIO
import pygame
import os, glob, time
import eyed3
from threading import Thread

#Пины светодиодов и кнопок
LED1 = 5
LED2 = 3
LED3 = 12
LED4 = 15
LED5 = 16
BUTTON1 = 7
BUTTON2 = 8
BUTTON3 = 10
BUTTON4 = 11
BUTTON5 = 13
STD_BOUNCE_T = 2500 #Время задержки после нажатия кнопки
#Соответсвие номера кнопки, светодиодов и их GPIO пинов
buttonPinDict = {1:BUTTON1, 2:BUTTON2, 3:BUTTON3, 4:BUTTON4, 5:BUTTON5}
ledPinDict = {1:LED1, 2:LED2, 3:LED3, 4:LED4, 5:LED5}

def find_sound(button_num): #Функция поиска пути к файлу
    a=[]
    tree = os.walk('/media/pi')
    for t in tree:
        a.append(t)
        break
        
    for fl_num in range(0, len(a[0][1])):
        if len(a[0][1]) > 0:
            flash_name = a[0][1][fl_num]
            print("Flash drive found: " + flash_name)
            file_name = str(button_num) + ".mp3"
            sound_path = "/media/pi/" + flash_name + "/" + file_name
            print("sound path = " + sound_path)
            return sound_path
    print('Error, no usb with mp3')
    return None

def turn_off_leds(): #Выключение всех светодиодов
    GPIO.output(LED1, GPIO.LOW)
    GPIO.output(LED2, GPIO.LOW)
    GPIO.output(LED3, GPIO.LOW)
    GPIO.output(LED4, GPIO.LOW)
    GPIO.output(LED5, GPIO.LOW)

def button_callback(button_num): #Действие по нажатию кнопки
    """ 
    #Тоже самое, что и ниже, но через библиотеку time
    tm_check = time.time() + 0.001
    while time.time() < tm_check:
        button_pin = button_channel(button_num)
        if GPIO.input(button_pin) == 0:
            print("False push")
            return
    """
    for i in range(0,10): #Проверка на ложное срабатывание (помехи и т.д.)
        if GPIO.input(buttonPinDict[button_num]) == 0:
            print("False push")
            return
    print('Button successfully pushed')
    #cleanup()
    turn_off_leds()
    sound_path = find_sound(button_num) #Найти путь к файлу
    if sound_path is not None:
        GPIO.output(ledPinDict[button_num], GPIO.HIGH) #Включить светодиод, соответствующий кнопке
        pygame.mixer.quit()
        song = eyed3.load(sound_path)
        frq = song.info.sample_freq
        pygame.mixer.init(frequency=frq, size=-16, channels=2, buffer=4096)
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play(0)

def end_music_led(): #Функция выключения светодиодов по окончанию музыки 
    SONG_END = pygame.USEREVENT + 1
    pygame.mixer.music.set_endevent(SONG_END)
    while True:
        for event in pygame.event.get():
            if event.type == SONG_END:
                print("The song ended!")
                turn_off_leds()
                break

#Инициализация пинов
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(BUTTON1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUTTON2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUTTON3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUTTON4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUTTON5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)
GPIO.setup(LED3, GPIO.OUT)
GPIO.setup(LED4, GPIO.OUT)
GPIO.setup(LED5, GPIO.OUT)
turn_off_leds()

#STANDART BOUNCE TIME = 2500!
GPIO.add_event_detect(BUTTON1, GPIO.RISING, callback=lambda *a: button_callback(1), bouncetime=STD_BOUNCE_T)
GPIO.add_event_detect(BUTTON2, GPIO.RISING, callback=lambda *a: button_callback(2), bouncetime=STD_BOUNCE_T)
GPIO.add_event_detect(BUTTON3, GPIO.RISING, callback=lambda *a: button_callback(3), bouncetime=STD_BOUNCE_T)
GPIO.add_event_detect(BUTTON4, GPIO.RISING, callback=lambda *a: button_callback(4), bouncetime=STD_BOUNCE_T)
GPIO.add_event_detect(BUTTON5, GPIO.RISING, callback=lambda *a: button_callback(5), bouncetime=STD_BOUNCE_T)

pygame.init()
#Запускает функцию выключения светодиодов при окончании музыки через поток
t = Thread(target = end_music_led, args=[])
t.start()
print('GPIO inited')

try:
  while True:
    time.sleep(0.1)

finally:
  print ("cleanup() GPIOs")
  GPIO.cleanup()
