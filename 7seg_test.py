import RPi.GPIO as GPIO
import time

def toggleValue(v):
    if(v == GPIO.LOW):
        return GPIO.HIGH
    elif(v == GPIO.HIGH):
        return GPIO.LOW
    else:
        return v
    
def setPinsToNumber(num):
    if(num < 16 and num >= 0):
        x0_value = num & 1
        x1_value = num & 2
        x2_value = num & 4
        x3_value = num & 8
        GPIO.output(x0_pin, x0_value)
        GPIO.output(x1_pin, x1_value)
        GPIO.output(x2_pin, x2_value)
        GPIO.output(x3_pin, x3_value)

#using broadcom mode for gpio numbering
GPIO.setmode(GPIO.BCM)

x0_pin = 24 #blue
x1_pin = 25 #green
x2_pin = 26 #yellow
x3_pin = 27 #orange
x0_value = GPIO.LOW
x1_value = GPIO.LOW
x2_value = GPIO.LOW
x3_value = GPIO.LOW

#set up pins
GPIO.setup(x0_pin, GPIO.OUT)
GPIO.setup(x1_pin, GPIO.OUT)
GPIO.setup(x2_pin, GPIO.OUT)
GPIO.setup(x3_pin, GPIO.OUT)
#set initial states
GPIO.output(x0_pin, x0_value)
GPIO.output(x1_pin, x1_value)
GPIO.output(x2_pin, x2_value)
GPIO.output(x3_pin, x3_value)

x0_value = GPIO.HIGH
GPIO.output(x0_pin, x0_value)
time.sleep(1)

x1_value = GPIO.HIGH
GPIO.output(x1_pin, x1_value)
time.sleep(1)

x2_value = GPIO.HIGH
GPIO.output(x2_pin, x2_value)
time.sleep(1)

x3_value = GPIO.HIGH
GPIO.output(x3_pin, x3_value)
time.sleep(1)

setPinsToNumber(0)

var = 0
while(True):
    var = input("Input a number (0 - 15) or \"q\" to quit")
    if(var == "q"):
        break
    setPinsToNumber(int(var))

GPIO.cleanup()