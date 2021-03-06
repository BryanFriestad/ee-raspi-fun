import RPi.GPIO as GPIO
import time
import random as rand

#The EEPROM chip has addressing pins A0-A12, but A11 and A12 are tied to VDD
#This cuts the total addressing space to 2048 bytes
#Address are actually from 0x1800 to 0x1FFF
#But since we only address the lowest 11 bits, we can just check between 0 and 2047

address_pins = [23, 8, 7, 12, 16, 20, 21, 19, 6, 5, 9]
data_pins = [18, 15, 14, 2, 3, 4, 17, 22]
chip_en_pin = 10
out_en_pin = 11
write_en_pin = 13

curr_addr = 0

def setup():
    #using broadcom mode for gpio numbering
    GPIO.setmode(GPIO.BCM)
    
    #set up pins
    GPIO.setup(address_pins, GPIO.OUT)
    GPIO.setup(data_pins, GPIO.OUT) #these can be either, but start outputting (meaning write)
    GPIO.setup(chip_en_pin, GPIO.OUT)
    GPIO.setup(out_en_pin, GPIO.OUT)
    GPIO.setup(write_en_pin, GPIO.OUT)
    
def clean_up():
    GPIO.cleanup()
    
def enable_chip():
    GPIO.output(chip_en_pin, 0)
    
def disable_chip():
    GPIO.output(chip_en_pin, 1)
    
def enable_output():
    GPIO.output(out_en_pin, 0)
    
def disable_output():
    GPIO.output(out_en_pin, 1)
    
def enable_write():
    GPIO.output(write_en_pin, 0)
    
def disable_write():
    GPIO.output(write_en_pin, 1)

def set_address(address):
    global curr_addr
    
    if(address < 0 or address > 2047):
        return -1
    curr_addr = address
    GPIO.output(address_pins, getBinaryArray(address, 11))
    return 0

def get_address():
    return curr_addr

def increment_address():
    global curr_addr
    
    return set_address(curr_addr + 1)

def decrement_address():
    global curr_addr

    return set_address(curr_addr - 1)
    
def readDataPins():
    arr = []
    for x in data_pins:
        arr.append(GPIO.input(x))
    return formIntFromBinaryArray(arr)

def setDataPins(data):
    if(data < 0 or  data > 255):
        return -1
    GPIO.output(data_pins, getBinaryArray(data, 8))
    return 0

def read_addr(address):
    #set data pins to be input
    GPIO.setup(data_pins, GPIO.IN)
    
    #set control pins
    disable_write()
    enable_output()
    
    #set address
    if(set_address(address) == -1):
        return -1

    #read data at current address
    word = readDataPins()

    #disable output
    disable_output()

    return word

def write_addr(byte, address):
    #set data pins to be output
    GPIO.setup(data_pins, GPIO.OUT)
    
    #set address
    if(set_address(address) == -1):
        return -1

    #set control pins
    disable_output()
    enable_write() #locks the address in
    
    #read data
    setDataPins(byte)
    disable_write() #locks the data in
    
    time.sleep(0.01) #10 ms is max write cycle time
    return 0

def getBinaryArray(intVal, arrLength):
    arr = []
    bit = 1
    for x in range(arrLength):
        arr.append(intVal & bit)
        bit = bit * 2
    #print(arr)
    return arr

def formIntFromBinaryArray(arr):
    value = 0
    for i in range(len(arr)):
        value = value + (arr[i] << i)
    return value
    
def main():
    setup()
    enable_chip()
    
    inv_cnt = 0
    
    for x in range(100):
        value = rand.randrange(0, 256)
        adr = rand.randrange(0, 2048)
        
        write_addr(value, adr)
        read_value = read_addr(adr)
        
        if(value != read_value):
            inv_cnt = inv_cnt + 1
            print("Invalid write!")
            print("Writing ", value, " to address ", adr)
            print("Value at address ", adr, " is ", read_value)
            print()
        
    print("Done! ", inv_cnt, " invalid writes.")
    disable_chip()
    clean_up()

if __name__ == "__main__":
    main()
