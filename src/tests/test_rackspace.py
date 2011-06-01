import unittest
from test_utils import generate_random_usage
from sitio.analyser import rackspace 

import random

class TestRackspaceCosts(unittest.TestCase):

    def testRackspaceComputationalCosts(self):                
        cpu_usage = generate_random_usage(random.randint(1,100000), 'spikes')
        mem_usage = generate_random_usage(random.randint(1,100000), 'spikes')
        rackspace_cost = rackspace.get_optimal_rackspace(cpu_usage, mem_usage, False)
        self.assertTrue(rackspace_cost > 0)
        rackspace_cost = rackspace.get_optimal_rackspace([0], [0])
        self.assertTrue(rackspace_cost == 0)        
        
        # assure it's a monotonically increasing function
        cpu = random.randint(1,1000)
        mem = random.randint(1,1000)
        rackspace_cost = rackspace.get_optimal_rackspace([cpu], [mem])        
        rackspace_cost2 = rackspace.get_optimal_rackspace([cpu*1.2], [mem*1.2])        
        self.assertTrue(rackspace_cost <= rackspace_cost2)
    
    def testAWSStorageCosts(self):
        current_storage = generate_random_usage(random.randint(10,100), 'spikes')    
        rack_costs = rackspace.get_storage_costs(current_storage)
        self.assertTrue(rack_costs > 0)
        rack_costs = rackspace.get_storage_costs([0])
        self.assertTrue(rack_costs == 0)

    
    def testNetoworkOutRackspaceCosts(self):
        vals = [random.randint(1, 1000) for _ in range(12)]
        net_cost = rackspace.get_network_out_price(vals) 
        self.assertTrue(net_cost > 0) 
        net_cost = rackspace.get_network_out_price([])
        self.assertTrue(net_cost == 0)
        
    def testNetworkInRackspaceCosts(self):       
        vals = [random.randint(1, 1000) for _ in range(12)] 
        net_cost = rackspace.get_network_in_price(vals) 
        self.assertTrue(net_cost > 0) 
        net_cost = rackspace.get_network_in_price([])
        self.assertTrue(net_cost == 0)

if __name__ == "__main__":
    unittest.main()