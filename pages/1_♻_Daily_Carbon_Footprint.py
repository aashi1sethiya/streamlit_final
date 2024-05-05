import streamlit as st
from streamlit_echarts import st_echarts
import pandas as pd
import matplotlib.pyplot as plt
from pyecharts import options as opts
from pyecharts.charts import PictorialBar
import numpy as np
from PIL import Image
import plotly.graph_objs as go


st.set_page_config(layout="wide")
selected_low_impact_meals = []

# Main page
st.title("Daily Carbon Footprint Calculator")

col1, col2 = st.columns([1,1])

with col1:
    # Placeholder for total CO2 emissions metric label
    total_co2_metric_placeholder = st.empty()
with col2:
    co2_emissions_saved_placeholder = st.empty()

user_input_started = False

# Define a shared variable to accumulate total CO2 emissions
total_emissions_all_tabs = 0
co2_emissions_saved_all_tabs = 0
# Function to calculate CO2 emissions for selected commutes

def calculate_commute_co2(selected_commutes, commute_miles):
    co2_emissions = {
        "Car": 0.404,
        "Bicycle": 0.002,
        "Walking": 0.01,
        "Bus": 0.299,
        "Train": 0.177,
        "Motorcycle": 0.225,
        "Electric Vehicle": 0.05,
        "Carpool": 0.202
    }
    total_emissions = sum(commute_miles.get(commute, 0) * co2_emissions.get(commute, 0) for commute in selected_commutes)
    return total_emissions

# Function to calculate CO2 emissions for selected meals

def calculate_meal_co2(meals, grasp_meals_left, grasp_meals_right, data):
    total_co2 = 0
    for meal in meals:
        grasp_meals = grasp_meals_left if meals.index(meal) % 2 == 0 else grasp_meals_right
        total_co2 += data[meal]["co2_per_serving"] * grasp_meals[meal] / 250
    return total_co2

# Function to display CO2 emissions metric

def display_co2_metric(total_emissions):
    total_co2_metric_placeholder.metric(label="Total Co2 emissions (kg)", value=round(total_emissions, 2))

# Function to display CO2 emissions saved metric

def display_co2_saved_metric(co2_emissions_saved_all_tabs):
    co2_emissions_saved_placeholder.metric(label="CO2 Emissions Saved (kg)", value=round(co2_emissions_saved_all_tabs, 2))


# Track whether any user input has been made using Streamlit's session state
if "user_input_started" not in st.session_state:
    st.session_state.user_input_started = False


tab1, tab2, tab3 = st.tabs(["Commute", "Food", "Appliances"])

