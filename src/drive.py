import RPi.GPIO as GPIO
from time import sleep
import utils

INPUT = 0
OUTPUT = 1

LOW = 0
HIGH = 1

# PWM pin definition
LEFT = 15
RIGHT = 14

# Those pins does not any function, actually :D
LEFT_B = 2
RIGHT_B = 3


def setPwm(PWM):
    GPIO.setup(PWM, GPIO.OUT)
    pwm = GPIO.PWM(PWM, 100)
    pwm.start(0)
    return pwm


def setMotor(left, right):
    pwmLeft.ChangeDutyCycle(left)
    pwmRight.ChangeDutyCycle(right)


def driveAngle(angle):
        # Stop
    if(angle == None):
        setMotor(0, 0)
    else:
        # Turn right
        if(angle > 0):
            setMotor(100 * utils.speed, 30 * utils.speed)
        # Turn left
        else:
            setMotor(30 * utils.speed, 100 * utils.speed)


def initialize():
    global pwmLeft, pwmRight, pwmLeft_B, pwmRight_B
    GPIO.setmode(GPIO.BCM)

    pwmLeft = setPwm(LEFT)
    pwmRight = setPwm(RIGHT)
    pwmLeft_B = setPwm(LEFT_B)
    pwmRight_B = setPwm(RIGHT_B)


def clean():
    GPIO.cleanup()
