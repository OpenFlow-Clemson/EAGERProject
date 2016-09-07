import os
import sys
import atexit

import mininet.util
import mininext.util
mininet.util.isShellBuiltin = mininext.util.isShellBuiltin
sys.modules['mininet.util'] = mininet.util

sys.path.insert(0, os.path.abspath('../..'))
from nodes.floodlight import Floodlight

from mininet.log import setLogLevel, info
from mininet.net import Mininet
from mininext.cli import CLI

from topo import QuaggaTopo

from mininext.net import MiniNExT
from mininet.node import OVSController


def addController():
    # Adding Floodlight Controller
    info('\n*** Adding controller\n')
    net.addController('c1', controller=Floodlight)
    net.addController('c2', controller=Floodlight)


def startNetwork():

    info('\n*** Creating BGP network topology\n')
    topo = QuaggaTopo()

    global net
    net = MiniNExT(topo=topo, build=False)

    addController()
    info('\n*** Starting the network\n')
    net.build()
    # net.start()

    sw1 = net.getNodeByName('sw1')
    sw2 = net.getNodeByName('sw2')
    # sw = net.getNodeByName('sw')

    # Just start sw for communication b/w BGP routers
    # sw.start([])
    sw1.start([])
    sw2.start([])

    h1 = net.getNodeByName('h1')
    h1.setIP('10.0.0.3/24', intf='h1-eth0')
    h2 = net.getNodeByName('h2')
    h2.setIP('20.0.0.3/24', intf='h2-eth0')

    as1 = net.getNodeByName('as1')
    as1.setIP('10.0.0.2/24', intf='as1-eth0')
    as1.setIP('100.0.0.1/24', intf='as1-eth1')

    as2 = net.getNodeByName('as2')
    as2.setIP('20.0.0.2/24', intf='as2-eth0')
    as2.setIP('100.0.0.2/24', intf='as2-eth1')

    info('** Running CLI\n')
    CLI(net)


def stopNetwork():

    if net is not None:
        info('** Tearing down BGP network\n')
        net.stop()


if __name__ == '__main__':

    # Force cleanup on exit by registering a cleanup function
    atexit.register(stopNetwork)

    # Tell mininet to print useful information
    setLogLevel('info')
startNetwork()