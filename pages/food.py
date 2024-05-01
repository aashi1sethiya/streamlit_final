import streamlit as st
import plotly.graph_objs as go
import numpy as np

low_impact_food_data = {
    "Locally sourced Fruits": {"co2_per_serving": 0.2},
    "Locally sourced Vegetables": {"co2_per_serving": 0.15},
    "Legumes": {"co2_per_serving": 0.2},
    "Rice & Grains": {"co2_per_serving": 0.9},
    "Tofu": {"co2_per_serving": 0.32},
    "Milk": {"co2_per_serving": 0.32},
    "Eggs": {"co2_per_serving": 0.2},
    "Breads & Pastas": {"co2_per_serving": 0.4},
    "Nuts": {"co2_per_serving": 0.04},
}

# Sort food categories based on CO2 emissions (from highest to lowest)
sorted_food_data = sorted(low_impact_food_data.items(), key=lambda x: x[1]["co2_per_serving"], reverse=False)
categories = [food[0] for food in sorted_food_data]
total_emissions = [food[1]["co2_per_serving"] for food in sorted_food_data]

# Define color gradient
color_scale = np.linspace(0, 1, len(categories))
colors = [f'rgb({255}, {int(255 - (255 * i))}, {0})' for i in color_scale]

# Plotting the graph with color gradient
fig = go.Figure(data=[go.Bar(x=categories, y=total_emissions, marker=dict(color=colors))])
fig.update_layout(
    title="Total CO2 Emissions by Food Category",
    xaxis_title="Food Category",
    yaxis_title="CO2 Emissions (kg) per Serving",
)
st.plotly_chart(fig, use_container_width=True)
