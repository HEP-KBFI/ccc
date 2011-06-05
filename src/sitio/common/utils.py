import time
import datetime

def print_ec2_costs(dc, sols):
    """Print out costs for AWS EC2 wrt to CPU and RAM in a very basic format 
    for easy import into Excel."""
    assert(len(dc) == len(sols))
    for i in range(len(dc)):
        print dc[i][0], dc[i][1], sols[i]
        
def nonneg(val):
    if val == None or val < 0:
        return 0
    else:        
        return val

def minusone_or_value(val):
    if val < 0:
        return -1
    else:
        return val

def num(s):
    from exceptions import ValueError
    try:
        return int(s)
    except ValueError:
        return float(s)

def unix2date(unix):
    return str(datetime.date.fromtimestamp(unix))

def date2unix(date):
    date = date.split('.')
    timestamp = (int(date[2]), int(date[1]), int(date[0]), 0, 0, 0, 0, 0, 0)
    return time.mktime(timestamp)

import random

def generate_random_usage(value, usage_pattern):
    """
    Generate uniformly random resource usage values for 12 periods (month) based on the initial value
    and the pattern type - 'flat', 'semi-flat' or 'spikes'. 
    """     
    coeff = 0
    if usage_pattern == 'flat': coeff = 0.1
    if usage_pattern == 'semi-flat': coeff = 0.3
    if usage_pattern == 'spikes': coeff = 0.7
    return [(int(random.uniform(1 - coeff, 1 + coeff) * value)) for _ in range(12)]
