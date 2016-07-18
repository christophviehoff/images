import time
import RPi.GPIO as GPIO
from hardware import conveyor

state = 0
index_enable = False
timer2 = True
timer1_dn=False

# dt means delta-time
def my_timer2(dt):
    global timer2
    timer2 ^= True
    if timer2:
        print "tick"
    else:
        print "tock"

def index_conveyor():
    global index_enable,timer1_dn
    skip = True
    cnt = 0
    global state

    # tiny circular 3 state machine updated by clock interval within kivy loop
    # thread alive
    while True:
        # update transition state
        transition01 = not GPIO.input(14)
        transition12 = skip #timer1_dn
        transition23 = skip

        # action planning based on state
        if state == 0:# conveyor run
            conveyor.fwd()
            if transition01:  # break beam sensor watch
                state = 1
        elif state == 1:#conevyro stop and wait
            conveyor.reset()
            time.sleep(3)  # wait timer
            #timer1_en()
            # call my_callback in 5 seconds
            if transition12:
                state = 2
        elif state == 2:  # conveyor run
            conveyor.fwd()
            # time.sleep(0.1) #only when sensor is still seen at stop
            if transition23: #restart cycle
                state = 0
                cnt += 1

        # cycle timer from state 0 to state 2
        if state == 0:
            startTime = time.time()
        if state == 2:
            endTime = time.time()
            print 'Tact time is {:.2f} seconds. Cycle: {}'.format((endTime - startTime), cnt)
