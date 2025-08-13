import numpy as np 

def solar_generation(timestep, solar_power_gen):
    #models the solar power generation based on the time of day using a sinusoidal wave function. Peak at miday, at night 0. 
    
    #normalize the time step from 0-2pi over a 24 hour day 
    angle = (timestep / 24) * 2 * np.pi 
    
    #sinusodial generation function: max at 12 pm (midday), 0 at night 
    output = solar_power_gen * max(np.sin(angle - np.pi / 2), 0)
    
    return output 

def wind_generation(timestep, region, wind_power_gen, wind_variability):
    #models the wind power generation based random variability centered at around 60% max, fluctuates independently on region and time step
    
    #model wind power generation as 60% of max 
    mean_output = 0.6 * wind_power_gen 
    
    #add random noise using normal distribution
    output = np.random.normal(loc= mean_output, scale = wind_variability)

    return output 

def traditional_generation(timestep, trad_power_gen):
    #models traditional power generation as a constant value, simulating a stable output 
    
    #model traditional power generation as a constant value 
    output = trad_power_gen
    
    #potential expansion later includes blackout variables, delays, and maintence delays 
    return output 

def generate_power(timestep, region, solar_power_gen, wind_power_gen, trad_power_gen, wind_variability):
    #models the total power generation for a region at a specific time step by combining its solar, wind, and traditional power generation
    
    solar = solar_generation(timestep, solar_power_gen) #get solar generation
    wind = wind_generation(timestep, region, wind_power_gen, wind_variability) #get wind generation
    tradition = traditional_generation(timestep, trad_power_gen) #get traditional generation 
    
    total_generation = solar + wind + tradition #sum all power generation sources 
    return total_generation 

'''for hour in range(24):
    power = generate_power(hour, region = 0)
    print(f"Hour {hour}: total generation = {power:.2f} kW") '''