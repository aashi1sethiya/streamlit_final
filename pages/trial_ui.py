import streamlit as st
import pandas as pd

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
        "Public Transportation": "🚍",
        "Motorcycle": "🏍️",
        "Electric Vehicle": "🔌",
        "Carpool": "🚗👥"  # Custom emoji for carpool
    }

    # Generate SVG elements for each bar with emojis
    svg_elements = []
    bottom_labels = []
    for i, (category, value) in enumerate(sorted_data):
        x = i * (bar_width - bar_overlap) + x_margin
        y = svg_height - (value * bar_height_ratio)
        height = value * bar_height_ratio
        tooltip = f"{category}: {value}"  # Tooltip content
        emoji_code = emoji_codes.get(category, "")
        # Adjust font size of emoji
        svg_elements.append(f'<text x="{x + (bar_width - x_margin) / 2}" y="{svg_height + bar_bottom_margin}" font-size="25" text-anchor="middle">{emoji_code}</text>')
        svg_elements.append(f'<path d="{symbol_path}" transform="translate({x}, {y}) scale({(bar_width - x_margin)/5}, {height/5})" fill="#e54035" opacity="{opacity}"><title>{tooltip}</title></path>')

    # Generate SVG code
    svg_code = f'<svg width="{svg_width}" height="{svg_height + bar_bottom_margin + bar_top_margin}">' + ''.join(svg_elements) + '</svg>'

    # Display SVG in Streamlit
    st.write(svg_code, unsafe_allow_html=True)

# Streamlit UI
st.title("CO2 Emissions by Commute Option")

# Sidebar with multiselect and numeric inputs
with st.sidebar:
    st.header("User Inputs")
    commute_options = [
        "Car",
        "Bicycle",
        "Walking",
        "Public Transportation",
        "Motorcycle",
        "Electric Vehicle",
        "Carpool"]
    
    selected_commutes = st.multiselect("Select Commute Options", commute_options)
    commute_miles = {commute: st.number_input(f"Miles for {commute}", min_value=0.1, max_value=None, step=0.1, key=f"{commute}_miles_input", value=0.1) for commute in selected_commutes}

# Calculate CO2 emissions for selected commutes
co2_emissions = {
    "Car": 0.404,
    "Bicycle": 0.002,
    "Walking": 0.01,
    "Public Transportation": 0.296,
    "Motorcycle": 0.225,
    "Electric Vehicle": 0.05,
    "Carpool": 0.202}

co2_emissions_selected = {commute: commute_miles.get(commute, 0) * co2_emissions.get(commute, 0) for commute in selected_commutes}

# Define the amount of overlap between bars
bar_overlap = 20

# Define opacity
opacity = 0.6

if co2_emissions_selected:
    st.header("CO2 Emissions Graph")
    col1, col2 = st.columns([3, 2])
    with col1:
        generate_graph(co2_emissions_selected, bar_overlap, opacity)

    # Calculate total CO2 emissions
    total_emissions = sum(co2_emissions_selected.values())
    
    with col2:
        st.subheader("Total CO2 Emissions")
        st.write(f"{total_emissions:.2f} kg")
