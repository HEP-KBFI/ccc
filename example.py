''' Demonstrates usage of cloud-calculator library. '''

# Our goal is to calculate We start by getting usage statistics. This can be 
# either simulated or acquired from one of the monitoring solutions 
# (e.g. Ganglia, Zabbix or collectd). 

# We generate usage statistics for a 12-month period
# Generation result is a list of accumulated monthly usage. 
# The last parameter - 'spikes', 'flat' or 'semi-flat' - is a randomization parameter,
# which describes variation of the usage
from sitio.common.utils import generate_random_usage

# network (GB/month) and storage (avg GB/month)
storage_used = generate_random_usage(40, 'spikes')
network_used_in = generate_random_usage(2, 'spikes')
network_used_out = generate_random_usage(20, 'spikes')

# consumed VM time (h/month) and used memory (GB/h*month), normalized to AWS CPU units 
cpu_usage = generate_random_usage(5000, 'spikes')
mem_usage = generate_random_usage(12000, 'spikes')

# Perform basic analysis
from sitio.analyser import aws, rackspace

# Calculate storage cost on two clouds: AWS and Rackspace
# Pricelists in csv format are located in sitio/analyser/pricelist folder.
ebs_storage_cost, s3_storage_cost = aws.get_storage_costs(storage_used)
rack_storage_costs = rackspace.get_storage_costs(storage_used)
print "Storage costs on AWS: $%s, $%s" %(ebs_storage_cost, s3_storage_cost)
print "Storage costs on Rackspace: $%s" % rack_storage_costs

# To calculate migration costs in a straightforward manner - simply migrating all the data - 
# we need to know two things: cost of moving out and cost of moving in.
aws_to_rack_migration_cost = aws.get_network_out_price(storage_used) + \
                            rackspace.get_network_in_price(storage_used)
print "Cost of migrating data from AWS to Rackspace: $%s " % aws_to_rack_migration_cost

# To get an estimate of how much a certain computational load would cost on a cloud, 
# we provide an implementation of the method described in 
# ''Towards a model for cloud computing cost estimation with reserved resources'', CLOUDCOMP'2010.
# It works by finding cheapest fit using LP of VM time and RAM consumption to cloud provider
# offering. The last boolean argument of the function signifies whether precise solution 
# is sought (True, results in solving NP problem) or approximate is enough (False, fast).
used_reserved_instances, ec2_cost = aws.get_optimal_ec2(cpu_usage, mem_usage, False)
print "Approximate cost on AWS EC2: $%s" % ec2_cost

# To use the same cpu_usage for Rackspace, we need to normalize use by Rackspace benchmark.
# This is an open issue, but some ad hoc testing showed that it is approximately x5 EC2 CU. YMMV.
cpu_usage = [5*x for x in cpu_usage]
rackspace_cost = rackspace.get_optimal_rackspace(cpu_usage, mem_usage, False)
print "Approximate cost of Rackspace: $%s" % rackspace_cost

