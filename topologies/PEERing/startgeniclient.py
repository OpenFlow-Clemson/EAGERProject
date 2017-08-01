import atexit
import os
import sys

import mininet.util
import mininext.util

mininet.util.isShellBuiltin = mininext.util.isShellBuiltin
sys.modules['mininet.util'] = mininet.util

sys.path.insert(0, os.path.abspath('../..'))
from nodes.floodlight import Floodlight

from mininet.log import setLogLevel, info
from mininext.cli import CLI

from clienttopo import QuaggaTopo
from bgp_manager import bgpMgmt

from mininext.net import MiniNExT
from mininet.node import RemoteController

import util

# Client-side global parameters for PEERING setup
quagga_node = 'quaggaC'
openvpn_tap_device = "tap1"
openvpn_tap_ip = '100.65.128.5'
ovs_peering_quagga = 'sw3'

# Client-side routing parameters for end-to-end communication
home_ASN = '47065'
peering_prefix = ['184.164.240.0/24', '184.164.241.0/24', '184.164.242.0/24', '184.164.243.0/24']
announce_prefix = peering_prefix[2]
quaggaC_facing_client = '184.164.242.2'
quaggaC_lo = '184.164.242.1/32'
client_ip = '184.164.242.100'
client_gw = quaggaC_facing_client


# Connects Client Side MiniNExT quagga instance to PEERing peers
def clientConnectPEERing():
    info('** Connecting Client Side Quagga to PEERing testbed ... \n')

    # Network topology setup
    sw_peering = net.getNodeByName('sw3')
    sw_client = net.getNodeByName('sw4')
    quaggaC = net.getNodeByName('quaggaC')
    client = net.getNodeByName('client')
    sw_peering.start([])


    # Controller setup
    c2 = net.getNodeByName('c2')
    for controller in net.controllers:
        controller.start()
    sw_client.start([c2])


    # PEERING setup
    tunnelip = util.getOpenVPNAddress()
    tapif = util.getTapInterface()

    cmd1 = 'ovs-vsctl add-port ' + ovs_peering_quagga + ' ' + tapif
    os.popen(cmd1)
    cmd2 = 'sudo ifconfig ' + tapif + ' 0.0.0.0'
    os.popen(cmd2)
    sw_peering.setIP('0.0.0.0', intf='sw3-eth1')
    quaggaC.setIP(tunnelip, intf='quaggaC-eth1')

    # End-to-end communication setup
    quaggaC.setIP(quaggaC_facing_client, prefixLen=24, intf='quaggaC-eth0')
    quaggaC.setIP(quaggaC_facing_client, prefixLen=24, intf='quaggaC-eth0')
    cmd3 = "ip addr add " + quaggaC_lo + ' dev lo'
    quaggaC.cmdPrint(cmd3)
    client.setIP(client_ip, prefixLen=24, intf='client-eth0')
    cmd4 = 'route add default gw ' + client_gw
    client.cmd(cmd4)


    info('** Announcing BGP prefix.. \n')
    bgpManager = bgpMgmt()
    bgpManager.prefix_announce(quagga_node, home_ASN, announce_prefix)


def startNetwork():
    info('\n*** Creating BGP network topology\n')
    topo = QuaggaTopo()

    global net
    net = MiniNExT(topo=topo, build=False)

    info('\n*** Starting the network\n')
    info('\n*** Adding controller\n')
    net.addController('c2', controller=Floodlight)
    # net.addController('c2', controller=RemoteController, port=6653)
    net.build()
    # net.start()

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