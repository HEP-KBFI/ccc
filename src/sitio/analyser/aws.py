"""
 Module for calculating costs of running services on AWS.
"""

from sitio.adapters import CSV_reader
from pulp.pulp import LpProblem, LpVariable, lpSum, value
from pulp.constants import LpMinimize, LpStatus, LpInteger, LpContinuous

# node parameters [price, 1year, 3year, reserved_price, RAM, CU, disk]
# <type>_<size>_<model>
from os import path
vms = CSV_reader.parse_csv2(path.join(path.dirname(__file__), 'pricelist', 'aws_computation.csv'))
data = CSV_reader.parse_csv2(path.join(path.dirname(__file__), 'pricelist', 'aws_data.csv'))
storage = CSV_reader.parse_csv2(path.join(path.dirname(__file__), 'pricelist', 'aws_storage.csv'))

def get_storage_costs(dem_curve):
    """
    Return total cost of the storage for S3 and EBS services. Takes a list of 
    average storage sizes each month. 
    """
    s3_price = sum(map(lambda x: storage["s3-simple"][0] * x, dem_curve))
    ebs_price = sum(map(lambda x: storage["ebs-volumes"][0] * x, dem_curve))
    return (s3_price, ebs_price)

def get_network_price(net_in, net_out):
    """
    Return the cost of inbound and outbound traffic.
        
    net_in/out values are in GB.
    """
    
    # simple for net-in
    net_in_price = get_network_in_price(net_in)
    net_out_price = get_network_out_price(net_out)
    return (net_in_price, net_out_price) 

def get_network_in_price(net_in):
    """ Return the total price for inbound traffic."""
    return sum(map(lambda x: data["in"] * x, net_in))

def get_network_out_price(net_out):
    """ Return the total price for outbound traffic."""
    # more complicated for net-out
    net_out_monthly = []
    # for each month
    for i in net_out:
        curr_price = 0      
        if i <= 1:
            curr_price += i*data['out-1GB']
            net_out_monthly.append(curr_price)
            continue
        if i <= 10 * 1024 + 1:
            curr_price += 1 * data['out-1GB']
            curr_price += (i - 1)*data['out-10TB']
            net_out_monthly.append(curr_price)
            continue
        if i <= 50 * 1024 + 1:
            curr_price += 1 * data['out-1GB']
            curr_price += 10 * 1024 * data['out-10TB']
            curr_price += (i - 1 - (10 * 1024))*data['out-40TB']
            net_out_monthly.append(curr_price)
            continue
        if i <= 150 * 1024 + 1:
            curr_price += 1 * data['out-1GB']
            curr_price += 10 * 1024 * data['out-10TB']
            curr_price += 40 * 1024 * data['out-40TB']
            curr_price += (i - 1 - (50 * 1024))*data['out-100TB']
            net_out_monthly.append(curr_price)
            continue
        else:
            curr_price += 1 * data['out-1GB']
            curr_price += 10 * 1024 * data['out-10TB']
            curr_price += 40 * 1024 * data['out-40TB']
            curr_price += 100 * 1024 * data['out-100TB']
            curr_price += (i - 1 - (150 * 1024))*data['out-150TB']
            net_out_monthly.append(curr_price)         
        
    return sum(net_out_monthly)

def get_optimal_ec2(cpu_usage, mem_usage, optimal=True, debug=False):
    """ 
    Calculates the optimal allocation of resources over a certain time span (with monthly granularity). 
    Formulates the problem of satisfying user demand (in CPU and RAM) as an LP problem with a monetary objective function. 
    
    Returns allocation of reserved instances and a total price for running the allocation on AWS.    
    """    
    assert(len(cpu_usage) == len(mem_usage))
    
    prob = LpProblem("The Simplified EC2 cost optimization", LpMinimize)
    # variables
    ## 1h instances (both on-demand and reserved)
    per_h_ondems = []
    per_h_reserved = []
    for p in range(len(cpu_usage)):
        # ondemand
        per_h_ondems += ["p %s ondem %s" %(p, i) for i in vms.keys()]
        # reserved
        per_h_reserved += ["p %s reserved %s" %(p, i) for i in vms.keys()]
        
    ## nr of 1-year reserved instances
    nr_of_1year_reserved = [ "res_1year %s" % i for i in vms.keys()]
    nr_of_3year_reserved = [ "res_3year %s" % i for i in vms.keys()]
    
    category = LpInteger if optimal else LpContinuous
    vars = LpVariable.dicts("aws", per_h_ondems + per_h_reserved + nr_of_1year_reserved + nr_of_3year_reserved, \
                            lowBound = 0, upBound = None, cat = category)

    # objective function    
    prob += lpSum([vars[vm] * vms[vm.split(" ")[3]][0] for vm in per_h_ondems]) \
            + lpSum([vars[vm] * vms[vm.split(" ")[3]][3] for vm in per_h_reserved]) \
            + lpSum([vars[vm] * vms[vm.split(" ")[1]][1] for vm in nr_of_1year_reserved]) \
            + lpSum([vars[vm] * vms[vm.split(" ")[1]][2] for vm in nr_of_3year_reserved]) \
            , "Total cost of running the infrastructure consuming (CPU/RAM)/h" 

    # constraints
    ## demand constraints
    for p in range(len(cpu_usage)):
        prob += lpSum([vars[vm] * vms[vm.split(" ")[3]][4] for vm in (per_h_ondems + per_h_reserved) if int(vm.split(" ")[1]) == p]) >= cpu_usage[p], "CPU demand, period %s" %p
        prob += lpSum([vars[vm] * vms[vm.split(" ")[3]][5] for vm in (per_h_ondems + per_h_reserved) if int(vm.split(" ")[1]) == p]) >= mem_usage[p], "RAM demand. period %s" %p
    
    ## constraints on the reserved instances - cannot use more than we paid for
    for i in per_h_reserved:
        t = i.split(" ")[3]
        prob += vars["res_1year %s" % t] + vars["res_3year %s" % t] >= vars[i], "Nr. of used reserved machines of type %s" %i
    prob.writeLP("/tmp/tmp.lp")
    prob.solve()  # for practical reasons don't wait too long   
    
    
    if debug:
        print "Status:", LpStatus[prob.status]
        print "Total Cost of the solution = ", value(prob.objective)
    
    res_instance = {}
    for v in prob.variables():
        if v.name.startswith("aws_res_") and v.varValue != 0.0:
            res_instance[v.name] = v.varValue
        
        if debug and v.varValue != 0.0:
            print v.name, "=", v.varValue
    
    return (res_instance, value(prob.objective))
