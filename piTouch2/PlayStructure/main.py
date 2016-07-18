# File name: layouts.py
import kivy
kivy.require('1.9.0')
import socket

#install_twisted_rector must be called before importing the reactor
from kivy.support import install_twisted_reactor
install_twisted_reactor()

#install kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.clock import Clock


#color constants
RED=(1,0,0,1)
GREEN=(0,1,0,1)


#Global variables
watchdog=True
debug=True
state=0

#import external modules
import time
import threading
from hardware import conveyor,utils
import RPi.GPIO as GPIO

#A simple Client that send messages to the echo server
from twisted.internet import reactor, protocol

class EchoClient(protocol.Protocol):
    def connectionMade(self):
        self.factory.app.on_connection(self.transport)

    #core receive here
    def dataReceived(self, data):
        self.factory.app.print_message(data)

class EchoFactory(protocol.ClientFactory):
    protocol = EchoClient

    def __init__(self, app):
        self.app = app

    def clientConnectionLost(self, conn, reason):
        self.app.print_header ("---connection lost")
        self.app.header.color=(1,0,0,1)

    def clientConnectionFailed(self, conn, reason):
        self.app.print_header ("---connection failed")
        self.app.header.color=(1,0,0,1)

class MyGridLayout(GridLayout):

    connection = None

    message = ObjectProperty(None)
    textbox = ObjectProperty(None)
    header  = ObjectProperty(None)

    #kivy-twisted setup
    def connect_to_server(self):
        #using self.ids.... this time instead of object property
        self.nickname = self.ids.title.text
        reactor.connectTCP('localhost', 8090, EchoFactory(self))
        host_name = socket.gethostname()
        ip_address = socket.gethostbyname(host_name)
        self.ids.hostname.text=host_name+':'+ip_address

    def disconnect(self):
        self.print_header ('---disconnecting')
        self.header.color=(1,0,0,1)
        if self.connection:
            self.connection.loseConnection()
            del self.connection

    def connection_state(self):
        if self.ids.switch.active:
            self.connect_to_server()
        else:
            self.disconnect()

    def on_connection(self, connection):
        self.print_header (self.nickname +" connected successfully!")
        self.header.color=(0,1,0,1)
        self.connection = connection

    #kivy-twisted core send stuff here
    def send_message(self, *args):
        msg = self.textbox.text
        if msg and self.connection:
            self.connection.write("%s : %s" % (self.nickname,self.textbox.text))
            self.textbox.text = ""

    def print_message(self, msg):
        self.message.text = msg

    def print_header(self, msg):
        self.header.text = msg

    #kivy update scheduled events

    #display input on Pin14 (break beam sensor)runs every 1/10sec
    def io_update(self, dt):
        #little indicator bar top right
        self.ids.bit1.rgb=GREEN

        if GPIO.input(14) == True:
            self.ids.bit1.state = 'normal'
            self.ids.bit1.text = 'OFF'

        else:
            self.ids.bit1.state = 'down'
            self.ids.bit1.text = 'ON'
    #runs every .5s to show user interface is active
    def i_am_alive(self,dt):
        global watchdog
        watchdog^=True
        if watchdog:
            self.ids.led1.rgb=GREEN
        else:
            self.ids.led1.rgb=RED

    #logic that runs as a thread inside Kivy

    def start_conveyor_thread(self):
        t=threading.Thread(name="Indexing Conveyor thread",target= self.index_conveyor)
        t.setDaemon(True)
        t.start()
    def index_conveyor(self):
        global state
        skip=True
        cnt = 0

        print threading.currentThread().getName(), '...started!'
        # tiny circular 3 state machine
        while True:
            transition01= not GPIO.input(14)
            transition12= skip
            transition23= skip

            if state == 0:
                conveyor.fwd()
                if transition01:
                    state=1
            elif state == 1:   #wait for job don
                conveyor.reset()
                time.sleep(5)
                if transition12:
                    state=2
            elif state == 2:   #fwd of sensor
                #self.ids.bit7.state="normal" when not timed
                conveyor.fwd()
                #time.sleep(.1)
                if transition23:
                    state=0
                    cnt += 1

             # cycle timer from state 0 to state 2
            if state == 0:
                startTime = time.time()
            if state == 2:
                endTime = time.time()
                #print 'Tact time is {:.2f} seconds. Cycle: {}'.format((endTime - startTime), cnt)
                #format for Kivy Label hwre
                self.ids.bit7.text='{:.4f} s'.format((endTime - startTime))
                self.ids.bit8.text='{:.0f} cycles'.format(cnt)
                #little indicator bar top right
                self.ids.bit7.rgb=GREEN
                self.ids.bit8.rgb=GREEN

    #kivy touchscreen event callbacks
    def cb_msg_bit1(self):
        self.print_message ('bit 1 event callback')
    def cb_msg_bit2(self):
        self.print_message ('bit 2 event callback')
        conveyor.fwd()
    def cb_msg_bit3(self):
        self.print_message ('bit 3 event callback')
        conveyor.rev()
    def cb_msg_bit4(self):
        self.print_message ('bit 4 event callback')
        conveyor.stop()
    def cb_msg_bit5(self):
        self.print_message  ('bit 5 event callback')
        conveyor.reset()
    def cb_msg_bit6(self):
        self.print_message  ('bit 6 event callback')
        self.start_conveyor_thread()
    def cb_msg_bit7(self,*args):
        self.message.text = 'bit 7 event callback'
    def cb_msg_bit8(self):
        self.message.text = 'bit 8 event callback'
    def cb_msg_bit9(self):
        self.message.text = 'bit 9 event callback'
    def cb_msg_bit10(self):
        self.message.text = 'bit 10 event callback'
    def cb_msg_bit11(self):
        self.message.text = 'bit 11 event callback'
    def cb_msg_bit12(self):
        self.message.text = 'bit 12 event callback'
    def cb_msg_bit13(self):
        self.message.text = 'bit 13 event callback'
    def cb_msg_bit14(self):
        self.message.text = 'bit 14 event callback'
    def cb_msg_bit15(self):
        self.message.text = 'bit 15 event callback'
    def cb_msg_bit16(self):
        self.message.text = 'bit 16 event callback'

class MainApp(App):
    def build(self):
        interface=MyGridLayout()
        #create all scheduled events
        Clock.schedule_interval(interface.io_update, 0)#every frame
        Clock.schedule_interval(interface.i_am_alive, .5)

        # uncomment to have index conveyor as part of Kivy  loop
        # Clock.schedule_interval(interface.index_conveyor, 1.0/60.0)
        # Regiter GPIO event
        # GPIO.add_event_detect(14, GPIO.FALLING, callback=interface.bb_update,bouncetime=200)

        return interface

if __name__=="__main__":

    try:
        conveyor.init()
        MainApp().run() #in kivy event loop now!!!

    except KeyboardInterrupt:
       # Handle the Ctrl-C exception to keep its error message from displaying.
       print('\nProcess terminated.')