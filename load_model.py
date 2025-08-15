import numpy as np 
def generate_demand(time_step, region, base_demand, peak_increase, peak_hours, demand_noise):
    #models electricity demand for a region at a specific time. Accounts for peak hours and noise 
    
    demand = base_demand 
    
    if time_step in peak_hours: #if time is during peak hours, add the peak increase to demand 
        demand += peak_increase  
        
    #add noise to simulate real-world variability in demand 
    noise = np.random.normal(0, demand_noise)
    demand += noise 
    

    return max(demand, 0) #ensure that demand is never below 0 
