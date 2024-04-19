import streamlit as st
from streamlit_echarts import st_echarts

def draw_gauge_chart(total_emission):
    option = {
        "series": [
            {
                "type": "gauge",
                "startAngle": 180,
                "endAngle": 0,
                "center": ["50%", "75%"],
                "radius": "90%",
                "min": 0,
                "max": 4,  # Adjust maximum value to accommodate CO2 emissions per meal
                "splitNumber": 4,  # Adjust splitNumber as needed
                "axisLine": {
                    "lineStyle": {
                        "width": 6,
                        "color": [
                            [0.25, '#7CFFB2'],  # Reversed color
                            [0.5, '#58D9F9'],   # Reversed color
                            [0.75, '#FDDD60'],  # Reversed color
                            [1, '#FF6E76']      # Reversed color
                        ]
                    }
                },
                "pointer": {
                    "icon": "path://M12.8,0.7l12,40.1H0.7L12.8,0.7z",
                    "length": "12%",
                    "width": 20,
                    "offsetCenter": [0, "-60%"],
                    "itemStyle": {
                        "color": "auto"
                    }
                },
                "axisTick": {
                    "length": 12,
                    "lineStyle": {
                        "color": "auto",
                        "width": 2
                    }
                },
                "splitLine": {
                    "length": 20,
                    "lineStyle": {
                        "color": "auto",
                        "width": 5
                    }
                },
                "axisLabel": {
                    "color": "#464646",
                    "fontSize": 20,
                    "distance": -60,
                    "rotate": "tangential",
                },
                "title": {
                    "offsetCenter": [0, "-10%"],
                    "fontSize": 20
                },
                "detail": {
                    "fontSize": 30,
                    "offsetCenter": [0, "-35%"],
                    "valueAnimation": True,
                    "color": "inherit"
                },
                "data": [
                    {
                        "value": total_emission,  # Use total CO2 emission value here
                        "name": "CO2 Emissions"
                    }
                ]
            }
        ]
    }
    return option


# Title
st.title("Meal Tracker and Carbon Footprint Calculator")

# Sidebar
st.sidebar.title("Meal Selection")

# Updated dataset for macros per 250 grams and CO2 emissions per serving
data = {
    "Eggs": {"energy_kcal": 388, "carbs": 2.5, "fats": 27.5, "proteins": 32.5, "co2_per_serving": 0.2},
    "Cereal": {"energy_kcal": 500, "carbs": 112.5, "fats": 5, "proteins": 12.5, "co2_per_serving": 0.3},
    "Toast": {"energy_kcal": 200, "carbs": 37.5, "fats": 2.5, "proteins": 7.5, "co2_per_serving": 0.1},
    "Oatmeal": {"energy_kcal": 375, "carbs": 67.5, "fats": 5, "proteins": 12.5, "co2_per_serving": 0.25},
    "Sandwich": {"energy_kcal": 700, "carbs": 80, "fats": 37.5, "proteins": 50, "co2_per_serving": 0.4},
    "Salad": {"energy_kcal": 400, "carbs": 20, "fats": 30, "proteins": 20, "co2_per_serving": 0.15},
    "Soup": {"energy_kcal": 300, "carbs": 50, "fats": 12.5, "proteins": 25, "co2_per_serving": 0.2},
    "Pasta": {"energy_kcal": 600, "carbs": 100, "fats": 20, "proteins": 37.5, "co2_per_serving": 0.35},
    "Chicken": {"energy_kcal": 500, "carbs": 0, "fats": 20, "proteins": 75, "co2_per_serving": 0.45},
    "Steak": {"energy_kcal": 700, "carbs": 0, "fats": 40, "proteins": 62.5, "co2_per_serving": 0.6},
    "Fish": {"energy_kcal": 400, "carbs": 0, "fats": 16, "proteins": 62.5, "co2_per_serving": 0.5},
    "Vegetables": {"energy_kcal": 200, "carbs": 50, "fats": 5, "proteins": 12.5, "co2_per_serving": 0.1}
}

# User Input
with st.sidebar.expander("Breakfast"):
    breakfast_choice = st.selectbox("Select Breakfast", options=["Select your dish"] + list(data.keys()), index=0)

    if breakfast_choice != "Select your dish":
        grasp_breakfast = st.slider("How much did you eat? (grams)", min_value=0, max_value=250, value=125, step=25, key="breakfast_slider")

