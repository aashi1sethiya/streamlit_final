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

def calculate_total_co2(meals, grasp_meals_left, grasp_meals_right, data):
    total_co2 = 0
    for i, meal in enumerate(meals):
        grasp_meals = grasp_meals_left if i % 2 == 0 else grasp_meals_right
        total_co2 += data[meal]["co2_per_serving"] * grasp_meals[meal] / 250  # Adjusted calculation
    return round(total_co2, 2)

def display_co2_text(meal, choice, grasp_meals_left, grasp_meals_right, data):
    if choice != "Select your dish":
        grasp_meals = grasp_meals_left if meal in grasp_meals_left else grasp_meals_right
        co2_per_serving = data[choice]["co2_per_serving"]
        co2_emission = co2_per_serving * grasp_meals[meal] / 250  # Adjusted calculation
        

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

# Main page
st.write("# Food CO2 Emissions + Macros Tracker")

# Sidebar
col1, col2, col3 = st.columns([3, 1, 1])  # Divide the space into three columns
with col1:
    st.subheader("Select your meal")
    meals = st.multiselect("Select Meals", list(data.keys()), default=[])

# Create two separate dictionaries to hold the slider values for each column
grasp_meals_left = {} 
grasp_meals_right = {}

# Loop over the meals and assign sliders to left and right columns based on index
for i, meal in enumerate(meals):
    if i % 2 == 0:  # Display in the left column for even indices
        grasp_meals_left[meal] = col2.slider(f"How much {meal}? (grams)", min_value=0, max_value=250, value=125, step=25, key=f"{meal}_slider_left")
    else:  # Display in the right column for odd indices
        grasp_meals_right[meal] = col3.slider(f"How much did you eat for {meal}? (grams)", min_value=0, max_value=250, value=125, step=25, key=f"{meal}_slider_right")

# Calculate total CO2 emission
total_emission = calculate_total_co2(meals, grasp_meals_left, grasp_meals_right, data)

# Displaying the CO2 Emission per Meal section
col1, col2 = st.columns([2, 1])
with col2:
    if meals:
        st.subheader("CO2 Emissions (kg)")
        for meal, choice in zip(meals, meals):
            display_co2_text(meal, choice, grasp_meals_left, grasp_meals_right, data)
            
    # Metrics columns
    metrics_col1, metrics_col2 = st.columns(2)
    for i, (meal, choice) in enumerate(zip(meals, meals)):
        if choice != "Select your dish":
            grasp_meals = grasp_meals_left if i % 2 == 0 else grasp_meals_right
            co2_emission = data[choice]["co2_per_serving"] * grasp_meals[meal] / 250
            if i % 2 == 0:
                with metrics_col1:
                    st.metric(label=meal, value=round(co2_emission, 2))
            else:
                with metrics_col2:
                    st.metric(label=meal, value=round(co2_emission, 2))

# Display total CO2 emission gauge
with  col1:
    if meals:
        st.write("### Total CO2 Emission Gauge")
        st_echarts(options=draw_gauge_chart(total_emission), height="300px")

# Display individual meal macros
if meals:
    st.write("### Individual Meal Macros:")
    selected_meals = [choice for choice in meals if choice != "Select your dish"]
    num_columns = min(len(selected_meals), 4)  # Limit the number of columns to 4
    num_rows = len(selected_meals) // num_columns + (1 if len(selected_meals) % num_columns != 0 else 0)
    columns = st.columns(num_columns)

    for i, meal in enumerate(selected_meals):
        if meal in data:  # Check if the meal is present in the data dictionary
            choice = meal
            grasp_meals = grasp_meals_left if meal in grasp_meals_left else grasp_meals_right
            total_energy = (data[choice]["energy_kcal"] * grasp_meals[meal]) / 250
            total_carbs = (data[choice]["carbs"] * grasp_meals[meal]) / 250
            total_fats = (data[choice]["fats"] * grasp_meals[meal]) / 250
            total_proteins = (data[choice]["proteins"] * grasp_meals[meal]) / 250
            with columns[i % num_columns]:
                st.subheader(f"{choice}")
                st.write(f"**Total Energy (kcal):** {total_energy:.2f}")
                st.bar_chart({"Carbs": total_carbs, "Fats": total_fats, "Proteins": total_proteins})
        else:
            st.write(f"No data available for {meal}")