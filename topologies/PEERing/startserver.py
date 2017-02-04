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
from mininet.link import Intf

from servertopo import QuaggaTopo

from mininext.net import MiniNExT
from mininet.node import OVSController, RemoteController


# Connects Server Side MiniNExT quagga instance to PEERing peers
def serverConnectPEERing():
    info('** Connecting Server Side Quagga to PEERing testbed ... \n')
    sw2 = net.getNodeByName('sw2')  # Switch Talks to PEERing
    sw1 = net.getNodeByName('sw1')
    quaggaS = net.getNodeByName('quaggaS')
    h1 = net.getNodeByName('h1')

    # sw1.start([])
    sw2.start([])
    os.popen('ovs-vsctl add-port sw2 tap5')
    os.popen('sudo ifconfig tap5 0.0.0.0')
    sw2.setIP('0.0.0.0', intf='sw2-eth1')

    quaggaS.setIP('10.0.0.2', prefixLen=24, intf='quaggaS-eth0')
    quaggaS.setIP('10.0.0.2', prefixLen=24, intf='quaggaS-eth0')  # MiniNExT Bug here
    quaggaS.setIP('100.69.128.3', intf='quaggaS-eth1')
    quaggaS.cmdPrint("ip addr add 184.164.243.1/32 dev lo")
    quaggaS.cmdPrint("route add -net 184.164.243.0 netmask 255.255.255.0 quaggaS-eth0")

    h1.setIP('10.0.0.1', prefixLen=24, intf='h1-eth0')
    h1.cmd('route add default gw 10.0.0.2')


def startNetwork():
    info('\n*** Creating BGP network topology\n')
    topo = QuaggaTopo()

    global net
    net = MiniNExT(topo=topo, build=False)

    info('\n*** Starting the network\n')
    net.addController('c1', controller=RemoteController, port=6653)
    net.build()
    net.start()

    serverConnectPEERing()

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
