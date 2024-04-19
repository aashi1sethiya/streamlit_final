import streamlit as st

# Title
st.title("Meal Tracker and Carbon Footprint Calculator")

# Sidebar
st.sidebar.title("Meal Selection")

# Main Page Content
st.write("Welcome to the Meal Tracker and Carbon Footprint Calculator App!")

# Updated dataset for macros per 250 grams
macros_data_per_250g = {
    "Eggs": {"energy_kcal": 388, "carbs": 2.5, "fats": 27.5, "proteins": 32.5},
    "Cereal": {"energy_kcal": 500, "carbs": 112.5, "fats": 5, "proteins": 12.5},
    "Toast": {"energy_kcal": 200, "carbs": 37.5, "fats": 2.5, "proteins": 7.5},
    "Oatmeal": {"energy_kcal": 375, "carbs": 67.5, "fats": 5, "proteins": 12.5},
    "Sandwich": {"energy_kcal": 700, "carbs": 80, "fats": 37.5, "proteins": 50},
    "Salad": {"energy_kcal": 400, "carbs": 20, "fats": 30, "proteins": 20},
    "Soup": {"energy_kcal": 300, "carbs": 50, "fats": 12.5, "proteins": 25},
    "Pasta": {"energy_kcal": 600, "carbs": 100, "fats": 20, "proteins": 37.5},
    "Chicken": {"energy_kcal": 500, "carbs": 0, "fats": 20, "proteins": 75},
    "Steak": {"energy_kcal": 700, "carbs": 0, "fats": 40, "proteins": 62.5},
    "Fish": {"energy_kcal": 400, "carbs": 0, "fats": 16, "proteins": 62.5},
    "Vegetables": {"energy_kcal": 200, "carbs": 50, "fats": 5, "proteins": 12.5}
}

# User Input
with st.sidebar.expander("Breakfast"):
    breakfast_choice = st.selectbox("Select Breakfast", options=["Select your dish"] + list(macros_data_per_250g.keys()), index=0)

    if breakfast_choice != "Select your dish":
        grasp_breakfast = st.slider("How much did you eat? (grams)", min_value=0, max_value=250, value=125, step=25, key="breakfast_slider")

with st.sidebar.expander("Lunch"):
    lunch_choice = st.selectbox("Select Lunch", options=["Select your dish"] + list(macros_data_per_250g.keys()), index=0)

    if lunch_choice != "Select your dish":
        grasp_lunch = st.slider("How much did you eat? (grams)", min_value=0, max_value=250, value=125, step=25, key="lunch_slider")

with st.sidebar.expander("Dinner"):
    dinner_choice = st.selectbox("Select Dinner", options=["Select your dish"] + list(macros_data_per_250g.keys()), index=0)

    if dinner_choice != "Select your dish":
        grasp_dinner = st.slider("How much did you eat? (grams)", min_value=0, max_value=250, value=125, step=25, key="dinner_slider")

# Display meal and selected dish
def display_meal(meal, dish):
    st.write(f"{meal}: {dish}")

# Calculate Macros and Visualizations
# For simplicity, let's just calculate total macros for each meal and display them as text for now

if breakfast_choice != "Select your dish":
    total_energy_kcal_breakfast = (macros_data_per_250g[breakfast_choice]["energy_kcal"] * grasp_breakfast) / 250
    total_carbs_breakfast = (macros_data_per_250g[breakfast_choice]["carbs"] * grasp_breakfast) / 250
    total_fats_breakfast = (macros_data_per_250g[breakfast_choice]["fats"] * grasp_breakfast) / 250
    total_proteins_breakfast = (macros_data_per_250g[breakfast_choice]["proteins"] * grasp_breakfast) / 250

    display_meal("Breakfast", breakfast_choice)
    st.write("Total Energy (kcal):", total_energy_kcal_breakfast)
    st.write("Total Carbs (g):", total_carbs_breakfast)
    st.write("Total Fats (g):", total_fats_breakfast)
    st.write("Total Proteins (g):", total_proteins_breakfast)

if lunch_choice != "Select your dish":
    total_energy_kcal_lunch = (macros_data_per_250g[lunch_choice]["energy_kcal"] * grasp_lunch) / 250
    total_carbs_lunch = (macros_data_per_250g[lunch_choice]["carbs"] * grasp_lunch) / 250
    total_fats_lunch = (macros_data_per_250g[lunch_choice]["fats"] * grasp_lunch) / 250
    total_proteins_lunch = (macros_data_per_250g[lunch_choice]["proteins"] * grasp_lunch) / 250

    display_meal("Lunch", lunch_choice)
    st.write("Total Energy (kcal):", total_energy_kcal_lunch)
    st.write("Total Carbs (g):", total_carbs_lunch)
    st.write("Total Fats (g):", total_fats_lunch)
    st.write("Total Proteins (g):", total_proteins_lunch)

if dinner_choice != "Select your dish":
    total_energy_kcal_dinner = (macros_data_per_250g[dinner_choice]["energy_kcal"] * grasp_dinner) / 250
    total_carbs_dinner = (macros_data_per_250g[dinner_choice]["carbs"] * grasp_dinner) / 250
    total_fats_dinner = (macros_data_per_250g[dinner_choice]["fats"] * grasp_dinner) / 250
    total_proteins_dinner = (macros_data_per_250g[dinner_choice]["proteins"] * grasp_dinner) / 250

    display_meal("Dinner", dinner_choice)
    st.write("Total Energy (kcal):", total_energy_kcal_dinner)
    st.write("Total Carbs (g):", total_carbs_dinner)
    st.write("Total Fats (g):", total_fats_dinner)
    st.write("Total Proteins (g):", total_proteins_dinner)
