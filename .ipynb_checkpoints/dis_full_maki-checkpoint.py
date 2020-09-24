#!/usr/bin/env python
# -*- coding: utf-8 -*-
# HC-SR04 ultrasonic range sensor
# with ADT7410 temperature sensor for sonic velocity correction
# ultrasonic
#   GPIO 17 output  = "Trig"
#   GPIO 27 input = "Echo"


#sensor1:rightfront
#sensor2:rightrear
#sensor3:left
#sensor4:front
 
import time
import RPi.GPIO as GPIO
import smbus
import random
import csv
import sys
 
# prepare for ADT7410 temperature sensor 
bus = smbus.SMBus(1)
address_adt7410 = 0x48
register_adt7410 = 0x00

# 保存ファイル名
saveName = "test092"
 
# prepare for HC-SR04 ultrasonic sensor
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#センサ1
GPIO.setup(26,GPIO.OUT)
GPIO.setup(19,GPIO.IN)
#センサ2
GPIO.setup(13,GPIO.OUT)
GPIO.setup(6,GPIO.IN)
#センサ3
GPIO.setup(11,GPIO.OUT)
GPIO.setup(9,GPIO.IN)
#センサ4
GPIO.setup(17,GPIO.OUT)
GPIO.setup(27,GPIO.IN)

# detect temperature in C
def readTemp():
    word_data =  bus.read_word_data(address_adt7410, register_adt7410)
    data = (word_data & 0xff00)>>8 | (word_data & 0xff)<<8
    data = data>>3 # 13ビットデータ
    if data & 0x1000 == 0:  # 温度が正または0の場合
        #temperature = data*0.0625
        pass
    else: # 温度が負の場合、 絶対値を取ってからマイナスをかける
    #    temperature = ( (~data&0x1fff) + 1)*-0.0625
        pass
    temperature = 20 # ここで温度を指定！
    return temperature
 
#sensor
def readSonic(sensor, temp):    
    if sensor == 1:
        GPIO.output(26, GPIO.LOW) 
        time.sleep(0.3)
        # send a 10us plus to Trigger
        GPIO.output(26, True)
        time.sleep(0.00001)        
        GPIO.output(26, False)
        # detect TTL level signal on Echo
        while GPIO.input(19) == 0:
            signaloff = time.time()
        while GPIO.input(19) == 1:
            signalon = time.time()
        
    elif sensor == 2:
        GPIO.output(13, GPIO.LOW)
        time.sleep(0.3)
        # send a 10us plus to Trigger
        GPIO.output(13, True)
        time.sleep(0.00001)        
        GPIO.output(13, False)
        # detect TTL level signal on Echo
        while GPIO.input(6) == 0:
            signaloff = time.time()
        while GPIO.input(6) == 1:
            signalon = time.time()
        
    elif sensor == 3:
        GPIO.output(11, GPIO.LOW)
        time.sleep(0.3)
        # send a 10us plus to Trigger
        GPIO.output(11, True)
        time.sleep(0.00001)        
        GPIO.output(11, False)
        # detect TTL level signal on Echo
        while GPIO.input(9) == 0:
            signaloff = time.time()
        while GPIO.input(9) == 1:
            signalon = time.time()
        
    elif sensor == 4:
        GPIO.output(17, GPIO.LOW) 
        time.sleep(0.3)
        # send a 10us plus to Trigger
        GPIO.output(17, True)
        time.sleep(0.00001)        
        GPIO.output(17, False)
        # detect TTL level signal on Echo
        while GPIO.input(27) == 0:
            signaloff = time.time()
        while GPIO.input(27) == 1:
            signalon = time.time()
            
    else:
        print("Incorrect usonic() function varible.")
            
    # calculate the time interval
    timepassed = signalon - signaloff
         
    # we now have our distance but it's not in a useful unit of
    # measurement. So now we convert this distance into centimetres
    distance = timepassed * (331.50 + 0.606681 * temp) * 100 / 2
         
    # return the distance of an object in front of the sensor in cm
    return distance
         
    # we're no longer using the GPIO, so tell software we're done
    GPIO.cleanup()
 
    