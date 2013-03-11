#!/usr/bin/env python
import os, sys

PATH_APP='/home/richardson/public_html/management/'

if PATH_APP not in sys.path:
    sys.path.append(PATH_APP)

os.environ["DJANGO_SETTINGS_MODULE"] = "www.settings"

import time
from twisted.application import internet, service
from twisted.internet import protocol
from twisted.python import log
from cluster.models import *

UDP_PORT = 43278; CHECK_PERIOD = 10; CHECK_TIMEOUT = 15

class Receiver(protocol.DatagramProtocol):
    """Receive UDP packets and log them in the clients dictionary"""

    def datagramReceived(self, data, (ip, port)):
        if data == 'hello' :
            self.callback(ip)

class DetectorService(internet.TimerService):
    """Detect clients not sending heartbeats for too long"""

    def __init__(self):
        internet.TimerService.__init__(self, CHECK_PERIOD, self.detect)
        self.beats = {}
        for node in Node.objects.filter(state = 1):
         node.state = 2
         node.save()

    def update(self, ip):
        node = Node.objects.get(ip = ip)
        node.state = 1
        if node.ip not in self.beats:
         log.msg('node %s is registered' % node.name)
        node.save()
        for vm in VM.objects.filter(node = node):
          if vm.state == 5:
           vm.state = 1
           vm.save()
           log.msg('vm on node %s is online after crashing' % node.name )
        self.beats[ip] = time.time()

    def detect(self):
        """Log a list of clients with heartbeat older than CHECK_TIMEOUT"""
        limit = time.time() - CHECK_TIMEOUT
        silent = [ip for (ip, ipTime) in self.beats.items() if ipTime < limit]
        for (ip, ipTime) in self.beats.items():
         if ipTime < limit:
          node = Node.objects.get(ip = ip)
          node.state = 0
          node.save()
          del self.beats[ip]
          log.msg('node %s is unregistered' % node.name )
          for vm in VM.objects.filter(node = node):
           vm.state = 5
           vm.save()
           log.msg('vm on node %s is crashed' % node.name )
           # itt elvagtak az ereit... :( 

application = service.Application('Heartbeat')
# define and link the silent clients' detector service
detectorSvc = DetectorService()
detectorSvc.setServiceParent(application)
# create an instance of the Receiver protocol, and give it the callback
receiver = Receiver()
receiver.callback = detectorSvc.update
# define and link the UDP server service, passing the receiver in
udpServer = internet.UDPServer(UDP_PORT, receiver)
udpServer.setServiceParent(application)
# each service is started automatically by Twisted at launch time
log.msg('Asynchronous heartbeat server listening on port %d\n'
    'press Ctrl-C to stop\n' % UDP_PORT)
