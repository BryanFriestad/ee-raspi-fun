import RPi.GPIO as GPIO
import time

x0_pin = 24 #blue
x1_pin = 25 #green
x2_pin = 26 #yellow
x3_pin = 27 #orange

display_state = 0 #unused currently

display_value = 0

def setup():
    global display_value
    #using broadcom mode for gpio numbering
    GPIO.setmode(GPIO.BCM)                                                              
    
    #set up pins
    GPIO.setup(x0_pin, GPIO.OUT, initial = display_value & 1)
    GPIO.setup(x1_pin, GPIO.OUT, initial = display_value & 2)
    GPIO.setup(x2_pin, GPIO.OUT, initial = display_value & 4)
    GPIO.setup(x3_pin, GPIO.OUT, initial = display_value & 8)

def clean_up():
    GPIO.cleanup([x0_pin, x1_pin, x2_pin, x3_pin])

def set_display(value):
    if(value < 16 and value >= 0):
        display_value = value
        x0_value = value & 1
        x1_value = value & 2
        x2_value = value & 4
        x3_value = value & 8
        GPIO.output(x0_pin, x0_value)
        GPIO.output(x1_pin, x1_value)
        GPIO.output(x2_pin, x2_value)
        GPIO.output(x3_pin, x3_value)
        return 0
    else:
        return -1

def reset_display():
    set_display(0)

def increment_display():
    global display_value
    return set_display(display_value + 1)

def decrement_display():
    global display_value
    return set_display(display_value - 1)

def get_display_value():
    global display_value
    return display_value

def main():
    setup()
    for x in range(16):
        set_display(x)
        time.sleep(0.5)

    for x in range(16):
        decrement_display()
        time.sleep(0.5)

    var = 0
    while(True):
        var = input("Input a number (0 - 15), \"g\" to get the displayed value, \"r\" to reset, or \"q\" to quit")
        if(var == 'q'):
            break
        elif(var == 'r'):
            reset_display()
        elif(var == 'g'):
            print("Currently displayed value is: ", get_display_value())
        else:       
            set_display(int(var))
    
    clean_up()

if __name__ == "__main__":
    main()
