def break_beam(channel):
    global debug
    if debug:
        if GPIO.input(14):     # if port 14 == 1
            print "Rising edge detected on 14"
        else:                  # if port 14 != 1
            print "Falling edge detected on 14"

def start_indexing():
    global index_enable
    index_enable = True
    print "index enabled", index_enable


def stop_indexing():
    global index_enable
    index_enable = False
    print "index disabled", index_enable

def stopwatch(state):
    pass

def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)

    wrapper.has_run = False
    return wrapper

@run_once
def timer1_en():
    global timer1_dn
    print "timer1 enabled"
    timer1_dn = False
    Clock.schedule_once(timer1,10)

def timer1(dt):
    timer1_dn=True

        #GPIO event callback
def bb_update(self, dt):
    if GPIO.input(14) == True:
        self.ids.bit1.state = 'normal'
        self.ids.bit1.text = 'OFF'
    else:
        self.ids.bit1.state = 'down'
        self.ids.bit1.text = 'ON'