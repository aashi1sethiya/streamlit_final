import streamlit as st

# Function to collect CO2 emissions from commute tab
def commute_tab():
    st.write("Commute Tab")
    co2_emission_commute = st.number_input("Enter CO2 emissions from commute", value=0.0, step=0.1)
    return co2_emission_commute

# Function to collect CO2 emissions from food tab
def food_tab():
    st.write("Food Tab")
    co2_emission_food = st.number_input("Enter CO2 emissions from food", value=0.0, step=0.1)
    return co2_emission_food

# Main function
def main():
    # Collect CO2 emissions from commute tab
    total_emissions_placeholder = st.empty()
    total_emissions_placeholder.metric("Total CO2 Emissions", "Calculating...")

    tab1, tab2 = st.tabs(["Commute", "Food"])

    # Collect CO2 emissions from commute tab
    with tab1:
        commute_emission = commute_tab()

    # Collect CO2 emissions from food tab
    with tab2:
        food_emission = food_tab()

    # Calculate and display total CO2 emissions
    total_emissions = commute_emission + food_emission
    total_emissions_placeholder.metric("Total CO2 Emissions", total_emissions, "kgCO2e")

if __name__ == "__main__":
    main()



