def get_user_input():
    try: 
        time_steps = int(input("Enter number of time steps (ex- 24 for 24 hrs): "))
        num_regions = int(input("Enter number of regions (ex- 1 for a single region or 4 for like cardinal directions): "))
        trad_power_gen = int(input("Enter tradition power generation (kW): "))
        solar_gen = int(input("Enter solar power generation (kW): "))
        wind_gen = int(input("Enter wind power generation (kW): "))
        wind_variability = int(input("Enter wind generation variability (the standard deviation of fluctations in kW): "))
        base_demand = int(input("Enter base demand (kW): "))
        demand_noise = int(input("Enter demand noise (standard deviation of demand fluctuations in kW): "))
        
        #PEAK HOUR INPUT 
        peak_hours = input("Enter peak hour(s) as a start-end (ex- 16-20 for 4pm to 8pm): ")
        try:
            start_hour, end_hour = map(int, peak_hours.split('-'))
            if 0 <= start_hour < end_hour <= time_steps:
                peak_hours = range(start_hour, end_hour)
            else:
                print(f"Invalid peak hours range. Must be between 0 to {time_steps} and starting hours < ending hours.")
                exit()
        except ValueError: 
            print("Invalid format for peak hours. Use start-end (ex- 16-20).")
            
        peak_increase = int(input("Enter peak hour(s) demand increase (kW): "))
        battery_capacity = int(input("Enter battery capacity (kWh): "))
        battery_charge_eff = int(input("Enter battery charge efficiency (0-100%): ")) / 100
        battery_charge_dis = int(input("Enter battery discharge efficiency (0-100%): ")) / 100
    except ValueError:
        print("Invalid input. Enter a whole number: ")
        exit()
        
    #PRICING SETUP
    print("\n -----------Dynamic Pricing Setup-----------")
    peak_price = float(input("Enter peak hour price ($/kWh), ex- 0.30: "))
    reg_price = float(input("Enter regular hour price ($/kWh), ex- 0.10: "))
    
    #CO2 EMISSIONS SETUP 
    print("\n -----------Dynamic CO2 Emissions Setup-----------")
    peak_emissions = float(input("Enter peak hour emissions (kg CO2/kWh), ex- 0.6: "))
    reg_emissions = float(input("Enter regular hour emissions (kg CO2/kWh), ex- 0.3: "))
    return (time_steps, num_regions, trad_power_gen, solar_gen, wind_gen, wind_variability, base_demand, demand_noise, peak_hours, 
            peak_increase, battery_capacity, battery_charge_eff, battery_charge_dis, start_hour, end_hour
            , peak_price, reg_price, peak_emissions, reg_emissions)
