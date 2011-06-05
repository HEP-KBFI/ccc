import unittest
from sitio.analyser import aws 

import random
from sitio.common.utils import generate_random_usage

class TestAWSCosts(unittest.TestCase):

    def testAWSComputationalCosts(self):                
        cpu_usage = generate_random_usage(random.randint(1,100000), 'spikes')
        mem_usage = generate_random_usage(random.randint(1,100000), 'spikes')
        _, ec2_cost = aws.get_optimal_ec2(cpu_usage, mem_usage, False)
        self.assertTrue(ec2_cost > 0)
        deployment, ec2_cost = aws.get_optimal_ec2([0], [0])
        self.assertTrue(ec2_cost == 0)
        self.assertTrue(deployment == {})
        
        # assure it's a monotonically increasing function
        cpu = random.randint(1,1000)
        mem = random.randint(1,1000)
        _, ec2_cost = aws.get_optimal_ec2([cpu], [mem])        
        _, ec2_cost2 = aws.get_optimal_ec2([cpu*1.2], [mem*1.2])        
        self.assertTrue(ec2_cost <= ec2_cost2)
        
        # solve in integers
        # assure that no reserved instances are offered for small numbers
        pack, _ = aws.get_optimal_ec2([1], [1], True)
        self.assertTrue(pack == {})
        
    def testAWSStorageCosts(self):
        current_storage = generate_random_usage(random.randint(10,100), 'spikes')    
        ebs_storage_cost, s3_storage_cost = aws.get_storage_costs(current_storage)
        self.assertTrue(s3_storage_cost > 0)
        self.assertTrue(ebs_storage_cost > 0)
        ebs_storage_cost, s3_storage_cost = aws.get_storage_costs([0])
        self.assertTrue(s3_storage_cost == 0)
        self.assertTrue(ebs_storage_cost == 0)
    
    def testNetoworkOutAWSCosts(self):
        vals = [random.randint(1, 1000) for _ in range(12)]
        net_cost = aws.get_network_out_price(vals) 
        self.assertTrue(net_cost > 0) 
        net_cost = aws.get_network_out_price([])
        self.assertTrue(net_cost == 0)
        
    def testNetworkInAWSCosts(self):       
        vals = [random.randint(1, 1000) for _ in range(12)] 
        net_cost = aws.get_network_in_price(vals) 
        self.assertTrue(net_cost > 0) 
        net_cost = aws.get_network_in_price([])
        self.assertTrue(net_cost == 0)

if __name__ == "__main__":
    unittest.main()