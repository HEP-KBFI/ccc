import unittest
import test_aws
import test_rackspace

if __name__ == '__main__':
    aws_costs = unittest.TestLoader().loadTestsFromTestCase(test_aws.TestAWSCosts)
    rs_costs = unittest.TestLoader().loadTestsFromTestCase(test_rackspace.TestRackspaceCosts)
    unittest.TextTestRunner(verbosity=2).run(
                                             unittest.TestSuite([aws_costs, rs_costs]))