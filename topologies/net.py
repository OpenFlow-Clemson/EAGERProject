from mininext.net import MiniNExT as Mininext


class MiniNExTXL(Mininext):
    """Extended MiniNExT class that adds the ability to add controllers from a Topo class"""

    def buildFromTopo(self, topo=None):
        print '*** Adding controllers:'
        for controllerName in topo.controllers():
            self.addController(controllerName, **topo.nodeInfo(controllerName))
            print controllerName + ' '
        Mininext.buildFromTopo(self, topo)
