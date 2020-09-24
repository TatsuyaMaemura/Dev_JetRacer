from jetracer.nvidia_racecar import NvidiaRacecar
car = NvidiaRacecar()
import numpy as np
import RPi.GPIO as GPIO
import time


# parameter setting
# 長さの単位はcm
isRoop = True

centerLine = 30
thresWidth = 15
facingAngleThres = 15

betweenSensors = 20


# steering setting
car.steering_gain = 1.0
car.steering_offset = 0.0

rightMax = 1.0
leftMax = -1.0

steerParam = 1.0 # steerParam * facingAngle で facingAngle[rad]曲がる


# throttle setting
car.throttle_gain = 0.5

speedHigh = 10
speedLow = 0.5


# *Distance are the acquired distance to the wall from each sensor
rightFrontDistance = np.empty(1)
rightRearDistance = np.empty(1)


# start time
startTime = time.time()


# Driving program
try:
    while isRoop:
        rightFrontDistance([0]) = getDistance() # Right front
        rightRearDistance([0]) = getDistance() # Right rear

        # Figure out status
        ## distance from car to the wall
        distance = np.mean([rightFrontDistance + rightRearDistance])
        farFromWall = distance > centerLine + thresWidth / 2
        closeToWall = distance < centerLine - thresWidth / 2

        ## rotaion of the car
        facingAngle = np.arctan((rightFrontDistance - rightRearDistance) / betweenSensors)
        # calcurate facing angle #


        if farFromWall:
            car.steering = rightMax
            car.throttle = speedLow
            # turning right #
        elif closeToWall:
            car.steering = leftMax
            car.throttle = speedLow
            #  turnning left #
        elif np.abs(facingAngle) > facingAngleThres:
            car.steering = steerParam * facingAngle
            car.throttle = speedLow
            # turning with appropriate angle #
        else:
            car.steering = 0.0 # keep sttering straight #
            car.throttle = speedHigh # Move Foward #


except KeyboardInterrupt:
    print('stop!')
    car.throttle = 0.0
    car.steering = 0.0
    GPIO.cleanup()
