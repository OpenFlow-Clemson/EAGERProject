import inspect
import os
import sys

sys.path.insert(0, os.path.abspath('..'))

from mininext.topo import Topo
from mininet.log import info

from mininext.services.quagga import QuaggaService
from collections import namedtuple

QuaggaHost = namedtuple("QuaggaHost", "name ip loIP")
net = None


class QuaggaTopo(Topo):
    """Creates a topology of Quagga routers"""

    def __init__(self):
        """Initialize a Quagga topology with 5 routers, configure their IP
           addresses, loop back interfaces, and paths to their private
           configuration directories."""
        info("*** Init parent Topo class\n")
        Topo.__init__(self)

        # Directory where this file / script is located"
        selfPath = os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe())))  # script directory

        # Initialize a service helper for Quagga with default options
        info("*** Start Quagga service\n")
        quaggaSvc = QuaggaService(autoStop=False)

        # Path configurations for mounts
        quaggaBaseConfigPath = selfPath + '/configs/'

        # List of Quagga host configs
        info("*** Create list of Quagga host configs\n")
        quaggaHosts = []
        quaggaHosts.append(QuaggaHost(name='as1', ip='100.0.0.1/24',
                                      loIP='1.1.1.1/24'))
        quaggaHosts.append(QuaggaHost(name='as2', ip='100.0.0.2/24',
                                      loIP='2.2.2.2/24'))
        quaggaHosts.append(QuaggaHost(name='as3', ip='100.0.0.3/24',
                                      loIP='3.3.3.3/24'))

        # Add switches
        info("*** Add two switches\n")
        sw1 = self.addSwitch(name='sw1', dpid='0000000000000001', failMode='secure')
        sw2 = self.addSwitch(name='sw2', dpid='0000000000000002', failMode='secure')
        sw3 = self.addSwitch(name='sw3', dpid='0000000000000003', failMode='secure')
        sw4 = self.addSwitch(name='sw4', dpid='0000000000000004', failMode='standalone')

        # Add Hosts
        info('*** Adding two regular hosts..\n')
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')

        # Add Links b/w host and OVS switch
        info('*** Adding links between regular hosts and switches..\n')
        self.addLink(h1, sw1)
        self.addLink(h2, sw2)
        self.addLink(h3, sw3)

        # Setup each Quagga router, add link between Routers
        quaggaContainerList = []
        for host in quaggaHosts:
            # Create an instance of a host, called a quaggaContainer
            quaggaContainer = self.addHost(name=host.name,
                                           ip=host.ip,
                                           hostname=host.name,
                                           privateLogDir=True,
                                           privateRunDir=True,
                                           inMountNamespace=True,
                                           inPIDNamespace=True,
                                           inUTSNamespace=True)

            # Add a loopback interface with an IP in router's announced range
            self.addNodeLoopbackIntf(node=host.name, ip=host.loIP)

            # Configure and setup the Quagga service for this node
            quaggaSvcConfig = \
                {'quaggaConfigPath': quaggaBaseConfigPath + host.name}
            self.addNodeService(node=host.name, service=quaggaSvc,
                                nodeConfig=quaggaSvcConfig)

            # Attach the quaggaContainer to the IXP Fabric Switch
            # self.addLink(quaggaContainer, sw)

            quaggaContainerList.append(quaggaContainer)

        # Add Link b/w quagga Router & OVS switch
        self.addLink(sw1, quaggaContainerList[0])
        self.addLink(sw2, quaggaContainerList[1])
        self.addLink(sw3, quaggaContainerList[2])
        # self.addLink(quaggaContainerList[0], quaggaContainerList[1])
        # self.addLink(quaggaContainerList[1], quaggaContainerList[2])
        # self.addLink(quaggaContainerList[0], quaggaContainerList[2])
        self.addLink(quaggaContainerList[0], sw4)
        self.addLink(quaggaContainerList[1], sw4)
        self.addLink(quaggaContainerList[2], sw4)
