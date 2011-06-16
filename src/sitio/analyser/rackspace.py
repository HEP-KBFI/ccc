"""
 Module for calculating costs of running services on Rackspace.
"""

from sitio.adapters import CSV_reader
try:
    from pulp.pulp import LpProblem, LpVariable, lpSum, value
    from pulp.constants import LpMinimize, LpContinuous, LpInteger
except ImportError:
    print "Pulp-OR module not installed. get_optimal_rackspace function will not work."

from os import path
vms = CSV_reader.parse_csv2(path.join(path.dirname(__file__), 'pricelist', 'rackspace_computation.csv'))
data = CSV_reader.parse_csv2(path.join(path.dirname(__file__), 'pricelist', 'rackspace_data.csv'))
storage = CSV_reader.parse_csv2(path.join(path.dirname(__file__), 'pricelist', 'rackspace_storage.csv'))

def get_storage_costs(dem_curve):
    """
    Return total cost of the storage on Rackspace. Takes a list of 
    average storage sizes each month. 
    """
    return sum(map(lambda x: storage["storage"] * x, dem_curve))

def get_network_price(net_in, net_out):
    """
    Return the cost of inbound and outbound traffic.
        
    net_in/out values are in GB.
    """
    net_in_price = get_network_in_price(net_in)
    net_out_price = get_network_out_price(net_out)
    return (net_in_price, net_out_price)

def get_network_in_price(net_in):
    """ Return the total price for inbound traffic."""
    return sum(map(lambda x: data["in"] * x, net_in))

def get_network_out_price(net_out):
    """ Return the total price for outbound traffic."""
    return sum(map(lambda x: data["out"] * x, net_out))


def get_optimal_rackspace(cpu_usage, mem_usage, optimal=True, debug=False):
    """ 
    Calculates the price of optimal resources allocation over a certain time span (with monthly granularity). 
    Formulates the problem of satisfying user demand (in CPU and RAM) as an LP problem with a monetary objective function. 
    """    
    assert(len(cpu_usage) == len(mem_usage))
    
    prob = LpProblem("Rackspace cost optimization", LpMinimize)
    # variables
    ## 1h instances
    per_h_ondems = []
    for p in range(len(cpu_usage)):
        per_h_ondems += ["p %s ondem %s" %(p, i) for i in vms.keys()]
    
    category = LpInteger if optimal else LpContinuous
    vars = LpVariable.dicts("rackspace", per_h_ondems, 0, None, cat=category)
    
    # objective function
    prob += lpSum([vars[vm] * vms[vm.split(" ")[3]][0] for vm in per_h_ondems]), "Total cost of running the infra (wrt to CPU/RAM)" 
    
    # constraints    
    ## demand constraints
    for p in range(len(cpu_usage)):
        prob += lpSum([vars[vm] * vms[vm.split(" ")[3]][2] for vm in per_h_ondems if int(vm.split(" ")[1]) == p]) >= cpu_usage[p], "CU demand period %s" %p
        prob += lpSum([vars[vm] * vms[vm.split(" ")[3]][3] for vm in per_h_ondems if int(vm.split(" ")[1]) == p]) >= mem_usage[p], "RAM demand period %s" %p

    prob.solve()
    
    if debug:        
        for v in prob.variables():
            if v.varValue != 0.0:
                print v.name, "=", v.varValue

        print "Total Cost of the solution = ", value(prob.objective)
    
    return value(prob.objective)