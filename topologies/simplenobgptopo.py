import os
import sys

import mininet.log as log
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.topo import Topo

sys.path.insert(0, os.path.abspath('..'))
import nodes

class SimpleNoBGPTopo(Topo):
    def __init__(self):
        Topo.__init__(self)
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        self.addLink(h1, s1)
        self.addLink(s1, s2)
        self.addLink(s2, h2)


if __name__ == '__main__':
    log.setLogLevel('info')
    net = Mininet(topo=SimpleNoBGPTopo(), build=False)
    c1 = net.addController(name='c1', controller=nodes.Floodlight)
    c2 = net.addController(name='c2', controller=nodes.Floodlight)
    net.build()
    net.getNodeByName('s1').start([c1])
    net.getNodeByName('s2').start([c2])
    for controller in net.controllers:
        controller.start()
    CLI(net)
