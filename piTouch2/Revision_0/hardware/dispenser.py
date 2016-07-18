''' API Communication Packet Specification
  Command Packet Specification
  Response Packet Specification
  Reserved Response Codes

- Card Dispenser API Command Codes Quick Guide

______________________________________________________
API Communication Packet Specification
______________________________________________________

Command Packet Specification
The command packet, normally transmitted from host controller such as
PC, embedded controller to CTD-202/CTD-203 card dispenser controller is
the beginning of a communication session. It is used for transmitting
the data/requests to other controller via RS-232 or USB to initiates a
command of action (such as disable or enable, requests, etc.).

The packet breakdown is as follows:

<STX><ADD><CMD><LEN><DTA><ETX><CHK>

Name	Hex	Definition
STX	02h	Start of Text Data
ADD	00h+	Device Address (Set to 0x01 if not used)
CMD	80h+	Command Code Byte (0x80-0xFF)
LEN	00h+	Length of Data Byte Size (0x00 or higher)
DTA	--h	Packet Data (Optional, leave empty if not used)
ETX	03h	End of Text Data
CHK	--h	XOR Checksum of data packet

Minimum Packet Length : 6 bytes
Maximum Packet Length : 36 bytes


Response Packet Specification
______________________________________________________

The response packet, normally transmitted from other controllers
to card dispenser controller in response to a command packet, is
the second (and usually final) stage of a communication session.
It is used to transfer the requested data back to card dispenser
controller and give a response code.

Name	Hex	                Definition
STX	02h              	Start of Text Data
ADD	00h+               	Device Address (Set to 0x01 if not used)
CMD	06h, 15h, FD-FFh	Reserved Response Code Byte (see below for
details)
LEN	00h+	            Length of Data  Byte Size (0x00 or higher)
DTA	--h	                Packet Data (Optional, leave empty if not used)
ETX	03h	                End of Text Data
CHK	--h	                XOR Checksum of data packet

Minimum Packet Length : 5 bytes
Maximum Packet Length : 36 bytes

NOTE for CHK (XOR Checksum):
You can calculate the XOR checksum by using Windows calculator with
scientific view, and select HEX radio button to add
STX+ADD+CMD+LEN+DATA+ETX
together using XOR button to get the XOR hex value.



Reserved Response Codes
______________________________________________________

A slave/host device, in responding to a request from the master/host
device, includes a response byte in its response packet. This byte can
be used to replay the success or failure of a particular commands
execution or communication error. Most of the response codes are
defined in the devices API specification, but a few response codes
are reserved as following:

Name	Reserved ResponseCodes	Definition
ACK	06h	                                Accepted/Positive Status
NAK	15h	                                Rejected/Negative Status
	FDh	                                Incomplete Command Packet
	FEh	                                Unrecognized Command Packet
	FFh	                                Data Packet Checksum Error


It is imperative that all master/host devices that adhere to this
specification handle these response codes.


Card Dispenser API Command Codes Quick Guide
______________________________________________________

Command codes will be in the range of 0x80 - 0xFF hex value.
Host controller communicating to card dispenser controller must
handle the following reserved and standard commands:

Reserved
Command
Codes	Definition
FFh	Disable Card Dispenser
FEh	Enable Card Dispenser (Default at start-up)
F0h	Reserved for Factory use only

Command
Codes	Definition	                                       Type of Variable (in Data Packet)
80h	Dispense Card                                 1 byte unsigned CHAR (Resp)
81h	Request Status	                        1 byte unsigned CHAR (Resp)
82h	Read Total Dispense Count Meter  2 bytes unsigned INT (Resp)
83h	Read Total Dispense Button Count Meter  2 bytes unsigned INT (Resp)
84h	Write Total Number of Retries	        1 byte unsigned CHAR
85h	Read Total Number of Retries	        1 byte unsigned CHAR (Resp)
86h	Reset the card dispenser	        None or 1 byte unsigned CHAR
87h	Write Card Hold set	                        1 byte unsigned CHAR
88h	Read Card Hold set	                        1 byte unsigned CHAR
89h	Write "Delay Time" in secs              1 byte unsigned CHAR
8Ah	Read "Delay Time" in secs              1 byte unsigned CHAR
A0h	Multi-Dispense with # cards             1 byte unsigned CHAR
A1h	Partial Dispense                                NONE

Note: (Resp) = data is available in Response Packet. Command Packet
contains no data.

Please see VENDAPIN Card Dispenser API Communication Documentation
for additional details on Command Codes list as described above.

'''

#list of available ports :
# python -m serial.tools.list_ports
# python -c "import serial.tools.list_ports;print serial.tools.list_ports.comports()"

import serial
from serial.tools import list_ports  #needs version 3.0 and up

# look-up tables for commands and responses, dictionaries unsorted key:value pair

command={
'dispense' :                  "020180000380",
'request_status':             "020181000381",
'read_dispense_total':        "020182000382",    # number : 02 01 06 02 00 18 03 04
'read_dispense_button_total': "020183000383",    # number : 02 01 06 02 00 18 03 1C
'write_total_retries':        "02018401030386",  # number 3
'read_total_retries':         "020185000385",
'reset_card_dispenser':       "02018601000387",  # checkbox off
'hard_reset_card_dispenser':  "02018601010386",  # checkbox on
'write_hold_card':            "02018701010387",
'read_hold_card':             "020188000388",
'write_delay_time':           "0201890102038A",  # number 2
'read_delay_time':            "02018A00038A",    # number 2 :02 01 06 02 02 00 03 06
'write_address':              "02019001010390",  # number 1
'multi_dispense':             "0201A0010203A3",  # number 2
'partial_dispense':           "0201A10003A1"
}

status_response={
'02011501310325':'busy',
'02011501320326':'empty',
'02010601300337':'ready',
'02010601340333':'card_hold',
'02011501380320':'partial_dispense',
'02011501340320':'partial dispense'
}

def list_of_serial_ports():
    #list available com ports
    open_ports=[]
    #select only the dispenser via the VID
    for port in list_ports.grep('0403:6001'):
    #USB ports only shows up when connected
        open_ports.append(port.device)

    return(open_ports)

def connect_to_serial_port(open_ports):
    try:# port configuration
        ser = serial.Serial(
            #port='/dev/ttyUSB0',
            port=open_ports[0],
            baudrate=19200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
    except (serial.SerialException,IndexError) :
        print "No Active serial ports found:"
    else: #found an open port
        if ser.is_open:
            print "Active serial port: " + ser.name

        ser.flushInput() #flush input buffer, discarding all its contents
        ser.flushOutput()#flush output buffer, aborting current output
                 #and discard all that is in buffer
        return(ser)

def get_status(ser):
    if ser.is_open:
        #print "Active serial port: " + ser.name
        #status request response cycle example
        #send command i:
        ser.write(command['request_status'].decode('hex'))
        print "Sent Packets: "+ command['request_status']

        #read response
        response_received= ser.readline(7).encode("hex")
        print "Received Packets: " + response_received

        #check if response is valid status response
        if response_received in status_response:
            return (status_response[response_received])
        else:
            return("not a valid status response")

        ser.close()

    else:
        return (None)

    #return(status_response[response_received])


if __name__=="__main__":
    #list all open ports
    print list_of_serial_ports()
    connect_to_serial_port(list_of_serial_ports())
    #returns the serial port object
    print connect_to_serial_port(list_of_serial_ports())
    #retruns verbose status of dispenser
    response=get_status(connect_to_serial_port(list_of_serial_ports()))
    print response