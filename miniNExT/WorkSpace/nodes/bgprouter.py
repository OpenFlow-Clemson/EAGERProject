from mininet.node import Node
import mininet.log as log
from bgp_router_cntl import BGPRTCntl


class BGPRouter(Node):

    def __init__(self, node):
        Node.__init__(self, node)
        self.routerController = BGPRTCntl()
        self.router = node


    def show_prefix(self):
        print 'Display Current BGP Prefix on Node', self.node, '!!'
        self.routerController.show_bgp_all_prefix(self.node)
        print '\n\n'



