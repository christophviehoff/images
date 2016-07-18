import RPi.GPIO as GPIO

def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT, initial=True)
    GPIO.setup(19, GPIO.OUT, initial=True)

def fwd():
    GPIO.output(18,False)
    GPIO.output(19,True)

def rev():
    GPIO.output(18,True)
    GPIO.output(19,False)

def stop():
    GPIO.output(18,False)
    GPIO.output(19,False)

def reset():
    GPIO.output(18,True)
    GPIO.output(19,True)

def index():
    fwd()
    time.sleep(.5)
    reset()
    print "indexing"

def cleanup():
    GPIO.cleanup()

print "[GPIO %s        ] [Import      ] Importing conveyor module" %GPIO.VERSION
print "[PI VERSION %s      ] [Import      ] Importing conveyor module" %GPIO.RPI_REVISION