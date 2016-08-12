import os
import sys

from mininext.cli import CLI

sys.path.insert(0, os.path.abspath('..'))
from mininext.topo import Topo as BaseTopo
from nodes import Floodlight
from net import MiniNExTXL
import mininet.log as log


class Topo(BaseTopo):
    """Extended topology to support BGP and session maintenance topologies
    for the EAGER project at Clemson University"""

    # TODO Consider adding bopts (BGP options) or something similar if useful
    def __init__(self, **opts):
        BaseTopo.__init__(self, **opts)

    def addController(self, name, **opts):
        return self.addNode(name, isController=True, **opts)

    def isController(self, n):
        '''Returns true if node is a controller.'''
        info = self.node_info[n]
        return info and info.get('isController', False)

    def controllers(self, sort=True):
        '''Return controllers.'''
        return [n for n in self.nodes(sort) if self.isController(n)]

    def hosts(self, sort=True):
        '''Return hosts.'''
        return [n for n in self.nodes(sort) if not self.isSwitch(n) and not self.isController(n)]

    # Add a group consisting of a controller, a switch, and a variable number of hosts
    def addIPRewriteGroup(self, name, controller=Floodlight, hosts=1, **opts):
        c = self.addController(name + 'c', controller=controller)
        s = self.addSwitch(name + 's')
        h = self.addHost(name + 'h')
        #self.addLink(c, s)
        self.addLink(s, h)

    # Add an autonomous system consisting of variable IP rewrite groups and a BGP router
    def addAutonomousSystem(self, name, **opts):
        pass


if __name__ == '__main__':
    log.setLogLevel('debug')
    mytopo = Topo()
    mytopo.addIPRewriteGroup('g1')
    mytopo.addIPRewriteGroup('g2')
    net = MiniNExTXL(topo=mytopo, build=True)
    print '-------------------------------------------'
    for c in net.controllers:
        print c.intfs
        print c.ip
        print c.port
        print c.IP()
    print '-------------------------------------------'
    print '-------------------------------------------'
    for s in net.switches:
        print s.intfs
        print s.IP()
    print '-------------------------------------------'
    net.start()
    CLI(net)
    net.stop()
