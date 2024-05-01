import streamlit as st
import pandas as pd
import plotly.graph_objs as go

# Load the dataset
appliances_data = {
    "Appliance": ["Refrigerator", "Television", "Computer/Laptop", "Washing Machine", "Dryer",
                  "Dishwasher", "Oven/Stove", "Microwave", "Toaster", "Electric Kettle",
                  "Coffee Maker", "Blender", "Vacuum Cleaner", "Iron", "Hairdryer",
                  "Air Conditioner", "Heater", "Fan", "LED Light", "Incandescent Light", "Water Heater"],
    "CO2_Emission_kg": [0.5, 0.1, 0.015, 0.75, 1, 0.7, 0.3, 0.2, 0.1, 0.1, 0.075, 0.075, 0.15, 0.1, 0.15,
                        1.25, 1.25, 0.075, 0.0075, 0.05, 1.5]
}

appliances_df = pd.DataFrame(appliances_data)

# Main function to run the Streamlit app
def main():
    st.title("Household Appliance CO2 Emissions Calculator")
    
    col1, col2 = st.columns([2,1])

    with col1:
        st.subheader('Select your Daily Appliance Usage')
        # Multi-select for selecting appliances
        selected_appliances = st.multiselect("Select Appliances", appliances_df["Appliance"])
        
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
        with st.expander('Viz for your Appliance usage'):
                # Calculate total CO2 emissions for selected appliances
                total_emissions = {}
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
        with st.expander("Appliance Savings"):
            st.subheader("Save Co2 emissions")
            savings = {}
            for appliance in selected_appliances:
                st.subheader(f"{appliance}")
                off_hours = st.number_input(f"Hours {appliance} switched off", min_value=0.0, step=0.25)
                temp_adjustment = st.number_input(f"Temperature adjustment for {appliance}", min_value=-10, max_value=10, step=1)
                cycle_reduction = st.number_input(f"Washing cycle reduction for {appliance}", min_value=0, max_value=5, step=1)
                
                # Calculate CO2 emission savings for the appliance
                savings[appliance] = appliances_df.loc[appliances_df['Appliance'] == appliance, 'CO2_Emission_kg'].values[0] * (
                    off_hours + temp_adjustment * 0.05 + cycle_reduction * 0.025
                )


# Run the app
if __name__ == "__main__":
    main()
