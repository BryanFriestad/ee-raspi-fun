import RPi.GPIO as GPIO
import time

address_pins = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
data_pins = [13, 14, 15, 16, 17, 18, 19, 20]
chip_en_pin = 21
out_en_pin = 22
write_en_pin = 23

def registerPins():
    #using broadcom mode for gpio numbering
    GPIO.setmode(GPIO.BCM)
    
    #set up pins
    GPIO.setup(address_pins, GPIO.OUT)
    GPIO.setup(data_pins, GPIO.OUT) #these can be either, but start outputting
    GPIO.setup(chip_en_pin, GPIO.OUT)
    GPIO.setup(out_en_pin, GPIO.OUT)
    GPIO.setup(write_en_pin, GPIO.OUT)
    
def cleanUp():
    GPIO.cleanup()
    
def enableChip():
    GPIO.output(chip_en_pin, 0)
    
def disableChip():
    GPIO.output(chip_en_pin, 1)
    
def enableOutput():
    GPIO.output(out_en_pin, 0)
    
def disableOuput():
    GPIO.output(out_en_pin, 1)
    
def enableWrite():
    GPIO.output(write_en_pin, 0)
    
def disableWrite():
    GPIO.output(write_en_pin, 1)
    
def getBinaryArray(intVal, arrLength):
    arr = []
    bit = 1
    for x in range(arrLength):
        arr.append(intVal & bit)
        bit = bit * 2
    print(arr)
    return arr

def formIntFromBinaryArray(arr):
    value = 0
    for i in range(arr.length()):
        value = value + (arr[i] << i)
    return value
    
def setAddressPins(address):
    if(address < 0 or address > 4096):
        return
    GPIO.output(address_pins, getBinaryArray(address, 12))
    
def setDataPins(data):
    if(data < 0 or data > 256):
        return
    GPIO.output(data_pins, getBinaryArray(data, 8))
    
def readDataPins():
    arr = []
    for x in data_pins:
        arr.append(GPIO.input(x))
    return formIntFromBinaryArray(arr)

def readWord(address):
    #set data pins to be input
    GPIO.setup(data_pins, GPIO.IN)
    
    #set control pins
    disableWrite()
    enableOutput()
    
    #read data
    setAddressPins(address)
    return readDataPins()

def writeWord(address, data):
    #set data pins to be output
    GPIO.setup(data_pins, GPIO.OUT)
    
    #set address before WE falls
    setAddressPins(address)
    
    #set control pins
    disableOutput()
    enableWrite() #specifically negedge WE after output is disabled
    
    #read data
    setDataPins(data)
    disableWrite()
    
    
if __name__ == "__main__":
    registerPins()
    enableChip()
    setAddressPins(5)
    time.sleep(3)
    cleanUp()
