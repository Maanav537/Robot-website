0#!/usr/bin/python3
# coding=utf8
import sys
import math
import time
import signal
import common.mecanum as mecanum

#Turning:
# 180degrees/s

# Forward:
# 50: 13.5in 343mm/s
# 100: 17in/s 430mm/s
# 25: 7in/s 170mm/s
# 28.57: 200mm/s - The standard

# Right:
# 50: 11in/s 280mm/s
# 100: 13.5in/s 342mm/s
# 25: 6in/s 150mm/s
# 33.22: 200mm/s - The standard

# Left:
# 50: 11in/s 280mm/s
# 100: 13.5in/s 342mm/s
# 25: 6in/s 150mm/s
# 33.22: 20#!/usr/bin/python3
#   90
#180   0
#  270

chassis = mecanum.MecanumChassis()
def moveForward(vel,t):
    #vel is velocity in mm/s.
    chassis.set_velocity(vel,90,0)
    time.sleep(t)
    chassis.set_velocity(0,0,0)

def moveRight(vel,t):
    #vel is velocity in mm/s.
    chassis.set_velocity(vel,0,0)
    time.sleep(t)
    chassis.set_velocity(0,0,0)
    
def moveBackward(vel,t):
    #vel is velocity in mm/s.
    chassis.set_velocity(vel,270,0)
    time.sleep(t)
    chassis.set_velocity(0,0,0)
    
def moveLeft(vel,t):
    #vel is velocity in mm/s.
    chassis.set_velocity(vel,180,0)
    time.sleep(t)
    chassis.set_velocity(0,0,0)
    
def moveDiagonal(vel,t,d):
    #vel is velocity in mm/s.
    #   90
    #180   0
    #  270
    chassis.set_velocity(vel,d,0)
    time.sleep(t)
    chassis.set_velocity(0,0,0)
    
def turn(s,t):
    #s is from -2 to 2
    #5 degrees a second.
    #2 is clockwise
    #-2 is counterclockwise
    chassis.set_velocity(0,0,s)
    time.sleep(t)
    chassis.set_velocity(0,0,0)
    
    
def sepVel(inputV):
	#solve for LR velocity (mm/s)
    LRv = (-0.0528 * inputV ** 2) + (9.16 * inputV) - 46 #debugging
    print(f"Left and Right MM/S = {LRv}")
    print(f"Left and Right FT/S = {LRv / 304.8}")
    #LRv = left right velocity
    # solve for FW velocity
    a = -0.06907
    b = 12.10
    c = -(89.33 + LRv)

    discriminant = b**2 - 4*a*c

    if discriminant < 0:
        return None  # No real solution

    sqrt_discriminant = math.sqrt(discriminant)
    
    x1 = (-b + sqrt_discriminant) / (2 * a)
    x2 = (-b - sqrt_discriminant) / (2 * a)
    FBv = (-0.06907 * x1 ** 2) + (12.10 * x1) - 89.33
    print(f"Forward and Backward MM/S = {FBv}")
    print(f"Forward and Backward FT/S = {FBv / 304.8}")
    return x1


def getRPM(mms):
	diamm = 2.5 * 25.4 #diameter of the wheels is 2.5, this converts to mm
	rpm = (mms * 60) / (math.pi * diamm)
	print(f"RPM is {rpm}")
	return rpm
	
def testMecanum(velocity=100):
	#velocity = 100  # User-defined input from 0–100

	# Get forward/backward velocity from sepVel and print all details
	fb_velocity = sepVel(velocity)

	# Get left/right velocity from sepVel math directly
	lr_velocity = (-0.0528 * velocity ** 2) + (9.16 * velocity) - 46

	# Print RPMs
	print("\nRPM Calculations:")
	print("LEFT/RIGHT RPM:")
	getRPM(lr_velocity)
	print("FORWARD/BACKWARD RPM:")
	getRPM(fb_velocity)

	print("\nMoving Robot:")

	# Move in all 4 directions for 1 second
	print("→ Moving FORWARD for 1 second")
	moveForward(fb_velocity, 1)

	print("→ Moving BACKWARD for 1 second")
	moveBackward(fb_velocity, 1)

	print("→ Moving LEFT for 1 second")
	moveLeft(lr_velocity, 1)

	print("→ Moving RIGHT for 1 second")
	moveRight(lr_velocity, 1)
	#use testMecanum() to test if it works
