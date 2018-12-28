import RPi.GPIO as GPIO
import threading
import time

def PiDriverSetup():
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    
def PiDriverDestroy():
    GPIO.cleanup()                     # Release resource

# state 'True' is light out
class LedCtrl():
    def __init__(self, Led_Pin ):
        self.Led_Pin = Led_Pin
        self.state = True
        
        GPIO.setup(Led_Pin, GPIO.OUT)   # Set LedPin's mode is output
        GPIO.output(self.Led_Pin, True)
    def getState(self):
        return self.state
    def LedOn(self):
        self.state = False
        GPIO.output(self.Led_Pin, self.state) 
    def LedOff(self):
        self.state = True
        GPIO.output(self.Led_Pin, self.state)
    def LedSwitch(self):
        if(self.state == True):
            self.state = False
        else:
            self.state = True
        GPIO.output(self.Led_Pin, self.state)
    def __del__(self):
        GPIO.output(self.Led_Pin, True)

class ButtonHandler(threading.Thread):
    def __init__(self, pin, func, edge='both', bouncetime=50):
        super().__init__(daemon=True)

        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

        self.edge = edge
        self.func = func
        self.pin = pin
        self.bouncetime = float(bouncetime)/1000

        self.lastpinval = GPIO.input(self.pin)

        self.t = threading.Timer(self.bouncetime, self.read)
        self.t.start()

    def read(self):
        pinval = GPIO.input(self.pin)

        if (
                ((pinval == 0 and self.lastpinval == 1) and
                 (self.edge in ['falling', 'both'])) or
                ((pinval == 1 and self.lastpinval == 0) and
                 (self.edge in ['rising', 'both']))
        ):
            self.func()

        self.lastpinval = pinval
        
        self.t = threading.Timer(self.bouncetime, self.read)
        self.t.start()
