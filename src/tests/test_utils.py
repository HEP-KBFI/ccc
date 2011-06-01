
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
        
