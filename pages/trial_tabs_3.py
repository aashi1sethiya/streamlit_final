import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

def calculate_footprints(actual_emission, new_emission):
    # Calculate the difference between new and actual emissions
    # Just using a scaling factor as an example
    actual_footprint = actual_emission / 100
    predicted_footprint = new_emission / 100
    return actual_footprint, predicted_footprint

def main():
    st.title("CO2 Footprint Comparison")

    st.sidebar.header("User Inputs")
    actual_emission = st.sidebar.number_input("Actual Commute CO2 Emissions", value=0.0, step=0.01)
    new_emission = st.sidebar.number_input("New Commute CO2 Emissions", value=0.0, step=0.01)

    actual_footprint, predicted_footprint = calculate_footprints(actual_emission, new_emission)
    
    # Load footprint image
    footprint_image = Image.open("footprint.png")

    # Plot actual and predicted footprints using the footprint image
    fig, ax = plt.subplots()
    categories = ["Actual", "Predicted"]
    footprints = [actual_footprint, predicted_footprint]
    bar_positions = np.arange(len(categories))

    # Calculate the maximum height of the footprints to set the ylim
    max_footprint = max(footprints)

    # Overlay the footprint image onto the plot
    for i, category in enumerate(categories):
        # Position the actual footprint image at the maximum height if the predicted footprint is less than the actual one
        if i == 0:  # Actual footprint
            footprint_height = max_footprint
        else:  # Predicted footprint
            footprint_height = footprints[i]
        
        ax.text(bar_positions[i], footprints[i], f"{footprints[i]:.2f}", ha='center')
        ax.imshow(footprint_image, aspect='auto', extent=(bar_positions[i] - 0.4, bar_positions[i] + 0.4, 0, footprint_height))

    # Customize plot
    ax.set_ylabel('CO2 Footprint')
    ax.set_title('Actual vs Predicted CO2 Footprint')
    ax.set_xticks(bar_positions)
    ax.set_xticklabels(categories)
    ax.set_xlim(bar_positions[0] - 0.5, bar_positions[-1] + 0.5)
    ax.set_ylim(0, max_footprint * 1.1)  # Set ylim to ensure all footprints are visible

    # Hide x-axis ticks and labels
    ax.xaxis.set_ticks_position('none')

    # Remove gridlines
    ax.grid(False)

    # Show plot
    st.pyplot(fig)
    
    st.write("Actual CO2 Footprint:", actual_footprint)
    st.write("Predicted CO2 Footprint:", predicted_footprint)

if __name__ == "__main__":
    main()
