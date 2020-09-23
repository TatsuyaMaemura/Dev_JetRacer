import numpy as np
# parameter setting
isRoop = True

centerLine = 30
thresWidth = 15
faceingAngleThres = 15

# *Distance are the acquired distance to the wall fron each sensor
rightFrontDistance = np.empty(1) 
rightRierDistance = np.empty(1)

while isRoop:
    rightFrontDistance([0]) = getDistance() # Right front
    rightRierDistance([0]) = getDistance() # Right rier 

    # Figure out statous
    ## distance from car to the wall
    distance = np.mean([rightFrontDistance + rightRierDistance])
    farFromWall = distance > centerLine + thresWidth / 2
    closeToWall = distance < centerLine - thresWidth / 2

    ## rotaion of the car
    faceingAngle = # calcurate facing angle #


    if farFromWall:
        # turning right #
    elif closeToWall:
        #  turnning left #
    else
        if np.abs(faceingAngle) > facingAngleThres
        # turning with appropriate angle #
        else
        # keep sttering straight #

    # Move Foward #