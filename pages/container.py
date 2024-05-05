import streamlit as st
import pandas as pd
import plotly.graph_objs as go

global total_new_co2_emission
# Load the dataset
appliances_data = {
    "Appliance": ["Refrigerator", "Television", "Computer/Laptop", "Washing Machine", "Dryer",
                  "Dishwasher", "Oven/Stove", "Microwave", "Toaster", "Electric Kettle",
                  "Coffee Maker", "Blender", "Vacuum Cleaner", "Iron", "Hairdryer",
                  "Air Conditioner", "Heater", "Fan", "LED Light", "Incandescent Light", "Water Heater"],
    "CO2_Emission_kg": [0.22, 0.088, 0.015, 0.75, 1, 0.7, 0.3, 0.2, 0.1, 0.1, 0.075, 0.075, 0.15, 0.1, 0.15,
                        1.25, 1.25, 0.075, 0.0075, 0.05, 1.5]
}
appliances_df = pd.DataFrame(appliances_data)

# Main function to run the Streamlit app
def main():
    st.title("Household Appliance CO2 Emissions Calculator")
    appliance_dictionary={}
    total_new_co2_emission = 0
    col1, col2 = st.columns([2,1])

    with col1:
        st.subheader('Select your Daily Appliance Usage')
        # Multi-select for selecting appliances
        selected_appliances = col1.multiselect("Select Appliances", appliances_df["Appliance"])
        
    with col2:
        usage_hours = {}  # Initialize usage_hours dictionary

        if selected_appliances:
            # Expander for taking user input for hours
            st.subheader('Individual Appliance Input')
            with st.expander("Adjust Hours Used"):
                for appliance in selected_appliances:
                    usage_hours[appliance] = st.slider(f"{appliance} - Hours used", min_value=0.0, max_value=24.0, value=0.0, 
                                                        step=0.25)


    if selected_appliances:
        total_emissions = {}
        with st.expander('Viz for your Appliance usage'):
                # Calculate total CO2 emissions for selected appliances
                for appliance, hours in usage_hours.items():
                    emission = appliances_df.loc[appliances_df['Appliance'] == appliance, 'CO2_Emission_kg'].values[0]
                    total_emissions[appliance] = emission * hours

                # Sort appliances by CO2 emissions (descending order)
                sorted_appliances = sorted(total_emissions, key=total_emissions.get, reverse=True)

                # Define a custom color scale from dark blue to medium blue
                custom_color_scale = [
                    (0, '#B0E0E6'),  # Dark blue
                    (0.5, '#6495ED'),  # Medium blue
                    (1, '#000080')  # Light blue
                ]
                # Display total CO2 emissions
                total_co2 = sum(total_emissions.values())
                st.metric(label="Total Appliances Co2 Emissions (kg)", value=round(total_co2, 2))
                # Plot horizontal bar chart with custom color scale
                fig = go.Figure(go.Bar(
                    x=[total_emissions[appliance] for appliance in sorted_appliances],
                    y=sorted_appliances,
                    orientation='h',
                    marker=dict(
                        color=[total_emissions[appliance] for appliance in sorted_appliances],  # Use CO2 emissions as color values
                        colorscale=custom_color_scale,  # Use custom color scale
                        colorbar=dict(title='CO2 Emissions (kg)')
                    )
                ))
                fig.update_layout(title="CO2 Emissions by Appliance", xaxis_title="CO2 Emissions (kg)",
                                yaxis_title="Appliance", showlegend=False)
                st.plotly_chart(fig)
    if selected_appliances:
            with st.expander('Co2 emmission saving in appliances'):
                co2_emissions_saved_placeholder = st.empty()
                col1, col2, col3 = st.columns([1,1,1])

                for i, appliance in enumerate(selected_appliances):
                    if i % 3 == 0:
                        with col1:
                            total_new_co2_emission += create_container(appliance, usage_hours, total_new_co2_emission, total_emissions)
                    elif i % 3 == 1:
                        with col2:
                            total_new_co2_emission += create_container(appliance, usage_hours, total_new_co2_emission, total_emissions)
                    else:
                        with col3:
                            total_new_co2_emission += create_container(appliance, usage_hours, total_new_co2_emission, total_emissions)
                co2_emissions_saved_placeholder.metric(label="Total CO2 emission savings", value=total_new_co2_emission, delta=True)            

