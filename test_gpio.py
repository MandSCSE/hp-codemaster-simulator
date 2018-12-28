import RPi.GPIO as GPIO
import threading
import time
import math

# pin11 --- led
BtnPin = 12    # pin12 --- button
BtnPin2 = 13
BtnPin3 = 15
BtnPin4 = 18

class LedCtrl():
    def __init__(self, Led_Pin ):
        self.Led_Pin = Led_Pin
        GPIO.setup(Led_Pin, GPIO.OUT)   # Set LedPin's mode is output
        GPIO.output(self.Led_Pin, True)
    def LedOn(self):
        GPIO.output(self.Led_Pin, False)
    def LedOff(self):
        GPIO.output(self.Led_Pin, True)
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

def setup():
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location

def Btn2(ev=None):
    led.LedOff()
    print("2")

def Btn3(ev=None):
    print("3")

def Btn4(ev=None):
    led.LedOn()
    print("4")

#def loop():

def destroy():
    GPIO.cleanup()                     # Release resource

class BeepCtrl():
    def __init__(self, Pin ):
        self.Pin = Pin
        self.state = False
        GPIO.setup(Pin, GPIO.OUT)   # Set LedPin's mode is output

        GPIO.output(self.Pin, False)
    def beepTone(self, freq, durning):
        """ durning is senconds """
        T = 1 / freq
        end = math.ceil(durning / T)
        for i in range(0, end):
            GPIO.output(self.Pin, True)
            time.sleep(T / 2)
            GPIO.output(self.Pin, False)
            time.sleep(T / 2)
    def beepOn(self):
        self.state = True
        GPIO.output(self.Pin, self.state)
    def beepOff(self):
        self.state = False
        GPIO.output(self.Pin, self.state)
    def __del__(self):
        GPIO.output(self.Pin, False)


if __name__ == '__main__':     # Program start from here

    setup()

    Do=523
    Re=587
    Mi=659
    Fa=698
    So=784
    La=880
    Si=988
    HDo=1047

    BeepPin = 7
    b = BeepCtrl(BeepPin)

    b.beepTone(Do, 0.1)
    time.sleep(1)
    b.beepTone(Re, 0.1)
    time.sleep(1)
    b.beepTone(Mi, 0.1)
    time.sleep(1)
    b.beepTone(Fa, 0.1)
    time.sleep(1)
    b.beepTone(So, 0.1)
    time.sleep(1)
    b.beepTone(La, 0.1)

    led = LedCtrl(11)
    led.LedOn()

    Btn22 = ButtonHandler(BtnPin2, Btn2, edge = 'rising')
    Btn33 = ButtonHandler(BtnPin3, Btn3, edge = 'rising')
    Btn44 = ButtonHandler(BtnPin4, Btn4, edge = 'rising')

    Btn22.start()
    Btn33.start()
    Btn44.start()

    print(GPIO.input(BtnPin3))
    try:
        #loop()
        while True:
            pass
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
