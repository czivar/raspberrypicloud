#!/usr/bin/python
import socket, time

SERVER = 'pimaster'
SERVER_PORT = 43278
BEAT_PERIOD = 5

while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
     s.connect((SERVER, SERVER_PORT))
     #s.sendto(s.getsockname()[0], (SERVER, SERVER_PORT))
     s.sendto('hello', (SERVER, SERVER_PORT))
     s.close()
    except:
     if __debug__: print 'Where are you, server?'
    if __debug__: print 'Time: %s' % time.ctime()
    time.sleep(BEAT_PERIOD)
