#to run in terminal: streamlit run streamlit_app/app.py
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models')))

import streamlit as st
from models.simulation import run_simulation
from models.environment import Environment

# Title and Description
st.title("Troglobite Evolution Simulation")
st.write("Simulate the evolution of troglobite traits in cave environments.")
# Sidebar for simulation parameters
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
preset_name = st.sidebar.selectbox("Cave Preset", ["default_cave", "rich_cave", "harsh_cave"])
num_patches = st.sidebar.number_input("Number of Patches", min_value=1, value=1)
egg_count = st.sidebar.number_input("Egg Count Per Reproduction", min_value=1, value=50)
carrying_capacity = st.sidebar.number_input("Carrying Capacity", min_value=100, value=2000)

# Run simulation and store results in session state
if st.sidebar.button("Run Simulation"):
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
        # Store results in session state
        st.session_state["results"] = results
        st.success("Simulation Complete!")

# Check if simulation results exist
if "results" in st.session_state:
    results = st.session_state["results"]

    # Plot population dynamics
    st.write("### Population Dynamics Over Generations")
    st.line_chart(results["population_sizes"])

    # Plot average fitness
    st.write("### Average Fitness Over Generations")
    st.line_chart(results["average_fitness"])

    # Dynamic trait toggles for Streamlit line chart
    st.write("### Trait Evolution Over Generations")
    st.write("Select which traits to display:")
    trait_toggles = {
        trait: st.checkbox(f"Show {trait.capitalize()}", value=True)
        for trait in results["trait_averages"].keys()
    }

    # Display selected traits using Streamlit's line chart
    selected_traits = {trait: values for trait, values in results["trait_averages"].items() if trait_toggles[trait]}
    if selected_traits:
        st.line_chart(selected_traits)
    else:
        st.write("No traits selected for display.")
