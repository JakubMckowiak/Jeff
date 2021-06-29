#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

# Create your objects here.
ev3 = EV3Brick()

data = DataLog('s1,'+'s2,'+'s3,'+'s4,'+'L,'+'P' name = "Jeff_robi_skrrr", timestamp = False, append = False )

SKRMAX = 100
MOC = 100

motorP1 = Motor(Port.A)
motorP2 = Motor(Port.B, Direction.COUNTERCLOCKWISE)
motorL1 = Motor(Port.C)
motorL2 = Motor(Port.D, Direction.COUNTERCLOCKWISE)
sensor3 = ColorSensor(Port.S3)
sensor1 = ColorSensor(Port.S1)
sensor2 = ColorSensor(Port.S2)
sensor4 = ColorSensor(Port.S4)


#max min sensor
maxc1 = 97
minc1 = 6

maxc2 = 87
minc2 = 4

maxc3 = 73
minc3 = 2

maxc4 = 86
minc4 = 4

maxcL = (maxc1 + maxc3)
maxcP = (maxc2 + maxc4)

SKR = 0
SKR1 = 0
SKR2 = 0
SKR3 = 0
SKR4 = 0
mode = 0

def dataLoging(skret, moc):
    global data, mode
    # czas = watch.time()
    # Poniższa linika resetuje czas, tak aby program
    # mierzył odstępy czasowe
    # watch.reset()
    data.log(sensor1.reflection()+ ',' + sensor2.reflection()+ ',' + sensor3.reflection()+ ',' + sensor4.reflection()+ ',' + motorL1.speed()+ ',' + motorP1.speed())

def standard():
    
    global maxc1, minc1, maxc2, minc2, maxc3, minc3, maxc4, minc4, maxcL, maxcP, SKRMAX, SKR1, SKR2, SKR3, SKR4
    SKR1 = -(((SKRMAX*(sensor1.reflection()-maxcL))/(minc1-maxcL)))
    SKR2 = ((SKRMAX*(sensor2.reflection()-maxcP))/(minc2-maxcP))

def ustaw():
    
    global maxc1, minc1, maxc2, minc2, maxc3, minc3, maxc4, minc4, maxcL, maxcP, SKRMAX, SKR1, SKR2, SKR3, SKR4
    SKR = (SKR1 + SKR2 + SKR3 + SKR4)
    dataLoging(SKR, MOC)
    motorL1.run(MOC + SKR)
    motorL2.run(MOC + SKR)
    motorP1.run(MOC - SKR)
    motorP2.run(MOC - SKR)

def wszystko():
    global  mode, maxc1, minc1, maxc2, minc2, maxc3, minc3, maxc4, minc4, maxcL, maxcP, SKRMAX, SKR1, SKR2, SKR3, SKR4, SKR
    if (sensor3.reflection() < ((maxc3 + minc3)/2)) and (sensor4.reflection() < ((maxc4 + minc4)/2)):
        #mod 3 skrzyzowanie
        mode = 3
        standard()
        SKR3 = -(((SKRMAX*(sensor3.reflection()-maxcL))/(minc3-maxcL)))
        SKR4 = ((SKRMAX*(sensor4.reflection()-maxcP))/(minc4-maxcP))

        ustaw()

    elif sensor3.reflection() < (maxc3 + minc3)/2:
        # mod -1
        mode = -1
        while sensor1.reflection() > (maxc1+minc1)/2:
            standard()
            if(abs(SKR3) < ((SKRMAX*(sensor3.reflection()-maxcL))/(minc3-maxcL))):
                SKR3 = -(((SKRMAX*(sensor3.reflection()-maxcL))/(minc3-maxcL)))
            SKR1 = -(((SKRMAX*((maxc1+minc1)/2-maxcL))/(minc1-maxcL)))
                        
            SKR = (SKR1 + SKR3)
            ustaw()
        SKR3= 0

    elif sensor4.reflection() < (maxc4 + minc4)/2:
        # mode 1
        mode = 1
        while sensor2.reflection() > (maxc2+minc2)/2:
            standard()
            if(SKR4 < ((SKRMAX*(sensor4.reflection()-maxcP))/(minc4-maxcP))):
                SKR4  = ((SKRMAX*(sensor4.reflection()-maxcP))/(minc4-maxcP))
            SKR2 = ((SKRMAX*((maxc2+minc2)/2-maxcP))/(minc2-maxcP))
            
            SKR = (SKR2 + SKR4)
            ustaw()
        SKR4 = 0

    elif sensor4.reflection() < (maxc4 + minc4)/2 and sensor2.reflection() < (maxc2 + minc2)/2:
        # mode 2
        mode = 2
        while(sensor4.reflection()< ((maxc4 + minc4)/2) and sensor1.reflection()< ((maxc1 + minc1)/2) and sensor2.reflection()< ((maxc2 + minc2)/2)):
            if(SKR4 < ((SKRMAX*(sensor4.reflection()-maxcP))/(minc4-maxcP))):
                SKR4 = ((SKRMAX*(sensor4.reflection()-maxcP))/(minc4-maxcP))
            SKR2 = ((SKRMAX*(maxc2-maxcP))/(minc2-maxcP))
        while(sensor1.reflection()> ((maxc1 + minc1)/2)):
            if(SKR4 <((SKRMAX*(sensor4.reflection()-maxcP))/(minc4-maxcP))):
                SKR4 = ((SKRMAX*(sensor4.reflection()-maxcP))/(minc4-maxcP))
            SKR = (SKR2 + SKR4)
            ustaw()
        SKR4 = 0

    elif sensor3.reflection() < (maxc3 + minc3)/2 and sensor1.reflection() < (maxc1 + minc1)/2: #mode -2
		# mode -2
        mode = -2
        while sensor3.reflection() < ((maxc3 + minc3)/2) and sensor2.reflection() < ((maxc2 + minc2)/2) and sensor1.reflection()< ((maxc1 + minc1)/2):
			
            if(SKR3 > -(((SKRMAX*(sensor3.reflection()-maxcL))/(minc3-maxcL)))):
                SKR3 = -(((SKRMAX*(sensor3.reflection()-maxcL))/(minc3-maxcL)))
            SKR1 = -(((SKRMAX*(maxc1-maxcL))/(minc1-maxcL)))
			
        while(sensor2.reflection()> ((maxc2 + minc2)/2)):
			
            if(SKR3 > -(((SKRMAX*(sensor3.reflection()-maxcL))/(minc3-maxcL)))):
                SKR3 = -(((SKRMAX*sensor3.reflection()-maxcL))/(minc3-maxcL))
            SKR = (SKR1 + SKR3)
            ustaw()
			
        SKR3 = 0

    else:
        standard()
        # mode 0 prosto
        mode = 0
        SKR3 = -(((SKRMAX*(sensor3.reflection()-maxcL))/(minc3-maxcL)))
        SKR4 = ((SKRMAX*(sensor4.reflection()-maxcP))/(minc4-maxcP))
        SKR = (SKR1 + SKR2 + SKR3 + SKR4)
        ustaw()

#działanie

while(1==1):
    wszystko()

# watch = StopWatch()