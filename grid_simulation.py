import numpy as np
import os 
import pandas as pd 
import matplotlib.pyplot as plt 
from generation_model import generate_power
from load_model import generate_demand 
from user_input import get_user_input
import datetime

def simulate(time_steps, num_regions, trad_power_gen, solar_gen, wind_gen, wind_variability, base_demand, demand_noise, peak_hours, 
            peak_increase, battery_capacity, battery_charge_eff, battery_charge_dis, start_hour, end_hour
            , peak_price, reg_price, peak_emissions, reg_emissions):
    demand_log = np.zeros((time_steps, num_regions)) #how much energy region r needs at time t
    generate_log = np.zeros((time_steps, num_regions)) #how much energy region r generates at time t 
    unmet_demand_log = np.zeros((time_steps, num_regions)) #how much energy region r needs at time t but does not have (blackout energy)
    battery_charge_state = np.zeros((time_steps + 1, num_regions)) #battery charge state for each region at time t, extra for t = 0
    
    total_cost = 0.0
    total_emissions = 0.0
    total_grid_energy = 0.0 
    total_battery_throughput = 0.0 #tracks charging and discharging 
    for t in range(time_steps):
        for region in range(num_regions):
            demand = generate_demand(t, region, base_demand, demand_noise, peak_hours, peak_increase)
            generate = generate_power(t, region, trad_power_gen, solar_gen, wind_gen, wind_variability)
            
            demand_log[t, region] = demand #this logs the demand for the region at time t
            generate_log[t, region] = generate #this logs the generation for the region at time t
            surplus = generate - demand 
            
            #pricing and emissions calculations
            price = peak_price if t in peak_hours else reg_price
            emissions = peak_emissions if t in peak_hours else reg_emissions
            if surplus >= 0: #if generation of power is greater than the demand, then the battery will be charged @ 90% efficiency
                charge_amt = surplus * battery_charge_eff
                available_cap = battery_capacity - battery_charge_state[t, region]
                true_charge = min(charge_amt, available_cap) #if the amount of excess is greater than the available capactity, then only charge the battery to the available capacity to prevent overflow
                battery_charge_state[t + 1, region] = battery_charge_state[t, region] + true_charge
                unmet = 0
                unmet_demand_log[t, region] = unmet 
                total_battery_throughput += true_charge 
            else: #if generation of power is less than the demand, then the battery will be discharged @ 90% efficiency 
                energy_needed = -surplus 
                max_discharge = battery_charge_state[t, region] * battery_charge_dis
                true_discharge = min(energy_needed, max_discharge)
                unmet = energy_needed - true_discharge #finds the unmet demand after discharging the battery
                battery_charge_state[t + 1, region] = battery_charge_state[t, region] - (true_discharge / battery_charge_dis) #accounts for the inefficiency of the battery 
                unmet_demand_log[t, region] = unmet 
                total_battery_throughput += true_discharge / battery_charge_dis 
                if unmet > 0: 
                    total_grid_energy += unmet 
                    total_cost += unmet * price
                    total_emissions += unmet * emissions 
    print("\n Simulation Summary: ")
    print(f"Total Grid Energy Imported: {total_grid_energy:.2f} kWh")
    print(f"Total Cost: ${total_cost:.2f}")
    print(f"Total Emissions: {total_emissions:.2f} kg CO2")
    print(f"Total Battery Energy Changes: {total_battery_throughput:.2f} kWh")
    return demand_log, generate_log, unmet_demand_log, battery_charge_state[:-1], total_grid_energy, total_cost, total_battery_throughput, total_emissions #drops last row to ensure matching shape with other logs

def save_to_csv(demand_log, generate_log, unmet_demand_log, bat_state_of_charge , total_cost, total_emissions, grid_energy, battery_flow):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("results", exist_ok=True) #makes sure the results folder is created if it does not already exist 
    
    #save main logs for demand, generation, unmet demand, and battery state of charge
    np.savetxt(f"results/demand_{timestamp}.csv", demand_log, delimiter=",", fmt="%.2f")
    np.savetxt(f"results/generation_{timestamp}.csv", generate_log, delimiter=",", fmt="%.2f")
    np.savetxt(f"results/unmet_demand_{timestamp}.csv", unmet_demand_log, delimiter=",", fmt="%.2f")
    np.savetxt(f"results/battery_soc_{timestamp}.csv", bat_state_of_charge, delimiter=",", fmt="%.2f")
    
    #save summary stats 
    summary_df = pd.DataFrame({
        "Metric": ["Total Grid Energy", "Total Cost", "Total Emissions", "Total Battery Flow"],
        "Value": [grid_energy, total_cost, total_emissions, battery_flow]
    })
    summary_df.to_csv(f"results/summary_{timestamp}.csv", index=False)
    print("Results have been saved to the 'results/' folder.")
        
if __name__ == "__main__": #call the plotter
    print("Starting simulation:")
    inputs = get_user_input()
    (time_steps, num_regions, trad_power_gen, solar_gen, wind_gen, wind_variability, base_demand, demand_noise, peak_hours, 
    peak_increase, battery_capacity, battery_charge_eff, battery_charge_dis, start_hour, end_hour
    , peak_price, reg_price, peak_emissions, reg_emissions) = inputs
    print("Inputs received, running simulation: ")
    demand, generate, unmet, bat_state_of_charge, total_cost, total_emissions, grid_energy, battery_flow = simulate(time_steps, num_regions, trad_power_gen, solar_gen, wind_gen, wind_variability, base_demand, demand_noise, peak_hours, 
    peak_increase, battery_capacity, battery_charge_eff, battery_charge_dis, start_hour, end_hour
    , peak_price, reg_price, peak_emissions, reg_emissions)
    from plot_results import plot_simulation
    plot_simulation(demand, generate, unmet, bat_state_of_charge, start_hour, end_hour)
    
    #save results 
    save_to_csv(demand, generate, unmet, bat_state_of_charge, total_cost, total_emissions, grid_energy, battery_flow)

