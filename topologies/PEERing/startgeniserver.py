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

from servertopo import QuaggaTopo
from bgp_manager import bgpMgmt

from mininext.net import MiniNExT
from mininet.node import RemoteController

import util


# Server-side Global Parameters for PEERING setup
quagga_node = 'quaggaS'
openvpn_tap_device = "tap5"
openvpn_tap_ip = '100.69.128.6'
ovs_peering_quagga = 'sw2'


# Server-side Global Parameters for end-to-end routing communication
home_ASN = '47065'
peering_prefix = ['184.164.240.0/24', '184.164.241.0/24', '184.164.242.0/24', '184.164.243.0/24']
announce_prefix = peering_prefix[3]
quaggaS_facing_server = '184.164.243.2'
quaggaS_lo = '184.164.243.1/32'
server_ip = '184.164.243.100'
server_gw = quaggaS_facing_server
server_static_route = 'route add -net 184.164.243.0 netmask 255.255.255.0 quaggaS-eth0'
# quaggaS.cmdPrint("route add -net 184.164.240.0 netmask 255.255.255.0 quaggaS-eth0")
# quaggaS.cmdPrint("route add -net 184.164.241.0 netmask 255.255.255.0 quaggaS-eth0")
# quaggaS.cmdPrint("route add -net 184.164.243.0 netmask 255.255.255.0 quaggaS-eth0")



# Connects Server Side MiniNExT quagga instance to PEERing peers
def serverConnectPEERing():
    info('** Connecting Server Side Quagga to PEERing testbed ... \n')

    # Network topology setup
    sw_peering = net.getNodeByName('sw2')
    sw_server = net.getNodeByName('sw1')
    quaggaS = net.getNodeByName('quaggaS')
    server = net.getNodeByName('server')
    sw_peering.start([])


    # Controller setup
    c1 = net.getNodeByName('c1')
    for controller in net.controllers:
        controller.start()
    sw_server.start([c1])


    # PEERING setup
    tunnelip = util.getOpenVPNAddress()
    tapif = util.getTapInterface()

    cmd1 = 'ovs-vsctl add-port ' + ovs_peering_quagga + ' ' + tapif
    os.popen(cmd1)
    cmd2 = 'sudo ifconfig ' + tapif + ' 0.0.0.0'
    os.popen(cmd2)
    sw_peering.setIP('0.0.0.0', intf='sw2-eth1')
    quaggaS.setIP(tunnelip, intf='quaggaS-eth1')


    # End-to-end communication setup
    quaggaS.setIP(quaggaS_facing_server, prefixLen=24, intf='quaggaS-eth0')
    quaggaS.setIP(quaggaS_facing_server, prefixLen=24, intf='quaggaS-eth0')
    cmd3 = "ip addr add " + quaggaS_lo + ' dev lo'
    quaggaS.cmdPrint(cmd3)
    cmd4 = server_static_route
    quaggaS.cmdPrint(cmd4)
    server.setIP(server_ip, prefixLen=24, intf='server-eth0')
    cmd5 = 'route add default gw ' + server_gw
    server.cmd(cmd5)


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
    net.addController('c1', controller=Floodlight)
    # net.addController('c1', controller=RemoteController, port=6653)

    net.build()
    # net.start()

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