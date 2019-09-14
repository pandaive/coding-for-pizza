#!/usr/bin/env python3

import cv2
import paho.mqtt.client as mqtt

import image_recognition
import regulator


if __name__ == "__main__":
    client = mqtt.Client()

    client.connect("192.168.0.1", 1883, 60)

    camera = cv2.VideoCapture("rtsp://hackathon:!Hackath0n@192.168.0.2:554")
    #camera = cv2.VideoCapture("/home/wiktor/hackathon/vlc-record-2019-09-14-15h21m18s-rtsp___192.168.0.2_554-.mp4")



    reg = regulator.AngleRegulator()

    last_direction = "stop"

    client.publish("freq", payload=str(1), qos=0, retain=False)

    while (1):
        ret, frame = camera.read()

        #frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)


        angle, im = image_recognition.get_angle(frame)

        cv2.imshow('VIDEO', im)
        cv2.waitKey(1)

        x, direction = reg.update(angle)


        if (direction != last_direction):
            last_direction = direction
            print(direction)
            client.publish("move", payload=direction, qos=0, retain=False)