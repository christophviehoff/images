import RPi.GPIO as GPIO
from kivy.clock import Clock
import time
timer1=True


def break_beam(dt):
    print "break beam"


def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT, initial=True)
    GPIO.setup(19, GPIO.OUT, initial=True)
    GPIO.setup(20, GPIO.OUT, initial=True)
    GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    #GPIO.add_event_detect(14, GPIO.BOTH, callback=break_beam,bouncetime=100)

def red():
    GPIO.output(18,False)
    GPIO.output(19,True)
    GPIO.output(20,True)

def green():
    GPIO.output(18,True)
    GPIO.output(19,False)
    GPIO.output(20,True)

def blue():
    GPIO.output(18,True)
    GPIO.output(19,True)
    GPIO.output(20,False)

def white():
    GPIO.output(18,False)
    GPIO.output(19,False)
    GPIO.output(20,False)

def yellow():
    GPIO.output(18,False)
    GPIO.output(19,False)
    GPIO.output(20,True)

def set(rgb):
    GPIO.output(18,int(rgb[0]))
    GPIO.output(19,int(rgb[1]))
    GPIO.output(20,int(rgb[2]))

def reset():
    GPIO.output(18,True)
    GPIO.output(19,True)
    GPIO.output(20,True)


def flash_red():
    def flash(dt):
        global timer1
        timer1^=True
        if timer1:
            red()
        else:
            reset()
    def flash_reset(dt):
        Clock.unschedule(blink)
        reset()

    blink=Clock.schedule_interval(flash, 0.5)
    Clock.schedule_once(flash_reset, 5)

def betrue():
    RGB=['000','001','010','011','100','101','110','111']
    for color in RGB:
        set(color)
        time.sleep(1)
    #blocking until done

def cleanup():
    GPIO.cleanup()

print "[GPIO %s        ] [Import      ] Importing rgb_module" %GPIO.VERSION
print "[PI VERSION %s      ] [Import      ] Importing rgb_module" %GPIO.RPI_REVISION