with tab1:
    total_emissions_tab1 = 0
    new_commute_miles = {}
    
    def generate_graph(commute_data, bar_overlap, opacity):
        # Sort commute data by CO2 emissions in descending order
        sorted_data = sorted(commute_data.items(), key=lambda x: x[1], reverse=True)

        # Calculate the maximum value for scaling
        max_value = max(commute_data.values())

        # Define SVG attributes
        max_commutes = max(len(commute_data), 7)  # Minimum number of commute options to ensure proper scaling
        min_svg_width = 500  # Minimum width for the graph
        svg_width = max(min_svg_width, max_commutes * 60)  # Adjusted width to take 2/3 of the page or minimum width
        svg_height = max(300, max_value * 7)  # Increased height
        bar_width = svg_width / len(commute_data)
        bar_height_ratio = svg_height / max_value
        bar_bottom_margin = 35  # Larger margin for the bottom labels
        bar_top_margin = 10  # Margin for the top labels
        y_label_margin = 35  # Margin for y-axis labels
        x_margin = 10  # Margin to separate bars from the y-axis

        # Define the symbol path
        symbol_path = 'M0,5 L5,5 C2.75,5 2.75,2.5 2.5,0 C2.25,2.5 2.25,5 0,5 Z'

        # Emoji codes for commute options with adjusted font size
        emoji_codes = {
            "Car": "🚗",
            "Bicycle": "🚲",
            "Walking": "🚶",
            "Motorcycle": "🏍️",
            "Electric Vehicle": "🔌",
            "Carpool": "🚗👥",
            "Bus": "🚌",
            "Train": "🚆"
        }

        # Generate SVG elements for each bar with emojis
        svg_elements = []
        bottom_labels = []
        for i, (category, value) in enumerate(sorted_data):
            x = i * (bar_width - bar_overlap) + x_margin
            y = svg_height - (value * bar_height_ratio)
            height = value * bar_height_ratio
            tooltip = f"{category}: {value:.2f}"  # Tooltip content
            emoji_code = emoji_codes.get(category, "")
            # Adjust font size of emoji
            svg_elements.append(f'<text x="{x + (bar_width - x_margin) / 2}" y="{svg_height + bar_bottom_margin}" font-size="25" text-anchor="middle">{emoji_code}</text>')
            svg_elements.append(f'<path d="{symbol_path}" transform="translate({x}, {y}) scale({(bar_width - x_margin)/5}, {height/5})" fill="#e54035" opacity="{opacity}"><title>{tooltip}</title></path>')

        # Generate SVG code
        svg_code = f'<svg width="{svg_width}" height="{svg_height + bar_bottom_margin + bar_top_margin}">' + ''.join(svg_elements) + '</svg>'

        # Display SVG in Streamlit
        st.write(svg_code, unsafe_allow_html=True)


    st.write("## Co2 Emissions for Commute")

    # Streamlit UI

    # Write "Add your daily commute" above the multi-select input
    st.subheader("Add your daily commute")

    # User Inputs
    commute_options = [
            "Car",
            "Bicycle",
            "Walking",
            "Motorcycle",
            "Electric Vehicle",
            "Carpool",
            "Bus",  
            "Train"
        ]

    # Splitting the layout into columns
    input_col1, input_col2, input_col3 = st.columns([3, 1, 1])
        
    # Multi-select input for commute options in the first column
    selected_commutes = input_col1.multiselect("# Select Commute Options", commute_options)
 
    # Inputs for miles traveled in the second and third columns

    commute_miles = {}
    for i, commute in enumerate(selected_commutes):
            if i % 2 == 0:
                col = input_col2
            else:
                col = input_col3
            commute_miles[commute] = col.number_input(f"{commute} miles", min_value=0.1, max_value=None, step=0.1, key=f"{commute}_miles_input", value=0.1)

    # Expander for user input, graphs, and other content related to tab 1
    with st.expander("My Daily Commute"):

        # Calculate CO2 emissions for selected commutes
        co2_emissions = {
            "Car": 0.404,
            "Bicycle": 0.002,
            "Walking": 0.01,
            "Motorcycle": 0.225,
            "Electric Vehicle": 0.05,
            "Carpool": 0.202,
            "Bus": 0.299,  # Buses are a common form of public transportation, often used for commuting or city travel.
            "Train": 0.177 # Trucks are typically used for transporting goods over long distances and are a significant source of CO2 emissions in the transportation sector.
        }

        co2_emissions_selected = {commute: commute_miles.get(commute, 0) * co2_emissions.get(commute, 0) for commute in selected_commutes}

        # Define the amount of overlap between bars
        bar_overlap = 20

        # Define opacity
        opacity = 0.6

        if co2_emissions_selected:
            col1, col2 = st.columns([3, 2])
            with col1:
                st.subheader("Co2 Emissions Graph")
                generate_graph(co2_emissions_selected, bar_overlap, opacity)
            
            with col2:
                # Calculate CO2 emissions for selected commutes
                co2_emissions_selected = {commute: commute_miles.get(commute, 0) * co2_emissions.get(commute, 0) for commute in selected_commutes}
                total_emissions_tab1 = sum(co2_emissions_selected.values())
                total_emissions_all_tabs += total_emissions_tab1
                # Display CO2 emissions metric if user input has started
                container = st.container(border= True)
                container.metric(label="Total Commute Co2 emissions (kg)", value=round(total_emissions_tab1, 2))
        if selected_commutes or st.session_state.user_input_started:
            display_co2_metric(total_emissions_all_tabs)
                


        # Function to generate the footprint bars
        def generate_footprint_bars(total_emissions_tab1, new_emission):
            # Calculate the height of the bars based on emissions
            actual_height = total_emissions_tab1  # scaling for visualization
            new_height = new_emission 

            # Load footprint image
            footprint_image = Image.open("footprint.png")

            # Plot footprint bars using the footprint image
            fig, ax = plt.subplots()

            # Plot actual emissions bar
            ax.imshow(footprint_image, aspect='auto', extent=(0, 1, 0, actual_height), alpha=0.7, cmap='viridis')
            ax.text(0.5, actual_height * 1 , f"{total_emissions_tab1:.2f}", ha='center', va='bottom', color='black',  fontsize=12)

            # Plot new emissions bar
            ax.imshow(footprint_image, aspect='auto', extent=(1.2, 2.2, 0, new_height), alpha=0.7, cmap='viridis')
            ax.text(1.7, new_height * 1, f"{new_emission:.2f}", ha='center', va='bottom', color='black',  fontsize=12)

            # Customize plot
            ax.set_ylabel('Co2 Emissions (kg)')
            ax.set_xticks([0.5, 1.7])
            ax.set_xticklabels(["Actual", "Predicted"])
            ax.set_xlim(0, 2.5)
            ax.set_ylim(0, max(actual_height, new_height) * 1.1)  # Set ylim to ensure all footprints are visible
            ax.grid(False)

            # Remove x-axis ticks
            ax.xaxis.set_ticks_position('none')

            # Remove y-axis ticks
            ax.yaxis.set_ticks_position('none')

            # Show plot
            st.pyplot(fig)

            # User Inputs for Tab 1
            total_emissions_tab1 = sum(co2_emissions_selected.values())
    
    st.subheader('')
    if selected_commutes:
        st.subheader('Add Commute for CO2 Savings Prediction')
        # Expander for user input for the new commute and CO2 emissions comparison
    if selected_commutes or st.session_state.user_input_started:
                    #  # Splitting the layout into columns
    # input_col1, input_col2, input_col3 = st.columns([3, 1, 1])
        
    # # Multi-select input for commute options in the first column
    # selected_commutes = input_col1.multiselect("# Select Commute Options", commute_options)

    # with st.expander('Miles of Commute'): 
    # # Inputs for miles traveled in the second and third columns
    #     commute_miles = {}
    #     for i, commute in enumerate(selected_commutes):
    #             if i % 2 == 0:
    #                 col = input_col2
    #             else:
    #                 col = input_col3
    #             commute_miles[commute] = col.number_input(f"{commute} miles", min_value=0.1, max_value=None, step=0.1, key=f"{commute}_miles_input", value=0.1)               
                with st.expander("Reduce Commute Carbon Footprint"):
                # Splitting the layout into columns
                    saved_col1, saved_col2, saved_col3 = st.columns([3, 1, 1])

                # User input for new commute - select box
                    
                    new_commutes = saved_col1.multiselect("Select New Commute Option", ["Car", "Bicycle", "Walking", "Bus", "Train", "Motorcycle", "Electric Vehicle", "Carpool"], key=None,placeholder="Please select an option", default=None)
                                                          
                    # User input for new commute - number input
                    for i, commute in enumerate(new_commutes):
                        if i % 2 == 0:
                            sav_col = saved_col2
                        else:
                            sav_col = saved_col3
                        new_commute_miles[commute] = sav_col.number_input(f"{commute} miles", min_value=0.1, max_value=None, step=0.1, key=f"Miles saved in {commute}", value=0.1)
                
                    # Calculate new emissions based on user input
                    if len(new_commutes) > 0:    
                        new_emission = {commute: new_commute_miles.get(commute, 0) * co2_emissions.get(commute, 0) for commute in new_commutes} # Actual emission rate for new commute
                        # Display CO2 emissions saved as metric
                        new_emission_values = sum(new_emission.values())
                        co2_emissions_saved = total_emissions_all_tabs - new_emission_values
                        co2_emissions_saved_all_tabs  += co2_emissions_saved
                        
                        if new_commutes:
                            st.subheader("Co2 Footprint Comparison")

                        col1, col2 = st.columns([3,1])
                        with col1:
                        # Generate and display the footprint bars
                            
                            generate_footprint_bars(total_emissions_tab1, new_emission_values)
                        
                        with col2:
                            container1 = st.container(border= True)
                            container1.metric(label="Co2 Emissions Saved", value=round(co2_emissions_saved, 2))
                            display_co2_saved_metric(co2_emissions_saved_all_tabs)                    
            
