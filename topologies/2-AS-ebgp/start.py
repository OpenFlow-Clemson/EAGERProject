import os
import sys

# mininet.util.isShellBuiltin = mininext.util.isShellBuiltin
# sys.modules['mininet.util'] = mininet.util

sys.path.insert(0, os.path.abspath('../..'))
from nodes.floodlight import Floodlight

from mininet.log import setLogLevel, info
from mininext.cli import CLI

from topo import QuaggaTopo

from mininext.net import MiniNExT


# def addController():


# Adding Floodlight Controller
# info('\n*** Adding controller\n')
# net.addController('c1', controller=Floodlight)
# net.addController('c2', controller=Floodlight)


def startNetwork():
    info('\n*** Creating BGP network topology\n')
    topo = QuaggaTopo()

    # global net
    net = MiniNExT(topo=topo, build=False)
    info(net)
    # addController()
    info('\n*** Adding controller\n')
    c1 = net.addController('c1', controller=Floodlight)
    c2 = net.addController('c2', controller=Floodlight)

    info('\n*** Starting the network\n')
    for hostName in net.topo.hosts():
        print net.topo.nodeInfo(hostName)
    net.build()

    sw1 = net.getNodeByName('sw1')
    sw2 = net.getNodeByName('sw2')

    for controller in net.controllers:
        controller.start()

    sw1.start([c1])
    sw2.start([c2])

    h1 = net.getNodeByName('h1')
    h1.setIP('10.0.0.4/24', intf='h1-eth0')
    h1.cmd('route add default gw 10.0.0.2')

    h2 = net.getNodeByName('h2')
    h2.setIP('20.0.0.4/24', intf='h2-eth0')
    h2.cmd('route add default gw 20.0.0.2')

    as1 = net.getNodeByName('as1')
    as1.setIP('10.0.0.2/24', intf='as1-eth0')
    as1.setIP('100.0.0.1/24', intf='as1-eth1')

    as2 = net.getNodeByName('as2')
    as2.setIP('20.0.0.2/24', intf='as2-eth0')
    as2.setIP('100.0.0.2/24', intf='as2-eth1')

    info('** Running CLI\n')
    CLI(net)
    net.stop()

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    startNetwork()
