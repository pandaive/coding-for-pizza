#!/usr/bin/env python3

import cv2
import paho.mqtt.client as mqtt

import time
import threading
import subprocess

import image_recognition
import regulator

local = True  # True
subprocess_mqtt = True

imageToProcess = None

threadIdle = True

client = None
if (not local and not subprocess_mqtt):
    client = mqtt.Client()
    client.connect("192.168.0.1", 1883, 60)

reg = regulator.AngleRegulator()

last_direction = "stop"


def thread_fn():
    global imageToProcess
    global threadIdle
    global last_direction
    while (1):
        if (imageToProcess is not None):
            threadIdle = False
            angle, im = image_recognition.get_angle(imageToProcess)

            cv2.imshow('VIDEO', im)
            cv2.waitKey(1)

            x, direction = reg.update(angle)

            if direction == "stop":
                if subprocess_mqtt:
                    subprocess.run(["mosquitto_pub", "-h", "192.168.0.1", "-t", "move", "-m", "stop"])
                else:
                    client.publish("move", payload="stop", qos=1, retain=True)
                break

            print("direction " + direction)
            print("angle {}".format(angle))

            if client:
                if (direction != last_direction):
                    last_direction = direction
                    if subprocess_mqtt:
                        subprocess.run(["mosquitto_pub", "-h", "192.168.0.1", "-t", "move", "-m", direction])
                    else:
                        client.publish("move", payload=direction, qos=1, retain=True)
                    print("Sent {}".format(direction))

            # time.sleep(0.3)
            #
            # if client:
            #     if True:  # (direction != last_direction):
            #         last_direction = "stop"
            #         if subprocess_mqtt:
            #             subprocess.run(["mosquitto_pub", "-h", "192.168.0.1", "-t", "move", "-m", "stop"])
            #         else:
            #             client.publish("move", payload="stop", qos=1, retain=True)
            #         print("Sent {}".format("stop"))

            # #
            # if client:
            #     client.publish("move", payload="stop", qos=0, retain=False)

            imageToProcess = None
            threadIdle = True


if __name__ == "__main__":
    thread = threading.Thread(target=thread_fn)

    thread.start()

    camera = cv2.VideoCapture("rtsp://hackathon:!Hackath0n@192.168.0.2:554")
    # camera = cv2.VideoCapture("/home/wiktor/hackathon/vlc-record-2019-09-14-15h21m18s-rtsp___192.168.0.2_554-.mp4")

    if client:
        client.publish("freq", payload=str(1), qos=0, retain=False)

    while (1):

        ret, frame = camera.read()

        if (threadIdle):
            imageToProcess = frame

        # time.sleep(0.1)
