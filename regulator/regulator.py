#!/usr/bin/env python3

from simple_pid import PID
import time

class AngleRegulator:
    pid = PID(1/360 / 10, 0.1, 0.05, setpoint=0)


    target = 0
    direction = "stop"

    delta = 20  # degrees

    def __init__(self):
        maxSpeed = 1# 5
        self.pid.output_limits = (0, maxSpeed)
        self.pid.sample_time = 0.05

    def set_target(self, target_degrees):
        self.target = target_degrees
        self.pid.setpoint = target_degrees

    def update(self, currentAngleDegrees):
        # returns tuple (direction, speed) where direction can be [left|right|stop]
        direction = "stop"

        direction_left = True

        if (currentAngleDegrees > self.target):
            direction_left = True
        else:
            direction_left = False

        if (abs(currentAngleDegrees - self.target) > 180):
            direction_left = not direction_left
            currentAngleDegrees = currentAngleDegrees - 180

        print("Diff is {}".format(abs(currentAngleDegrees - self.target)))

        if (abs(currentAngleDegrees - self.target) < self.delta):
            direction = "stop"
        elif direction_left:
            direction = "left"
        else:
            direction = "right"

        z = -currentAngleDegrees if currentAngleDegrees > self.target else currentAngleDegrees

        out = self.pid(z)

        return out, direction



if __name__ == "__main__":
    reg = AngleRegulator()
    reg.set_target(0)

    print(reg.update(100))
    time.sleep(0.10)
    print(reg.update(100))
    time.sleep(0.10)
    print(reg.update(100))
    time.sleep(0.10)
    print(reg.update(100))
    time.sleep(0.10)

    print(reg.update(90))
    time.sleep(0.10)
    print(reg.update(80))
    time.sleep(0.10)
    print(reg.update(70))
    time.sleep(0.10)
    print(reg.update(60))
    time.sleep(0.10)
    print(reg.update(50))
    time.sleep(0.10)
    print(reg.update(40))
    time.sleep(0.10)
    print(reg.update(30))
    time.sleep(0.10)
    print(reg.update(20))
    time.sleep(0.10)
    print(reg.update(10))
    time.sleep(0.10)
    print(reg.update(0))
    time.sleep(0.10)
    print(reg.update(0))