def create_container(appliance, usage_hours, total_new_co2_emission, total_emissions):
    with st.container(border=True, height=300):
        co2_emission_saved=0
        if appliance == "Water Heater":
            st.subheader(appliance)
            use_less_hot_water = st.checkbox("Use less hot water", key=f"{appliance}_checkbox1")
            use_renewable_fuels = st.checkbox("Use renewable fuels", key=f"{appliance}_checkbox2")
            use_better_tech = st.checkbox("Use better technology/hybrid with renewables", key=f"{appliance}_checkbox3")
            if use_less_hot_water:
                duration = st.number_input("Duration (hours)", key=f"{appliance}_duration", value=0.0, min_value=0.0, step=0.25, max_value=usage_hours[appliance])
                new_co2_emission = duration * 0.5  # Adjust this value as needed
                if duration:
                    co2_emission_saved =  total_emissions[appliance]   - new_co2_emission
                    st.write(f"CO2 emission savings for {appliance}: {co2_emission_saved} kg")
                    total_new_co2_emission += co2_emission_saved
        elif appliance == "Air Conditioner":
            st.subheader(appliance)
            switched_off_ac = st.checkbox("Switched off AC", key=f"{appliance}_checkbox4")
            increased_temp_settings = st.checkbox("Increase temperature settings", key=f"{appliance}_checkbox5")
            if switched_off_ac or increased_temp_settings:
                duration = st.number_input("Duration (hours)", key=f"{appliance}_duration", value=0.0, min_value=0.0, step=0.25, max_value=usage_hours[appliance])
                temperature = st.number_input("Temperature (°C)", key=f"{appliance}_temperature", value=0, step=1)
                new_co2_emission = duration * 1.0  # Adjust this value as needed
                if duration:
                    co2_emission_saved =  total_emissions[appliance]   - new_co2_emission
                    st.write(f"CO2 emission savings for {appliance}: {co2_emission_saved} kg")
                    total_new_co2_emission += co2_emission_saved
        # Add other appliances and their conditions here
        elif appliance == "Heater":
            st.subheader(appliance)
            switched_off_heater = st.checkbox("Switched off Heater", key=f"{appliance}_checkbox6")
            reduced_temp_settings = st.checkbox("Reduced temperature settings", key=f"{appliance}_checkbox7")
            if switched_off_heater or reduced_temp_settings:
                duration = st.number_input("Duration (hours)", key=f"{appliance}_duration", value=0.0, min_value=0.0, step=0.25, max_value=usage_hours[appliance])
                temperature = st.number_input("Temperature (°C)", key=f"{appliance}_temperature", value=0, step=1)
                new_co2_emission = duration * 1.25  # Adjust this value as needed
                
                if duration:
                    co2_emission_saved =  total_emissions[appliance]   - new_co2_emission
                    st.write(f"CO2 emission savings for {appliance}: {co2_emission_saved} kg")
                    total_new_co2_emission += co2_emission_saved
        # Repeat this pattern for each appliance
        elif appliance == "Television":
            st.subheader(appliance)
            did_not_use_tv = st.checkbox("Did not use TV", key=f"{appliance}_checkbox8")
            if did_not_use_tv:
                duration = st.number_input("Duration (hours)", key=f"{appliance}_duration", value=0.0, min_value=0.0, step=0.25, max_value=usage_hours[appliance])
                new_co2_emission = duration * 0.088  # Adjust this value as needed
                if duration:
                    co2_emission_saved =  total_emissions[appliance]   - new_co2_emission
                    st.write(f"CO2 emission savings for {appliance}: {co2_emission_saved} kg")
                    total_new_co2_emission += co2_emission_saved
        # Repeat this pattern for each appliance
        elif appliance == "Fan":
            st.subheader(appliance)
            did_not_use_fan = st.checkbox("Did not use Fan", key=f"{appliance}_checkbox9")
            if did_not_use_fan:
                duration = st.number_input("Duration (hours)", key=f"{appliance}_duration", value=0.0, min_value=0.0, step=0.25, max_value=usage_hours[appliance])
                new_co2_emission = duration * 0.075  # Adjust this value as needed
                if duration:
                    co2_emission_saved =  total_emissions[appliance]   - new_co2_emission
                    st.write(f"CO2 emission savings for {appliance}: {co2_emission_saved} kg")
                    total_new_co2_emission += co2_emission_saved
        elif appliance == "Dryer":
            st.subheader(appliance)
            did_not_use_dryer = st.checkbox("Did not use Dryer", key=f"{appliance}_checkbox10")
            if did_not_use_dryer:
                duration = st.number_input("Duration (hours)", key=f"{appliance}_duration", value=0.0, min_value=0.0, step=0.25, max_value=usage_hours[appliance])
                new_co2_emission = duration * 1.0  # Adjust this value as needed
                if duration:
                    co2_emission_saved =  total_emissions[appliance]   - new_co2_emission
                    st.write(f"CO2 emission savings for {appliance}: {co2_emission_saved} kg")
                    total_new_co2_emission += co2_emission_saved

        # Add more appliances here
        # For example:
        elif appliance == "Coffee Maker":
            st.subheader(appliance)
            did_not_use_coffee_maker = st.checkbox("Did not use Coffee Maker", key=f"{appliance}_checkbox11")
            if did_not_use_coffee_maker:
                duration = st.number_input("Duration (hours)", key=f"{appliance}_duration", value=0.0, min_value=0.0, step=0.25, max_value=usage_hours[appliance])
                new_co2_emission = duration * 0.075  # Adjust this value as needed
                if duration:
                    co2_emission_saved =  total_emissions[appliance]   - new_co2_emission
                    st.write(f"CO2 emission savings for {appliance}: {co2_emission_saved} kg")
                    total_new_co2_emission += co2_emission_saved

        elif appliance == "Blender":
            st.subheader(appliance)
            did_not_use_blender = st.checkbox("Did not use Blender", key=f"{appliance}_checkbox12")
            if did_not_use_blender:
                duration = st.number_input("Duration (hours)", key=f"{appliance}_duration", value=0.0, min_value=0.0, step=0.25, max_value=usage_hours[appliance])
                new_co2_emission = duration * 0.075  # Adjust this value as needed
                if duration:
                    co2_emission_saved =  total_emissions[appliance]   - new_co2_emission
                    st.write(f"CO2 emission savings for {appliance}: {co2_emission_saved} kg")
                    total_new_co2_emission += co2_emission_saved
        elif appliance == "Vacuum Cleaner":
            st.subheader(appliance)
            did_not_use_vacuum_cleaner = st.checkbox("Did not use Vacuum Cleaner", key=f"{appliance}_checkbox13")
            if did_not_use_vacuum_cleaner:
                duration = st.number_input("Duration (hours)", key=f"{appliance}_duration", value=0.0, min_value=0.0, step=0.25, max_value=usage_hours[appliance])
                new_co2_emission = duration * 0.15  # Adjust this value as needed
                if duration:
                    co2_emission_saved =  total_emissions[appliance]   - new_co2_emission
                    st.write(f"CO2 emission savings for {appliance}: {co2_emission_saved} kg")
                    total_new_co2_emission += co2_emission_saved

        elif appliance == "Iron":
            st.subheader(appliance)
            did_not_use_iron = st.checkbox("Did not use Iron", key=f"{appliance}_checkbox14")
            if did_not_use_iron:
                duration = st.number_input("Duration (hours)", key=f"{appliance}_duration", value=0.0, min_value=0.0, step=0.25, max_value=usage_hours[appliance])
                new_co2_emission = duration * 0.1  # Adjust this value as needed
            
                if duration:
                    co2_emission_saved =  total_emissions[appliance]   - new_co2_emission
                    st.write(f"CO2 emission savings for {appliance}: {co2_emission_saved} kg")
                    total_new_co2_emission += co2_emission_saved

        elif appliance == "Hairdryer":
            st.subheader(appliance)
            did_not_use_hairdryer = st.checkbox("Did not use Hairdryer", key=f"{appliance}_checkbox15")
            if did_not_use_hairdryer:
                duration = st.number_input("Duration (hours)", key=f"{appliance}_duration", value=0.0, min_value=0.0, step=0.25, max_value=usage_hours[appliance])
                new_co2_emission = duration * 0.15  # Adjust this value as needed
                if duration:
                    co2_emission_saved =  total_emissions[appliance]   - new_co2_emission
                    st.write(f"CO2 emission savings for {appliance}: {co2_emission_saved} kg")
                    total_new_co2_emission += co2_emission_saved

        elif appliance == "Toaster":
            st.subheader(appliance)
            did_not_use_toaster = st.checkbox("Did not use Toaster", key=f"{appliance}_checkbox16")
            if did_not_use_toaster:
                duration = st.number_input("Duration (hours)", key=f"{appliance}_duration", value=0.0, min_value=0.0, step=0.25, max_value=usage_hours[appliance])
                new_co2_emission = duration * 0.075  # Adjust this value as needed
                if duration:
                    co2_emission_saved =  total_emissions[appliance]   - new_co2_emission
                    st.write(f"CO2 emission savings for {appliance}: {co2_emission_saved} kg")
                    total_new_co2_emission += co2_emission_saved

        elif appliance == "Electric Kettle":
            st.subheader(appliance)
            did_not_use_electric_kettle = st.checkbox("Did not use Electric Kettle", key=f"{appliance}_checkbox17")
            if did_not_use_electric_kettle:
                duration = st.number_input("Duration (hours)", key=f"{appliance}_duration", value=0.0, min_value=0.0, step=0.25, max_value=usage_hours[appliance])
                new_co2_emission = duration * 0.1  # Adjust this value as needed
                if duration:
                    co2_emission_saved =  total_emissions[appliance]   - new_co2_emission
                    st.write(f"CO2 emission savings for {appliance}: {co2_emission_saved} kg")
                    total_new_co2_emission += co2_emission_saved

        elif appliance == "Microwave":
            st.subheader(appliance)
            did_not_use_microwave = st.checkbox("Did not use Microwave", key=f"{appliance}_checkbox18")
            if did_not_use_microwave:
                duration = st.number_input("Duration (hours)", key=f"{appliance}_duration", value=0.0, min_value=0.0, step=0.25, max_value=usage_hours[appliance])
                new_co2_emission = duration * 0.15  # Adjust this value as needed
                if duration:
                    co2_emission_saved =  total_emissions[appliance]   - new_co2_emission
                    st.write(f"CO2 emission savings for {appliance}: {co2_emission_saved} kg")
                    total_new_co2_emission += co2_emission_saved

        elif appliance == "Water Heater":
            st.subheader(appliance)
            use_less_hot_water = st.checkbox("Use less hot water", key=f"{appliance}_checkbox19")
            if use_less_hot_water:
                duration = st.number_input("Duration (hours)", key=f"{appliance}_duration", value=0.0, min_value=0.0, step=0.25, max_value=usage_hours[appliance])
                new_co2_emission = duration * 0.5  # Adjust this value as needed
                if duration:
                    co2_emission_saved =  total_emissions[appliance]   - new_co2_emission
                    st.write(f"CO2 emission savings for {appliance}: {co2_emission_saved} kg")
                    total_new_co2_emission += co2_emission_saved

        elif appliance == "Incandescent Light":
            st.subheader(appliance)
            did_not_use_incandescent_light = st.checkbox("Did not use Incandescent Light", key=f"{appliance}_checkbox20")
            if did_not_use_incandescent_light:
                duration = st.number_input("Duration (hours)", key=f"{appliance}_duration", value=0.0, min_value=0.0, step=0.25, max_value=usage_hours[appliance])
                new_co2_emission = duration * 0.05  # Adjust this value as needed
                if duration:
                    co2_emission_saved =  total_emissions[appliance]   - new_co2_emission
                    st.write(f"CO2 emission savings for {appliance}: {co2_emission_saved} kg")
                    total_new_co2_emission += co2_emission_saved
        elif appliance == "Dishwasher":
            st.subheader(appliance)
            did_not_use_dishwasher = st.checkbox("Did not use Dishwasher", key=f"{appliance}_checkbox23")
            did_not_use_power_dry = st.checkbox("Did not use Power Dry", key=f"{appliance}_checkbox24")
            if did_not_use_dishwasher or did_not_use_power_dry:
                duration = st.number_input("Duration (hours)", key=f"{appliance}_duration", value=0.0, min_value=0.0, step=0.25, max_value=usage_hours[appliance])
                new_co2_emission = duration * 0.7  # Adjust this value as needed
                if duration:
                    co2_emission_saved =  total_emissions[appliance]   - new_co2_emission
                    st.write(f"CO2 emission savings for {appliance}: {co2_emission_saved} kg")
                    total_new_co2_emission += co2_emission_saved

        elif appliance == "Oven/Stove":
            st.subheader(appliance)
            did_not_use_oven_stove = st.checkbox("Did not use Oven/Stove", key=f"{appliance}_checkbox25")
            if did_not_use_oven_stove:
                duration = st.number_input("Duration (hours)", key=f"{appliance}_duration", value=0.0, min_value=0.0, step=0.25, max_value=usage_hours[appliance])
                new_co2_emission = duration * 0.3  # Adjust this value as needed
                if duration:
                    co2_emission_saved =  total_emissions[appliance]   - new_co2_emission
                    st.write(f"CO2 emission savings for {appliance}: {co2_emission_saved} kg")
                    total_new_co2_emission += co2_emission_saved
        elif appliance == "Refrigerator":
            st.subheader(appliance)
            did_not_use_refrigerator = st.checkbox("Did not use Refrigerator", key=f"{appliance}_checkbox27")
            if did_not_use_refrigerator:
                duration = st.number_input("Duration (hours)", key=f"{appliance}_duration", value=0.0, min_value=0.0, step=0.25, max_value=usage_hours[appliance])
                new_co2_emission = duration * 0.22  # Adjust this value as needed
                if duration:
                    co2_emission_saved =  total_emissions[appliance]   - new_co2_emission
                    st.write(f"CO2 emission savings for {appliance}: {co2_emission_saved} kg")
                    total_new_co2_emission += co2_emission_saved
        elif appliance == "Washing Machine":
            st.subheader(appliance)
            did_not_use_washing_machine = st.checkbox("Did not use Washing Machine", key=f"{appliance}_checkbox30")
            if did_not_use_washing_machine:
                duration = st.number_input("Duration (hours)", key=f"{appliance}_duration", value=0.0, min_value=0.0, step=0.25, max_value=usage_hours[appliance])
                new_co2_emission = duration * 0.75  # Adjust this value as needed
                if duration:
                    co2_emission_saved =  total_emissions[appliance]   - new_co2_emission
                    st.write(f"CO2 emission savings for {appliance}: {co2_emission_saved} kg")
                    total_new_co2_emission += co2_emission_saved

        elif appliance == "Computer/Laptop":
            st.subheader(appliance)
            did_not_use_computer_laptop = st.checkbox("Did not use Computer/Laptop", key=f"{appliance}_checkbox31")
            if did_not_use_computer_laptop:
                duration = st.number_input("Duration (hours)", key=f"{appliance}_duration", value=0.0, min_value=0.0, step=0.25, max_value=usage_hours[appliance])
                new_co2_emission = duration * 0.015  # Adjust this value as needed
                if duration:
                    co2_emission_saved =  total_emissions[appliance]   - new_co2_emission
                    st.write(f"CO2 emission savings for {appliance}: {co2_emission_saved} kg")
                    total_new_co2_emission += co2_emission_saved
        return co2_emission_saved        

# Run the app
if __name__ == "__main__":
    main()