with st.sidebar.expander("Lunch"):
    lunch_choice = st.selectbox("Select Lunch", options=["Select your dish"] + list(data.keys()), index=0)

    if lunch_choice != "Select your dish":
        grasp_lunch = st.slider("How much did you eat? (grams)", min_value=0, max_value=250, value=125, step=25, key="lunch_slider")

with st.sidebar.expander("Dinner"):
    dinner_choice = st.selectbox("Select Dinner", options=["Select your dish"] + list(data.keys()), index=0)

    if dinner_choice != "Select your dish":
        grasp_dinner = st.slider("How much did you eat? (grams)", min_value=0, max_value=250, value=125, step=25, key="dinner_slider")

# Calculate CO2 emissions per serving for selected meals
def calculate_total_co2():
    total_co2 = 0
    if breakfast_choice != "Select your dish":
        total_co2 += data[breakfast_choice]["co2_per_serving"] * grasp_breakfast / 1000
    if lunch_choice != "Select your dish":
        total_co2 += data[lunch_choice]["co2_per_serving"] * grasp_lunch / 1000
    if dinner_choice != "Select your dish":
        total_co2 += data[dinner_choice]["co2_per_serving"] * grasp_dinner / 1000
    return total_co2

# Display macros for selected meals
def display_meal(meal, dish, total_energy, total_carbs, total_fats, total_proteins):
    st.subheader(f"{meal} - {dish}")

    st.write(f"**Total Energy (kcal) for {dish} {meal}:** {total_energy:.2f}")

    st.write(f"**Macros for {dish} {meal}:**")
    st.bar_chart({"Carbs": total_carbs, "Fats": total_fats, "Proteins": total_proteins})

# Calculate and display total CO2 emissions
total_emission = calculate_total_co2()

# Display total CO2 emission gauge chart
if breakfast_choice != "Select your dish" or lunch_choice != "Select your dish" or dinner_choice != "Select your dish":
    st.write("### Total CO2 Emission:")
    st_echarts(options=draw_gauge_chart(total_emission), height="300px")

# Display macros for selected meals side by side
if breakfast_choice != "Select your dish" or lunch_choice != "Select your dish" or dinner_choice != "Select your dish":
    st.write("### Individual Meal Macros:")
    col1, col2, col3 = st.columns(3)

if breakfast_choice != "Select your dish":
    total_energy_breakfast = (data[breakfast_choice]["energy_kcal"] * grasp_breakfast) / 250
    total_carbs_breakfast = (data[breakfast_choice]["carbs"] * grasp_breakfast) / 250
    total_fats_breakfast = (data[breakfast_choice]["fats"] * grasp_breakfast) / 250
    total_proteins_breakfast = (data[breakfast_choice]["proteins"] * grasp_breakfast) / 250

    with col1:
        display_meal("Breakfast", breakfast_choice, total_energy_breakfast, total_carbs_breakfast, total_fats_breakfast, total_proteins_breakfast)

if lunch_choice != "Select your dish":
    total_energy_lunch = (data[lunch_choice]["energy_kcal"] * grasp_lunch) / 250
    total_carbs_lunch = (data[lunch_choice]["carbs"] * grasp_lunch) / 250
    total_fats_lunch = (data[lunch_choice]["fats"] * grasp_lunch) / 250
    total_proteins_lunch = (data[lunch_choice]["proteins"] * grasp_lunch) / 250

    with col2:
        display_meal("Lunch", lunch_choice, total_energy_lunch, total_carbs_lunch, total_fats_lunch, total_proteins_lunch)

if dinner_choice != "Select your dish":
    total_energy_dinner = (data[dinner_choice]["energy_kcal"] * grasp_dinner) / 250
    total_carbs_dinner = (data[dinner_choice]["carbs"] * grasp_dinner) / 250
    total_fats_dinner = (data[dinner_choice]["fats"] * grasp_dinner) / 250
    total_proteins_dinner = (data[dinner_choice]["proteins"] * grasp_dinner) / 250

    with col3:
        display_meal("Dinner", dinner_choice, total_energy_dinner, total_carbs_dinner, total_fats_dinner, total_proteins_dinner)
