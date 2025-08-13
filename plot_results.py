import numpy as np 
import matplotlib.pyplot as plt

def plot_simulation(demand, generation, unmet, bat_state_of_charge, peak_start, peak_end):
    #plots the demand, generation, unmet demand, and battery status for each region over time, each region is plotted seperately
    
    time_steps, num_regions = demand.shape 
    time = np.arange(time_steps) 
    
    for region in range(num_regions): #plot each region seperately 
        plt.figure(figsize=(10, 5))
        plt.plot(time, demand[:, region], label='Demand', color='red')
        plt.plot(time, generation[:, region], label='Generation', color='green')
        plt.plot(time, unmet[:, region], label='Unmet Demand', color='blue')
        plt.plot(time, bat_state_of_charge[:, region], label='Battery State', color='purple')

        if peak_start < peak_end: 
            plt.axvspan(peak_start, peak_end, color ='yellow', alpha=0.2, label='Peak Hours') #highlights the peak hours in yellow
        else:
            plt.axvspan(peak_start, 24, color='yellow', alpha=0.2, label='Peak Hours') #handles casess where peak hours cross or wrap around midnight
            plt.axvspan(0, peak_end, color='yellow', alpha=0.2)
        plt.title(f"Region {region} Energy Usage Over Time")
        plt.xlabel("Time (Hours)")
        plt.ylabel("Energy (kW)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()