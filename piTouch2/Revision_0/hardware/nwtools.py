#!/usr/bin/env python
# Python Network Programming Cookbook -- Chapter -1
# This program is optimized for Python 2.7. It may run on any
# other Python version with/without modifications.

import socket

def print_machine_info():
    host_name = socket.gethostname()
    ip_address = socket.gethostbyname(host_name)
    #print "Host name: %s" % host_name
    #print "IP address: %s" % ip_address
    return (host_name,ip_address)

def get_remote_machine_info(remote_host):
    try:
        #print "IP address: %s" %socket.gethostbyname(remote_host)
        return socket.gethostbyname(remote_host)
    except socket.error, err_msg:
        #print "%s: %s" %(remote_host, err_msg)
        return (None)

def find_service_name():
    protocolname = 'tcp'
    for port in [80, 25]:
        print "Port: %s => service name: %s" %(port, socket.getservbyport(port, protocolname))
    print "Port: %s => service name: %s" %(53, socket.getservbyport(53, 'tcp'))

def test_socket_timeout():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "Default socket timeout: %s" %s.gettimeout()
    s.settimeout(100)
    print "Current socket timeout: %s" %s.gettimeout()

if __name__ == '__main__':
    print print_machine_info()
    print get_remote_machine_info('www.nike.com')
    find_service_name()