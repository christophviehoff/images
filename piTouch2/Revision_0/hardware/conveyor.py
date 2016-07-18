import RPi.GPIO as GPIO

debug=True


def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(19, GPIO.OUT, initial=True)
    GPIO.setup(20, GPIO.OUT, initial=True)
    GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def fwd():
    GPIO.output(20,False)
    GPIO.output(19,True)

def rev():
    GPIO.output(20,True)
    GPIO.output(19,False)

def stop():
    GPIO.output(19,False)
    GPIO.output(20,False)

def reset():
    GPIO.output(19,True)
    GPIO.output(20,True)

def index():
    pass

def cleanup():
    GPIO.cleanup()

print "[GPIO %s        ] [Import      ] Importing conveyor module" %GPIO.VERSION
print "[PI VERSION %s      ] [Import      ] Importing conveyor module" %GPIO.RPI_REVISION