import streamlit as st

total_emissions_all_tabs = 0

with st.sidebar:
    st.title("Options to Reduce CO2 Emissions")

    # Option 1: Highlight Low-Impact Foods
    st.header("Highlight Low-Impact Foods")
    low_impact_foods = st.multiselect(
        "Select Low-Impact Foods",
        ["Fruits", "Vegetables", "Legumes", "Grains"],
        help="Select low-impact foods to reduce CO2 emissions."
    )
    # Calculate CO2 emissions saved based on low-impact food choices
    low_impact_emissions = len(low_impact_foods) * 0.1  # Assuming each low-impact food saves 0.1 kg CO2 emissions
    total_emissions_all_tabs -= low_impact_emissions  # Subtract emissions saved

    # Option 2: Emphasize Local and Seasonal
    st.header("Emphasize Local and Seasonal")
    local_seasonal = st.checkbox(
        "Choose Local and Seasonal Foods",
        help="Select to reduce CO2 emissions by choosing locally produced and seasonal foods."
    )
    if local_seasonal:
        # Calculate CO2 emissions saved for choosing local and seasonal foods
        local_seasonal_emissions = 0.5  # Assuming choosing local and seasonal foods saves 0.5 kg CO2 emissions
        total_emissions_all_tabs -= local_seasonal_emissions  # Subtract emissions saved

    # Option 3: Promote Sustainable Farming Practices
    st.header("Promote Sustainable Farming Practices")
    st.write("Learn about organic farming, agroforestry, and regenerative agriculture to reduce CO2 emissions.")

    # Option 4: Reduce Food Waste
    st.header("Reduce Food Waste")
    st.write("Reduce food waste by meal planning, proper storage, and utilizing leftovers creatively.")

    # Option 5: Choose Energy-Efficient Cooking Methods
    st.header("Choose Energy-Efficient Cooking Methods")
    st.write("Use energy-efficient cooking methods like steaming, stir-frying, or pressure cooking.")

    # Option 6: Opt for Packaging-Free Options
    st.header("Opt for Packaging-Free Options")
    st.write("Choose products with minimal or recyclable packaging, or buy in bulk to reduce packaging waste.")

    # Option 7: Encourage Plant-Based Meals
    st.header("Encourage Plant-Based Meals")
    plant_based = st.checkbox(
        "Incorporate Plant-Based Meals",
        help="Select to reduce CO2 emissions by incorporating plant-based meals."
    )
    if plant_based:
        # Calculate CO2 emissions saved for incorporating plant-based meals
        plant_based_emissions = 1.0  # Assuming incorporating plant-based meals saves 1.0 kg CO2 emissions
        total_emissions_all_tabs -= plant_based_emissions  # Subtract emissions saved


with st.header("Food CO2 Emissions + Macros"):
    # Your existing code for food CO2 emissions and macros goes here

    # Display total CO2 emissions saved
    st.write(f"Total CO2 emissions saved: {total_emissions_all_tabs:.2f} kg")
