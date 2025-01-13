#to run in terminal: streamlit run streamlit_app/app.py
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models')))

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from models.simulation import run_simulation
from models.environment import Environment

# Title and Description
st.title("Troglobite Evolution Simulation")
st.write("Simulate the evolution of troglobite traits in cave environments.")


# Sidebar for Simulation Parameters
st.sidebar.header("Simulation Parameters")
num_decades = st.sidebar.number_input("Number of Decades", min_value=1, value=10)
population_size = st.sidebar.number_input("Initial Population Size", min_value=100, value=500)
mutation_rate = st.sidebar.number_input(
    "Mutation Rate (set to default)",
    min_value=0.0,
    value=0.00185,
    step=0.00001,
    format="%.5f"  # Display up to 5 decimal places
)
num_patches = st.sidebar.number_input("Number of Patches", min_value=1, value=1)
egg_count = st.sidebar.number_input("Egg Count Per Reproduction", min_value=1, value=50)
carrying_capacity = st.sidebar.number_input("Carrying Capacity", min_value=100, value=2000)

# Environmental Configuration Options
st.sidebar.header("Environment Configuration")
environment_option = st.sidebar.radio(
    "Choose Environment Setup:",
    ("Preset Environment", "Custom Environment")
)

if environment_option == "Preset Environment":
    # Choose from predefined presets
    preset_name = st.sidebar.selectbox(
        "Cave Preset",
        ["default_cave", "rich_cave", "harsh_cave"]
    )
    light_level = None  # Use preset values
    food_availability = None
else:
    # Custom Environment setup
    st.sidebar.write("Custom Environment Settings:")
    light_level = st.sidebar.slider(
        "Light Level (0 = Complete Darkness, 0.5 = Lit)",
        0.0, 0.5, 0.1
    )
    food_availability = st.sidebar.slider(
        "Food Availability (0 = Scarce, 1 = Abundant)",
        0.0, 1.0, 0.1
    )
    preset_name = None  # No preset used
    
if st.sidebar.button("Run Simulation"):
    st.subheader("Simulation Results")

    # Run the simulation
    with st.spinner("Running simulation..."):
        results = run_simulation(
            num_decades=num_decades,
            initial_population_size=population_size,
            mutation_rate=mutation_rate,
            preset_name=preset_name,
            num_patches=num_patches,
            egg_count=egg_count,
            carrying_capacity=carrying_capacity,
        )

    # Check if results are valid
    if results:
        st.success("Simulation Complete!")

        # Population Size Chart
        st.write("### Population Dynamics Over Generations")
        st.line_chart(results["population_sizes"])
        # Food Availability Chart
        st.write("### Food Availability Over Generations")
        st.line_chart(results["food_availability"])
    else:
        st.error("No results returned from simulation.")
        import matplotlib.pyplot as plt
        
        # Average Fitness Chart
        st.write("### Average Fitness Over Generations")
        st.line_chart(results["average_fitness"])

        # Trait Evolution
        st.write("### Trait Evolution Over Generations")
        for trait, values in results["trait_averages"].items():
            st.write(f"**{trait.capitalize()}**")
            st.line_chart(values)



    # User-selected traits to display
    st.write("### Trait Evolution Over Generations")
    st.write("Select which traits to display:")
    trait_toggles = {}
    for trait in results["trait_averages"].keys():
        trait_toggles[trait] = st.checkbox(f"Show {trait.capitalize()}", value=True)

    # Filter traits based on toggles
    selected_traits = {trait: values for trait, values in results["trait_averages"].items() if trait_toggles[trait]}

    # Plot traits on a single graph
    if selected_traits:
        generations = range(1, len(next(iter(selected_traits.values()))) + 1)  # Number of generations
        plt.figure(figsize=(10, 6))
        for trait, values in selected_traits.items():
            plt.plot(generations, values, label=trait.capitalize(), linewidth=2)
        plt.xlabel("Generation")
        plt.ylabel("Average Trait Value")
        plt.title("Trait Evolution Over Generations")
        plt.legend()
        plt.grid(True)
        st.pyplot(plt)
    else:
        st.write("No traits selected for display.")

