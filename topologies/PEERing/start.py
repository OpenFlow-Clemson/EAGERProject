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

from topo import QuaggaTopo
from bgp_manager import bgpMgmt

from mininext.net import MiniNExT
from mininet.node import OVSController, RemoteController


peering_prefix = ['184.164.240.0/24', '184.164.241.0/24', '184.164.242.0/24', '184.164.243.0/24']
home_ASN = '47065'
quagga_node_S = 'quaggaS'
quagga_node_C = 'quaggaC'


def addController():
    # Adding Floodlight Controller
    info('\n*** Adding controller\n')
    net.addController('c1', controller=Floodlight)


# Connects Server Side MiniNExT Quagga instance to PEERing peers
def serverConnectPEERing():
    info('** Connecting Server Side Quagga to PEERing testbed ... \n')
    sw2 = net.getNodeByName('sw2')        # Switch Talks to PEERing
    quaggaS = net.getNodeByName('quaggaS')
    h1 = net.getNodeByName('h1')

    sw2.start([])

    os.popen('ovs-vsctl add-port sw2 tap5')
    os.popen('sudo ifconfig tap5 0.0.0.0')
    sw2.setIP('0.0.0.0', intf='sw2-eth1')

    quaggaS.setIP('10.0.0.2', prefixLen=24, intf='quaggaS-eth0')
    quaggaS.setIP('10.0.0.2', prefixLen=24, intf='quaggaS-eth0')  # setIP twice b/c MiniNExT Bug here
    quaggaS.setIP('100.69.128.7', intf='quaggaS-eth1')
    quaggaS.cmdPrint("ip addr add 184.164.243.1/32 dev lo")
    quaggaS.cmdPrint("route add -net 184.164.243.0 netmask 255.255.255.0 quaggaS-eth0")

    h1.setIP('10.0.0.1', prefixLen=24, intf='h1-eth0')
    h1.cmd('route add default gw 10.0.0.2')

    info('** Server Side Quagga Announcing BGP prefix.. \n')
    bgpManager = bgpMgmt()
    bgpManager.prefix_announce(quagga_node_S, home_ASN, peering_prefix[3])


# Connects Client Side MiniNExT Quagga instance to PEERing peers
def clientConnectPEERing():
    info('** Connecting Client Side Quagga to PEERing testbed ... \n')
    sw3 = net.getNodeByName('sw3')        # Switch Talks to PEERing
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

    h2.setIP('184.164.242.100',prefixLen=24, intf='h2-eth0')
    h2.cmd('route add default gw 184.164.242.2')

    info('** Client Side Quagga Announcing BGP prefix.. \n')
    bgpManager = bgpMgmt()
    bgpManager.prefix_announce(quagga_node_C, home_ASN, peering_prefix[2])


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


