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

from clienttopo import QuaggaTopo

from mininext.net import MiniNExT
from mininet.node import OVSController, RemoteController


# Connects Client Side MiniNExT quagga instance to PEERing peers
def clientConnectPEERing():
    info('** Connecting Client Side Quagga to PEERing testbed ... \n')
    sw3 = net.getNodeByName('sw3')  # Switch Talks to PEERing
    sw4 = net.getNodeByName('sw4')
    quaggaC = net.getNodeByName('quaggaC')
    h2 = net.getNodeByName('h2')

    sw3.start([])

    os.popen('ovs-vsctl add-port sw3 tap1')
    os.popen('sudo ifconfig tap1 0.0.0.0')
    sw3.setIP('0.0.0.0', intf='sw3-eth1')

    quaggaC.setIP('184.164.242.2', prefixLen=24, intf='quaggaC-eth0')
    quaggaC.setIP('184.164.242.2', prefixLen=24, intf='quaggaC-eth0')
    quaggaC.setIP('100.65.128.5', intf='quaggaC-eth1')
    quaggaC.cmdPrint("ip addr add 184.164.242.1/32 dev lo")

    h2.setIP('184.164.242.100', prefixLen=24, intf='h2-eth0')
    h2.cmd('route add default gw 184.164.242.2')


def startNetwork():
    info('\n*** Creating BGP network topology\n')
    topo = QuaggaTopo()

    global net
    net = MiniNExT(topo=topo, build=False)

    info('\n*** Starting the network\n')
    net.addController('c1', controller=RemoteController, port=6653)
    net.build()
    net.start()

    clientConnectPEERing()

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
