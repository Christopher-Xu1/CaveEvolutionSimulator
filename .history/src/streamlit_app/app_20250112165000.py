import streamlit as st
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models')))

from models.simulation import run_simulation  # Import your simulation logic
from models.simulation import run_simulation
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

# Run the simulation
if st.sidebar.button("Run Simulation"):
    st.subheader("Simulation Results")
    
    # Initialize environment
    if environment_option == "Preset Environment":
        environment = Environment(
            num_patches=num_patches,
            preset=Environment.cave_presets(preset_name)
        )
    else:
        environment = Environment(num_patches=num_patches)
        for patch in environment.patches:
            patch["light_level"] = light_level
            patch["food_availability"] = food_availability

    # Run the simulation
    with st.spinner("Running simulation..."):
        try:
            results = run_simulation(
                num_decades=num_decades,
                initial_population_size=population_size,
                mutation_rate=mutation_rate,
                preset_name=preset_name,
                num_patches=num_patches,
                egg_count=egg_count,
                carrying_capacity=carrying_capacity,
            )
        except Exception as e:
            st.error(f"Error running simulation: {e}")
            st.stop()

    # Display Results
    if results:
        st.success("Simulation Complete!")
        
        # Display population size
        st.write("### Population Dynamics Over Generations")
        st.line_chart(results["population_sizes"])

        # Display average fitness
        st.write("### Average Fitness Over Generations")
        st.line_chart(results["average_fitness"])

        # Display trait evolution
        st.write("### Trait Evolution Over Generations")
        for trait, values in results["trait_averages"].items():
            st.line_chart({trait: values})

        # Display resource usage
        st.write("### Food Availability Over Generations")
        st.line_chart(results["food_availability"])

    else:
        st.error("No results returned from simulation.")