with tab2:
        
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
                total_co2 += data[meal]["co2_per_serving"] * grasp_meals[meal] / 1  # Adjusted calculation
            return round(total_co2, 2)

        def display_co2_text(meal, choice, grasp_meals_left, grasp_meals_right, data):
            if choice != "Select your dish":
                grasp_meals = grasp_meals_left if meal in grasp_meals_left else grasp_meals_right
                co2_per_serving = data[choice]["co2_per_serving"]
                co2_emission = co2_per_serving * grasp_meals[meal] / 1  # Adjusted calculation
        
                

        data = {
    "Eggs": {"energy_kcal": 388, "carbs": 2.5, "fats": 27.5, "proteins": 32.5, "co2_per_serving": 0.2},
    "Cereal": {"energy_kcal": 500, "carbs": 112.5, "fats": 5, "proteins": 12.5, "co2_per_serving": 0.03},
    "Milk": {"energy_kcal": 500, "carbs": 112.5, "fats": 5, "proteins": 12.5, "co2_per_serving": 0.32}, #
    "Tofu": {"energy_kcal": 500, "carbs": 112.5, "fats": 5, "proteins": 12.5, "co2_per_serving": 0.08}, #
    "Bread": {"energy_kcal": 200, "carbs": 37.5, "fats": 2.5, "proteins": 7.5, "co2_per_serving": 0.025},
    "Oatmeal": {"energy_kcal": 375, "carbs": 67.5, "fats": 5, "proteins": 12.5, "co2_per_serving": 0.047},
    "Veggie Sandwich": {"energy_kcal": 700, "carbs": 80, "fats": 37.5, "proteins": 50, "co2_per_serving": 0.4},
    "Salad Mix": {"energy_kcal": 400, "carbs": 20, "fats": 30, "proteins": 20, "co2_per_serving": 0.07},
    "Soup": {"energy_kcal": 300, "carbs": 50, "fats": 12.5, "proteins": 25, "co2_per_serving": 0.3},
    "Veg Pasta": {"energy_kcal": 600, "carbs": 100, "fats": 20, "proteins": 37.5, "co2_per_serving": 0.11},
    "Chicken": {"energy_kcal": 500, "carbs": 0, "fats": 20, "proteins": 75, "co2_per_serving": 1.82},
    "Fish": {"energy_kcal": 400, "carbs": 0, "fats": 16, "proteins": 62.5, "co2_per_serving": 1.34},
    "Root Vegetables": {"energy_kcal": 200, "carbs": 50, "fats": 5, "proteins": 12.5, "co2_per_serving": 0.04},
    "Beef": {"energy_kcal": 700, "carbs": 0, "fats": 45, "proteins": 60, "co2_per_serving": 15.5},
    "Pork": {"energy_kcal": 600, "carbs": 0, "fats": 30, "proteins": 70, "co2_per_serving": 2.44},
    "Lamb": {"energy_kcal": 600, "carbs": 0, "fats": 35, "proteins": 65, "co2_per_serving": 5.84},
    "Prawns": {"energy_kcal": 200, "carbs": 0, "fats": 5, "proteins": 30, "co2_per_serving": 4.07},
    "Crab": {"energy_kcal": 150, "carbs": 0, "fats": 2, "proteins": 20, "co2_per_serving": 1.77}, 
    "Cheese": {"energy_kcal": 150, "carbs": 0, "fats": 2, "proteins": 20, "co2_per_serving": 2.79}, #
    "Dark Chocolate": {"energy_kcal": 150, "carbs": 0, "fats": 2, "proteins": 20, "co2_per_serving": 0.95}, #
    "Rice": {"energy_kcal": 150, "carbs": 0, "fats": 2, "proteins": 20, "co2_per_serving": 0.16}, #
    "Berries": {"energy_kcal": 150, "carbs": 0, "fats": 2, "proteins": 20, "co2_per_serving": 0.22},#
    "Banana": {"energy_kcal": 150, "carbs": 0, "fats": 2, "proteins": 20, "co2_per_serving": 0.11}, #
    "Tomato": {"energy_kcal": 150, "carbs": 0, "fats": 2, "proteins": 20, "co2_per_serving": 0.06}, #
    "Orange/ Apple": {"energy_kcal": 150, "carbs": 0, "fats": 2, "proteins": 20, "co2_per_serving": 0.05}#
    }

        low_impact_food_data = {
            "Locally sourced Fruits": {"co2_per_serving": 0.05},  # Placeholder value
            "Locally sourced Vegetables": {"co2_per_serving": 0.08},  # Placeholder value
            "Legumes": {"co2_per_serving": 0.067},  # Placeholder value
            "Rice": {"co2_per_serving": 0.16},  # Placeholder value
            "Tofu": {"co2_per_serving": 0.08},  # Placeholder value
            "Milk": {"co2_per_serving": 0.32},  # Placeholder value
            "Eggs": {"co2_per_serving": 0.2},  # Placeholder value
            "Bread": {"co2_per_serving": 0.025},
            "Soup": {"co2_per_serving": 0.3},
            "Veg Pasta": {"co2_per_serving": 0.11}, # Placeholder value
            "Nuts": {"co2_per_serving": 0.014},
            "Salad Mix": {"co2_per_serving": 0.07},
            "Dark Chocolate": {"co2_per_serving": 0.95}
            }
        
        def calculate_total_co2_emission(selected_meals):
            total_emission = 0
            for meal in selected_meals:
                if meal in low_impact_food_data:
                    total_emission += low_impact_food_data[meal]["co2_per_serving"]
            return total_emission

        # Main page
        st.write("## Co2 Emissions for Food")

        # Sidebar
        col1, col2, col3 = st.columns([3, 1, 1])  # Divide the space into three columns
        with col1:
            st.subheader("Add your Daily Meal")
            meals = st.multiselect("Select Meals", list(data.keys()), default=None)

        # Create two separate dictionaries to hold the slider values for each column
        grasp_meals_left = {} 
        grasp_meals_right = {}

        # Loop over the meals and assign sliders to left and right columns based on index
        for i, meal in enumerate(meals):
            if i % 2 == 0:  # Display in the left column for even indices
                grasp_meals_left[meal] = col2.slider(f"{meal} (servings)", min_value=0.0, max_value=4.0, value=0.0, step=0.5, key=f"{meal}_slider_left")
            else:  # Display in the right column for odd indices
                grasp_meals_right[meal] = col3.slider(f"{meal} (servings)", min_value=0.0, max_value=4.0, value=0.0, step=0.5, key=f"{meal}_slider_right")

    
        # Calculate total CO2 emission
        total_emission = calculate_total_co2(meals, grasp_meals_left, grasp_meals_right, data)
        total_emissions_all_tabs += total_emission

        # Displaying the CO2 Emission per Meal section
        col1, col2 = st.columns([2, 1])
        with col2:
            if meals:
                st.subheader("Co2 Emissions (kg)")
                for meal, choice in zip(meals, meals):
                    display_co2_text(meal, choice, grasp_meals_left, grasp_meals_right, data)
                    
            # Metrics columns
                with st.expander("Individual Meals Co2 Emissions"):
                    metrics_col1, metrics_col2 = st.columns(2)
                    for i, (meal, choice) in enumerate(zip(meals, meals)):
                        if choice != "Select your dish":
                            grasp_meals = grasp_meals_left if i % 2 == 0 else grasp_meals_right
                            co2_emission = data[choice]["co2_per_serving"] * grasp_meals[meal] / 1
                            if i % 2 == 0:
                                with metrics_col1:
                                    st.metric(label=meal, value=round(co2_emission, 2))
                            else:
                                with metrics_col2:
                                    st.metric(label=meal, value=round(co2_emission, 2))
        
        
        def generate_footprint_bars(total_emission, total_emission_selected_meals):
            # Calculate the height of the bars based on emissions
            actual_height = total_emission  # scaling for visualization
            new_height = total_emission_selected_meals 

            # Load footprint image
            footprint_image = Image.open("footprint.png")

            # Plot footprint bars using the footprint image
            fig, ax = plt.subplots()

            # Plot actual emissions bar
            ax.imshow(footprint_image, aspect='auto', extent=(0, 1, 0, actual_height), alpha=0.7, cmap='viridis')
            ax.text(0.5, actual_height * 1, f"{total_emission:.2f}", ha='center', va='center', color='black', fontsize=12)

            # Plot new emissions bar
            ax.imshow(footprint_image, aspect='auto', extent=(1.2, 2.2, 0, new_height), alpha=0.7, cmap='viridis')
            ax.text(1.7, new_height * 1, f"{total_emission_selected_meals:.2f}", ha='center', va='center', color='black', fontsize=12)

            # Customize plot
            ax.set_ylabel('Co2 Emissions (kg)')
            ax.set_xticks([0.5, 1.7])
            ax.set_xticklabels(["Actual", "New"])
            ax.set_xlim(0, 2.5)
            ax.set_ylim(0, max(actual_height, new_height) * 1.1)  # Set ylim to ensure all footprints are visible
            ax.grid(False)

            # Remove x-axis ticks
            ax.xaxis.set_ticks_position('none')

            # Remove y-axis ticks
            ax.yaxis.set_ticks_position('none')

            # Show plot
            st.pyplot(fig)

        # Display total CO2 emission gauge
        with  col1:
            if meals:
                st.write("### Total CO2 Emission Gauge")
                st_echarts(options=draw_gauge_chart(total_emission), height="300px")

        if meals:
            with st.expander("Reduce Food Carbon Footprint"):
                selected_low_impact_meals = st.multiselect("Select Low-Impact Foods",
                list(low_impact_food_data.keys()), default=None,
                help="Select low-impact foods for your meals to reduce CO2 emissions.")
                if selected_low_impact_meals:
                        total_emission_selected_meals = calculate_total_co2_emission(selected_low_impact_meals)
                        co2_emissions_food_saved = total_emission - total_emission_selected_meals
                        co2_emissions_saved_all_tabs  += co2_emissions_food_saved
                        display_co2_saved_metric(co2_emissions_saved_all_tabs)
                        st.subheader('Co2 Footprint Comparison')
                col1, col2 = st.columns([2,1])
                with col1:
                    if selected_low_impact_meals:
                        generate_footprint_bars(total_emission, total_emission_selected_meals)
                with col2:
                    if selected_low_impact_meals:
                        container2 = st.container(border= True)
                        container2.metric(label="Total Co2 Emission saved", value=round(co2_emissions_food_saved,2))
                    
                

        # Display individual meal macros
        if meals:
            with st.expander("Individual Meal Macros"):
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

        if meals:
            display_co2_metric(total_emissions_all_tabs)
        if selected_low_impact_meals:
            display_co2_saved_metric(co2_emissions_saved_all_tabs)
 
