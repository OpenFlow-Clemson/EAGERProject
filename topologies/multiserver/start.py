import os
import sys
import atexit
import time

import mininet.util
import mininext.util
mininet.util.isShellBuiltin = mininext.util.isShellBuiltin
sys.modules['mininet.util'] = mininet.util

sys.path.insert(0, os.path.abspath('../..'))
from nodes.floodlight import Floodlight
from nodes.bgp_router_cntl import BGPRTCntl
from nodes.restutils import EAGERRest

from mininet.log import setLogLevel, info
from mininet.net import Mininet
from mininext.cli import CLI

from topo import QuaggaTopo

from mininext.net import MiniNExT
from mininet.node import OVSController


def startNetwork():
    info('\n*** Creating BGP network topology\n')
    topo = QuaggaTopo()

    net = MiniNExT(topo=topo, build=False)
    info(net)

    info('\n*** Adding controller\n')
    c1 = net.addController('c1', controller=Floodlight)
    c2 = net.addController('c2', controller=Floodlight)
    c3 = net.addController('c3', controller=Floodlight)

    info('\n*** Starting the network\n')
    net.build()

    sw1 = net.getNodeByName('sw1')
    sw2 = net.getNodeByName('sw2')
    sw3 = net.getNodeByName('sw3')
    sw4 = net.getNodeByName('sw4')

    for controller in net.controllers:
        controller.start()

    sw1.start([c1])
    sw2.start([c2])
    sw3.start([c3])
    sw4.start([])

    h1 = net.getNodeByName('h1')
    h1.setIP('10.0.0.4/24', intf='h1-eth0')
    h1.cmd('route add default gw 10.0.0.2')

    h2 = net.getNodeByName('h2')
    h2.setIP('20.0.0.4/24', intf='h2-eth0')
    h2.cmd('route add default gw 20.0.0.2')

    h3 = net.getNodeByName('h3')
    h3.setIP('30.0.0.4/24', intf='h3-eth0')
    h3.cmd('route add default gw 30.0.0.2')

    as1 = net.getNodeByName('as1')
    as1.setIP('10.0.0.2/24', intf='as1-eth0')
    as1.setIP('100.0.0.1/24', intf='as1-eth1')

    as2 = net.getNodeByName('as2')
    as2.setIP('20.0.0.2/24', intf='as2-eth0')
    as2.setIP('100.0.0.2/24', intf='as2-eth1')

    as3 = net.getNodeByName('as3')
    as3.setIP('30.0.0.2/24', intf='as3-eth0')
    as3.setIP('100.0.0.3/24', intf='as3-eth1')

    as1.setARP(h1.IP(), h1.MAC())
    as2.setARP(h2.IP(), h2.MAC())
    as3.setARP(h3.IP(), h3.MAC())

    info('*** Advertising new prefixes..\n')
    bgpController = BGPRTCntl()

    bgpController.inject_one_prefix('as2', 200, '40.0.0.0/24')
    bgpController.inject_one_prefix('as2', 200, '50.0.0.0/24')
    bgpController.show_bgp_all_prefix('as2')
    as2.cmd('route add default gw 20.0.0.4')

    bgpController.inject_one_prefix('as3', 300, '60.0.0.0/24')
    bgpController.inject_one_prefix('as3', 300, '70.0.0.0/24')
    bgpController.show_bgp_all_prefix('as3')
    as3.cmd('route add default gw 30.0.0.4')

    info('*** Configuring controllers..\n')
    #time.sleep(3)

    #info(str(c1.http_port) + ' http_port\n')
    #c1Rest = EAGERRest(c1.ip, c1.http_port)
    #c1Rest.enableRandomizer()
    #c1Rest.disableRandomizer()

    # c1.addServer('20.0.0.4')
    # c1.addServer('30.0.0.4')
    # c2.addServer('20.0.0.4')
    # c3.addServer('30.0.0.4')
    #
    # c1.addPrefix('40.0.0.0', '255.255.255.0', '20.0.0.4')
    # c1.addPrefix('50.0.0.0', '255.255.255.0', '20.0.0.4')
    # c1.addPrefix('60.0.0.0', '255.255.255.0', '30.0.0.4')
    # c1.addPrefix('70.0.0.0', '255.255.255.0', '30.0.0.4')
    # c2.addPrefix('40.0.0.0', '255.255.255.0', '20.0.0.4')
    # c2.addPrefix('50.0.0.0', '255.255.255.0', '20.0.0.4')
    # c3.addPrefix('60.0.0.0', '255.255.255.0', '30.0.0.4')
    # c3.addPrefix('70.0.0.0', '255.255.255.0', '30.0.0.4')
    #

    # c1.setRandomizeTo(False)
    # c2.setRandomizeTo(True)
    # c3.setRandomizeTo(True)
    #
    # c1.enableRandomizer()
    # c2.enableRandomizer()
    # c3.enableRandomizer()

    info('** Running CLI\n')
    CLI(net)
    net.stop()

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    startNetwork()
