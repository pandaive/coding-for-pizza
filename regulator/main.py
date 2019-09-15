#!/usr/bin/env python3

import cv2
import paho.mqtt.client as mqtt

import time
import threading
import subprocess

import image_recognition
import regulator

local = False  # True
subprocess_mqtt = True
withWorkCycle = False

imageToProcess = None

threadIdle = True
workCycleMode = False

client = None
if (not local and not subprocess_mqtt):
    client = mqtt.Client()
    client.connect("192.168.0.1", 1883, 60)

reg = regulator.AngleRegulator()

last_direction = "stop"

workcycleDegrees = [
(90 * 1, "right"),
(90 * 2, "right"),
(90 * 3, "right"),
(90 * 4, "right"),
(90 * 5, "right"),
(90 * 6, "right"),
(90 * 8, "right"),
(90 * 8, "right"),
(90 * 9, "right"),
(-1, "stop"),
(180, "left"),
(-1, "stop"),
    (180, "right"),
    (90, "right"),
(-1, "stop"),
    (180, "left"),
(180, "left"),
(180, "left"),
(180, "left"),
    (45, "left"),
(-1, "stop")

]
workcycle_i = 0


def thread_fn():
    global imageToProcess
    global threadIdle
    global last_direction
    global workCycleMode
    global workcycle_i
    while (1):
        if (imageToProcess is not None):
            threadIdle = False
            angle, im = image_recognition.get_angle(imageToProcess)

            cv2.imshow('VIDEO', im)
            cv2.waitKey(1)

            x, direction = reg.update(angle)

            #print("Direction {}".format(direction))

            if direction == "stop":
                if not local:
                    if subprocess_mqtt:
                        subprocess.run(["mosquitto_pub", "-h", "192.168.0.1", "-t", "move", "-m", "stop"])
                    else:
                        client.publish("move", payload="stop", qos=1, retain=True)
                # if (not workCycleMode and not withWorkCycle):
                #     break
                if (not workCycleMode and withWorkCycle):
                    workCycleMode = True
                    time.sleep(1)
                if workCycleMode:
                    global workcycle_i
                    t = workcycleDegrees[workcycle_i][0] % 360
                    dir = workcycleDegrees[workcycle_i][1]
                    reg.set_target(t)
                    reg.workcycle_direction = dir
                    if t < 0:
                        if subprocess_mqtt:
                            subprocess.run(["mosquitto_pub", "-h", "192.168.0.1", "-t", "move", "-m", "stop"])
                        else:
                            client.publish("move", payload="stop", qos=1, retain=True)
                        time.sleep(0.5)


                    workcycle_i += 1



            print("direction " + direction)
            print("angle {}".format(angle))

            if not local:
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
    #camera = cv2.VideoCapture("/home/wiktor/hackathon/vlc-record-2019-09-14-15h21m18s-rtsp___192.168.0.2_554-.mp4")

    if client:
        client.publish("freq", payload=str(1), qos=0, retain=False)

    while (1):

        ret, frame = camera.read()

        if (threadIdle):
            imageToProcess = frame

        #time.sleep(0.1)