if selected_commutes or meals:
    st.session_state.user_input_started = True


# Display CO2 emissions saved as metric

with tab3:
    global total_new_co2_emission_saved
    appliance_dictionary={}
    duration=0
    
    def create_container(appliance, usage_hours, total_emissions):
        with st.container(border=True, height=300):
            co2_emission_saved=0
            duration=0
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
                        rounded_co2_emission_saved = round(co2_emission_saved, 2)
                        st.write(f"CO2 emission savings for {appliance}: {rounded_co2_emission_saved} kg")
            elif appliance == "Air Conditioner":
                st.subheader(appliance)
                switched_off_ac = st.checkbox("Switched off AC", key=f"{appliance}_checkbox4")
                increased_temp_settings = st.checkbox("Increase temperature settings", key=f"{appliance}_checkbox5")
                if switched_off_ac or increased_temp_settings:
                    duration = st.number_input("Duration (hours)", key=f"{appliance}_duration", value=0.0, min_value=0.0, step=0.25, max_value=usage_hours[appliance])
                    temperature = st.number_input("Temperature (°C)", key=f"{appliance}_temperature", value=0, step=1)
                    new_co2_emission = duration * 1.25  # Adjust this value as needed
                    if duration:
                        co2_emission_saved =  total_emissions[appliance]   - new_co2_emission
                        rounded_co2_emission_saved = round(co2_emission_saved, 2)
                        st.write(f"CO2 emission savings for {appliance}: {rounded_co2_emission_saved} kg")
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
                        rounded_co2_emission_saved = round(co2_emission_saved, 2)
                        st.write(f"CO2 emission savings for {appliance}: {rounded_co2_emission_saved} kg")

            # Repeat this pattern for each appliance
            elif appliance == "Television":
                st.subheader(appliance)
                did_not_use_tv = st.checkbox("Did not use TV", key=f"{appliance}_checkbox8")
                if did_not_use_tv:
                    duration = st.number_input("Duration (hours)", key=f"{appliance}_duration", value=0.0, min_value=0.0, step=0.25, max_value=usage_hours[appliance])
                    new_co2_emission = duration * 0.088  # Adjust this value as needed
                    if duration:
                        co2_emission_saved =  total_emissions[appliance]   - new_co2_emission
                        rounded_co2_emission_saved = round(co2_emission_saved, 2)
                        st.write(f"CO2 emission savings for {appliance}: {rounded_co2_emission_saved} kg")
            # Repeat this pattern for each appliance
            elif appliance == "Fan":
                st.subheader(appliance)
                did_not_use_fan = st.checkbox("Did not use Fan", key=f"{appliance}_checkbox9")
                if did_not_use_fan:
                    duration = st.number_input("Duration (hours)", key=f"{appliance}_duration", value=0.0, min_value=0.0, step=0.25, max_value=usage_hours[appliance])
                    new_co2_emission = duration * 0.032  # Adjust this value as needed
                    if duration:
                        co2_emission_saved =  total_emissions[appliance]   - new_co2_emission
                        rounded_co2_emission_saved = round(co2_emission_saved, 2)
                        st.write(f"CO2 emission savings for {appliance}: {rounded_co2_emission_saved} kg")
    
            elif appliance == "Dryer":
                st.subheader(appliance)
                did_not_use_dryer = st.checkbox("Did not use Dryer", key=f"{appliance}_checkbox10")
                if did_not_use_dryer:
                    duration = st.number_input("Duration (hours)", key=f"{appliance}_duration", value=0.0, min_value=0.0, step=0.25, max_value=usage_hours[appliance])
                    new_co2_emission = duration * 1.0  # Adjust this value as needed
                    if duration:
                        co2_emission_saved =  total_emissions[appliance]   - new_co2_emission
                        rounded_co2_emission_saved = round(co2_emission_saved, 2)
                        st.write(f"CO2 emission savings for {appliance}: {rounded_co2_emission_saved} kg")

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
                        rounded_co2_emission_saved = round(co2_emission_saved, 2)
                        st.write(f"CO2 emission savings for {appliance}: {rounded_co2_emission_saved} kg")

            elif appliance == "Blender":
                st.subheader(appliance)
                did_not_use_blender = st.checkbox("Did not use Blender", key=f"{appliance}_checkbox12")
                if did_not_use_blender:
                    duration = st.number_input("Duration (hours)", key=f"{appliance}_duration", value=0.0, min_value=0.0, step=0.25, max_value=usage_hours[appliance])
                    new_co2_emission = duration * 0.075  # Adjust this value as needed
                    if duration:
                        co2_emission_saved =  total_emissions[appliance]   - new_co2_emission
                        rounded_co2_emission_saved = round(co2_emission_saved, 2)
                        st.write(f"CO2 emission savings for {appliance}: {rounded_co2_emission_saved} kg")
            elif appliance == "Vacuum Cleaner":
                st.subheader(appliance)
                did_not_use_vacuum_cleaner = st.checkbox("Did not use Vacuum Cleaner", key=f"{appliance}_checkbox13")
                if did_not_use_vacuum_cleaner:
                    duration = st.number_input("Duration (hours)", key=f"{appliance}_duration", value=0.0, min_value=0.0, step=0.25, max_value=usage_hours[appliance])
                    new_co2_emission = duration * 0.15  # Adjust this value as needed
                    if duration:
                        co2_emission_saved =  total_emissions[appliance]   - new_co2_emission
                        rounded_co2_emission_saved = round(co2_emission_saved, 2)
                        st.write(f"CO2 emission savings for {appliance}: {rounded_co2_emission_saved} kg")

            elif appliance == "Iron":
                st.subheader(appliance)
                did_not_use_iron = st.checkbox("Did not use Iron", key=f"{appliance}_checkbox14")
                if did_not_use_iron:
                    duration = st.number_input("Duration (hours)", key=f"{appliance}_duration", value=0.0, min_value=0.0, step=0.25, max_value=usage_hours[appliance])
                    new_co2_emission = duration * 0.1  # Adjust this value as needed
                
                    if duration:
                        co2_emission_saved =  total_emissions[appliance]   - new_co2_emission
                        rounded_co2_emission_saved = round(co2_emission_saved, 2)
                        st.write(f"CO2 emission savings for {appliance}: {rounded_co2_emission_saved} kg")

            elif appliance == "Hairdryer":
                st.subheader(appliance)
                did_not_use_hairdryer = st.checkbox("Did not use Hairdryer", key=f"{appliance}_checkbox15")
                if did_not_use_hairdryer:
                    duration = st.number_input("Duration (hours)", key=f"{appliance}_duration", value=0.0, min_value=0.0, step=0.25, max_value=usage_hours[appliance])
                    new_co2_emission = duration * 0.15  # Adjust this value as needed
                    if duration:
                        co2_emission_saved =  total_emissions[appliance]   - new_co2_emission
                        rounded_co2_emission_saved = round(co2_emission_saved, 2)
                        st.write(f"CO2 emission savings for {appliance}: {rounded_co2_emission_saved} kg")
            elif appliance == "Toaster":
                st.subheader(appliance)
                did_not_use_toaster = st.checkbox("Did not use Toaster", key=f"{appliance}_checkbox16")
                if did_not_use_toaster:
                    duration = st.number_input("Duration (hours)", key=f"{appliance}_duration", value=0.0, min_value=0.0, step=0.25, max_value=usage_hours[appliance])
                    new_co2_emission = duration * 0.1  # Adjust this value as needed
                    if duration:
                        co2_emission_saved =  total_emissions[appliance]   - new_co2_emission
                        rounded_co2_emission_saved = round(co2_emission_saved, 2)
                        st.write(f"CO2 emission savings for {appliance}: {rounded_co2_emission_saved} kg")

            elif appliance == "Electric Kettle":
                st.subheader(appliance)
                did_not_use_electric_kettle = st.checkbox("Did not use Electric Kettle", key=f"{appliance}_checkbox17")
                if did_not_use_electric_kettle:
                    duration = st.number_input("Duration (hours)", key=f"{appliance}_duration", value=0.0, min_value=0.0, step=0.25, max_value=usage_hours[appliance])
                    new_co2_emission = duration * 0.1  # Adjust this value as needed
                    if duration:
                        co2_emission_saved =  total_emissions[appliance]   - new_co2_emission
                        rounded_co2_emission_saved = round(co2_emission_saved, 2)
                        st.write(f"CO2 emission savings for {appliance}: {rounded_co2_emission_saved} kg")
                
            elif appliance == "Microwave":
                st.subheader(appliance)
                did_not_use_microwave = st.checkbox("Did not use Microwave", key=f"{appliance}_checkbox18")
                if did_not_use_microwave:
                    duration = st.number_input("Duration (hours)", key=f"{appliance}_duration", value=0.0, min_value=0.0, step=0.25, max_value=usage_hours[appliance])
                    new_co2_emission = duration * 0.2  # Adjust this value as needed
                    if duration:
                        co2_emission_saved =  total_emissions[appliance]   - new_co2_emission
                        rounded_co2_emission_saved = round(co2_emission_saved, 2)
                        st.write(f"CO2 emission savings for {appliance}: {rounded_co2_emission_saved} kg")
                

            elif appliance == "Water Heater":
                st.subheader(appliance)
                use_less_hot_water = st.checkbox("Use less hot water", key=f"{appliance}_checkbox19")
                if use_less_hot_water:
                    duration = st.number_input("Duration (hours)", key=f"{appliance}_duration", value=0.0, min_value=0.0, step=0.25, max_value=usage_hours[appliance])
                    new_co2_emission = duration * 1.5  # Adjust this value as needed
                    if duration:
                        co2_emission_saved =  total_emissions[appliance]   - new_co2_emission
                        rounded_co2_emission_saved = round(co2_emission_saved, 2)
                        st.write(f"CO2 emission savings for {appliance}: {rounded_co2_emission_saved} kg")


            elif appliance == "Incandescent Light":
                st.subheader(appliance)
                did_not_use_incandescent_light = st.checkbox("Did not use Incandescent Light", key=f"{appliance}_checkbox20")
                if did_not_use_incandescent_light:
                    duration = st.number_input("Duration (hours)", key=f"{appliance}_duration", value=0.0, min_value=0.0, step=0.25, max_value=usage_hours[appliance])
                    new_co2_emission = duration * 0.05  # Adjust this value as needed
                    if duration:
                        co2_emission_saved =  total_emissions[appliance]   - new_co2_emission
                        rounded_co2_emission_saved = round(co2_emission_saved, 2)
                        st.write(f"CO2 emission savings for {appliance}: {rounded_co2_emission_saved} kg")
            
            elif appliance == "Dishwasher":
                st.subheader(appliance)
                did_not_use_dishwasher = st.checkbox("Did not use Dishwasher", key=f"{appliance}_checkbox23")
                did_not_use_power_dry = st.checkbox("Did not use Power Dry", key=f"{appliance}_checkbox24")
                if did_not_use_dishwasher or did_not_use_power_dry:
                    duration = st.number_input("Duration (hours)", key=f"{appliance}_duration", value=0.0, min_value=0.0, step=0.25, max_value=usage_hours[appliance])
                    new_co2_emission = duration * 0.7  # Adjust this value as needed
                    if duration:
                        co2_emission_saved =  total_emissions[appliance]   - new_co2_emission
                        rounded_co2_emission_saved = round(co2_emission_saved, 2)
                        st.write(f"CO2 emission savings for {appliance}: {rounded_co2_emission_saved} kg")
                    
            elif appliance == "Oven/Stove":
                st.subheader(appliance)
                did_not_use_oven_stove = st.checkbox("Did not use Oven/Stove", key=f"{appliance}_checkbox25")
                if did_not_use_oven_stove:
                    duration = st.number_input("Duration (hours)", key=f"{appliance}_duration", value=0.0, min_value=0.0, step=0.25, max_value=usage_hours[appliance])
                    new_co2_emission = duration * 0.3  # Adjust this value as needed
                    if duration:
                        co2_emission_saved =  total_emissions[appliance]   - new_co2_emission
                        rounded_co2_emission_saved = round(co2_emission_saved, 2)
                        st.write(f"CO2 emission savings for {appliance}: {rounded_co2_emission_saved} kg")
                
            elif appliance == "Refrigerator":
                st.subheader(appliance)
                did_not_use_refrigerator = st.checkbox("Did not use Refrigerator", key=f"{appliance}_checkbox27")
                if did_not_use_refrigerator:
                    duration = st.number_input("Duration (hours)", key=f"{appliance}_duration", value=0.0, min_value=0.0, step=0.25, max_value=usage_hours[appliance])
                    new_co2_emission = duration * 0.22  # Adjust this value as needed
                    if duration:
                        co2_emission_saved =  total_emissions[appliance]   - new_co2_emission
                        rounded_co2_emission_saved = round(co2_emission_saved, 2)
                        st.write(f"CO2 emission savings for {appliance}: {rounded_co2_emission_saved} kg")
                
            elif appliance == "Washing Machine":
                st.subheader(appliance)
                did_not_use_washing_machine = st.checkbox("Did not use Washing Machine", key=f"{appliance}_checkbox30")
                if did_not_use_washing_machine:
                    duration = st.number_input("Duration (hours)", key=f"{appliance}_duration", value=0.0, min_value=0.0, step=0.25, max_value=usage_hours[appliance])
                    new_co2_emission = duration * 0.75  # Adjust this value as needed
                    if duration:
                        co2_emission_saved =  total_emissions[appliance]   - new_co2_emission
                        rounded_co2_emission_saved = round(co2_emission_saved, 2)
                        st.write(f"CO2 emission savings for {appliance}: {rounded_co2_emission_saved} kg")
            
            elif appliance == "Computer/Laptop":
                st.subheader(appliance)
                did_not_use_computer_laptop = st.checkbox("Did not use Computer/Laptop", key=f"{appliance}_checkbox31")
                if did_not_use_computer_laptop:
                    duration = st.number_input("Duration (hours)", key=f"{appliance}_duration", value=0.0, min_value=0.0, step=0.25, max_value=usage_hours[appliance])
                    new_co2_emission = duration * 0.015  # Adjust this value as needed
                    if duration:
                        co2_emission_saved =  total_emissions[appliance]   - new_co2_emission
                        rounded_co2_emission_saved = round(co2_emission_saved, 2)
                        st.write(f"CO2 emission savings for {appliance}: {rounded_co2_emission_saved} kg")

            return (co2_emission_saved, duration)
    # Load the dataset
    appliances_data = {
        "Appliance": ["Refrigerator", "Television", "Computer/Laptop", "Washing Machine", "Dryer",
                    "Dishwasher", "Oven/Stove", "Microwave", "Toaster", "Electric Kettle",
                    "Coffee Maker", "Blender", "Vacuum Cleaner", "Iron", "Hairdryer",
                    "Air Conditioner", "Heater", "Fan", "Incandescent Light", "Water Heater"],
        "CO2_Emission_kg": [0.22, 0.088, 0.015, 0.75, 1, 0.7, 0.3, 0.2, 0.1, 0.1, 0.075, 0.075, 0.15, 0.1, 0.15,
                            1.25, 1.25, 0.075,  0.05, 1.5]
    }
    appliances_df = pd.DataFrame(appliances_data)

    st.write("## CO2 Emissions for Household Appliance")
    col1, col2 = st.columns([2,1])

    with col1:
        st.subheader('Add your Daily Appliance Usage')
        # Multi-select for selecting appliances
        selected_appliances = col1.multiselect("Select Appliances", appliances_df["Appliance"])
        
    with col2:
        usage_hours = {}  # Initialize usage_hours dictionary

        if selected_appliances:
            # Expander for taking user input for hours
            st.subheader('Individual Appliance Input')
            for appliance in selected_appliances:
                usage_hours[appliance] = st.slider(f"{appliance} hours used", min_value=0.0, max_value=24.0, value=0.0, 
                                                        step=0.25)


    if selected_appliances:
        total_emissions = {}
        with st.expander('My Daily Appliance Usage'):
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
                total_emissions_all_tabs += total_co2
                display_co2_metric(total_emissions_all_tabs)

    if selected_appliances:
            st.subheader('')
            st.subheader('Add Appliance for CO2 Savings Prediction')
            with st.expander('Reduce Appliance Carbon Footprint'):
                co2_emissions_saved_current_placeholder = st.empty()
                total_new_co2_emission_saved=0
                col1, col2, col3 = st.columns([1,1,1])
                saved = 0
                duration = 0
                for i, appliance in enumerate(selected_appliances):
                    if i % 3 == 0:
                        with col1:
                            (saved, duration) = create_container(appliance, usage_hours, total_emissions)
                            total_new_co2_emission_saved += saved
                    elif i % 3 == 1:
                        with col2:
                            (saved, duration) = create_container(appliance, usage_hours, total_emissions)
                            total_new_co2_emission_saved += saved
                    else:
                        with col3:
                            (saved, duration) = create_container(appliance, usage_hours, total_emissions)
                            total_new_co2_emission_saved += saved
                co2_emissions_saved_current_placeholder.metric(label="Total CO2 emission savings", value=round(total_new_co2_emission_saved, 2))
                co2_emissions_saved_all_tabs += total_new_co2_emission_saved
                if duration > 0:
                    display_co2_saved_metric(co2_emissions_saved_all_tabs)
                    duration=0
                
            
                            

