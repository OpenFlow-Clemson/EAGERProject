from quagga_driver import QuaggaDriver
import time


peering_prefix = ['184.164.240.0/24', '184.164.241.0/24', '184.164.242.0/24', '184.164.243.0/24']

home_ASN = '47065'

quagga_node = 'quaggaS'

quagga_node_C = 'quaggaC'

route_map = 'AMSIX'

class bgpMgmt:
    def __init__(self):
        self.bgpController = QuaggaDriver()

    def show_node_prefix(self, node):
        print '>>> Display Current BGP Prefix on Node', node, '!!'
        self.bgpController.show_bgp_all_prefix(node)
        print '\n\n'

    def show_all_neighbors(self, node):
        print '>>> Display BGP neighbors on Node', node, '!!'
        self.bgpController.show_bgp_neighbors(node)
        print '\n\n'

    def show_node_neighbor(self, node, prefix):
        print '>>> Display BGP neighbor ', prefix, ' on Node', node, '!!'
        self.bgpController.show_bgp_neighbor(node, prefix)
        print '\n\n'


    def show_adv_route(self, node, prefix):
        print '>>> Display advertised routes on Node', node, '!!'
        self.bgpController.show_adv_routes(node, prefix)
        print '\n\n'

    # inbound soft-reconfiguration must be enabled
    def show_recv_route(self, node, prefix):
        print '>>> Display received routes on Node', node, '!!'
        self.bgpController.show_recv_routes(node, prefix)
        print '\n\n'


    def show_learned_route(self, node, prefix):
        print '>>> Display learned BGP routes on Node', node, '!!'
        self.bgpController.show_learned_routes(node, prefix)
        print '\n\n'


    def show_route_map(self, node, route_map):
        print '>>> Display BGP route-map on Node', node, '!!'
        self.bgpController.show_route_map(node, route_map)
        print '\n\n'


    def prefix_announce(self, node, router_id, prefix):
        print '>>> Inject BGP prefix ', prefix, ' on Node', node, '!!'
        self.bgpController.inject_one_prefix(node, router_id, prefix)
        # self.bgpController.show_advertise_routes(node, prefix)
        print '\n\n'



    # Flip bgp prefix in certain time interval
    # Can NOT Flap prefix too fast, needs to stick on one announcement for 2h
    def prefix_flip(self, node, router_id, prefix_orin, prefix_new, delay_interval):
        self.bgpController.inject_one_prefix(node, router_id, prefix_new)
        time.sleep(delay_interval)
        self.bgpController.remove_one_prefix(node, router_id, prefix_orin)


def main():
    bgpManager = bgpMgmt()

    # BGP manipulation on Server side
    # bgpManager.show_node_neighbor(quagga_node, '100.69.128.1')
    # bgpManager.show_adv_route(quagga_node, '100.69.128.1')
    bgpManager.prefix_announce(quagga_node, home_ASN, peering_prefix[3])
    # bgpManager.show_adv_route(quagga_node, '100.69.128.1')


    # BGP manipulation on Client side
    bgpManager.prefix_announce(quagga_node_C, home_ASN, peering_prefix[2])




if __name__ == '__main__':
    main()


