#!/usr/bin/env python3

import cv2
import paho.mqtt.client as mqtt

import time
import threading

import image_recognition
import regulator

local = True

imageToProcess = None

threadIdle = True

client = None
if (not local):
    client = mqtt.Client()
    client.connect("192.168.0.1", 1883, 60)
reg = regulator.AngleRegulator()

def thread_fn():
    global imageToProcess
    global threadIdle
    while(1):
        if (imageToProcess is not None):
            threadIdle = False
            angle, im = image_recognition.get_angle(imageToProcess)

            cv2.imshow('VIDEO', im)
            cv2.waitKey(1)

            x, direction = reg.update(angle)

            print("direction " + direction)
            print("angle {}".format(angle))

            if client:
                client.publish("move", payload=direction, qos=0, retain=False)

            # time.sleep(0.2)
            #
            # if client:
            #     client.publish("move", payload="stop", qos=0, retain=False)

            imageToProcess = None
            threadIdle = True


if __name__ == "__main__":
    thread = threading.Thread(target=thread_fn)

    thread.start()



    #camera = cv2.VideoCapture("rtsp://hackathon:!Hackath0n@192.168.0.2:554")
    camera = cv2.VideoCapture("/home/wiktor/hackathon/vlc-record-2019-09-14-15h21m18s-rtsp___192.168.0.2_554-.mp4")

    if client:
        client.publish("freq", payload=str(1), qos=0, retain=False)

    while (1):


        ret, frame = camera.read()

        if (threadIdle):
            imageToProcess = frame

