#to run in terminal: streamlit run streamlit_app/app.py
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models')))

import streamlit as st
from models.simulation import run_simulation
from models.environment import Environment
import pandas as pd
# Function to prepare simulation data for download
def prepare_csv_data(results):
    # Create a DataFrame for population sizes and average fitness
    data = {
        "Generation": list(range(1, len(results["population_sizes"]) + 1)),
        "Population Size": results["population_sizes"],
        "Average Fitness": results["average_fitness"],
    }

    # Add traits to the DataFrame
    for trait, values in results["trait_averages"].items():
        data[f"Trait - {trait.capitalize()}"] = values

    # Add food availability
    data["Food Availability"] = results["food_availability"]

    # Convert to DataFrame
    df = pd.DataFrame(data)
    return df



# Title and Description
st.title("Cave Fish Evolution Simulation")
st.write("Simulate the evolution of troglobite traits in cave environments by testing out different cave conditions and fish populations.")
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
# egg_count = st.sidebar.number_input("Egg Count Per Reproduction", min_value=1, value=50)
carrying_capacity = st.sidebar.number_input("Carrying Capacity", min_value=100, value=2000)

# Sidebar for Environment Configuration
st.sidebar.header("Environment Configuration")
environment_option = st.sidebar.radio(
    "Choose Environment Setup:",
    ["Preset Environment", "Custom Environment"]
)

if environment_option == "Preset Environment":
    # Choose from predefined presets
    preset_name = st.sidebar.selectbox(
        "Cave Preset",
        ["default_cave", "rich_cave", "harsh_cave"]
    )
    num_patches = st.sidebar.number_input("Number of Patches", min_value=1, value=1)
    light_level = None  # Use preset values
    food_availability = None  # Use preset values
else:
    # Custom Environment setup
    st.sidebar.write("Custom Environment Settings:")
    num_patches = st.sidebar.number_input("Number of Patches", min_value=1, value=3)
    light_level = st.sidebar.slider(
        "Light Level (0 = Complete Darkness, 0.5 = Lit)",
        0.0, 0.5, 0.1
    )
    food_availability = st.sidebar.slider(
        "Food Availability (0 = Scarce, 1 = Abundant)",
        0.0, 1.0, 0.5
    )
    preset_name = None  # No preset used


# Run simulation and store results in session state
if st.sidebar.button("Run Simulation"):
    with st.spinner("Running simulation..."):
        if environment_option == "Preset Environment":
            # Initialize environment using preset
            environment = Environment(
                num_patches=num_patches,
                preset=Environment.cave_presets(preset_name)
            )
        else:
            # Initialize environment with custom settings
            environment = Environment(num_patches=num_patches)
            for patch in environment.patches:
                patch["light_level"] = light_level
                patch["food_availability"] = food_availability

        # Run the simulation
        results = run_simulation(
            num_decades=num_decades,
            initial_population_size=population_size,
            mutation_rate=mutation_rate,
            preset_name=preset_name,  # None for custom environment
            num_patches=num_patches,
            egg_count=50,
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
    
    st.write("### Food Availability Over Generations")
    st.line_chart(results["food_availability"])

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



# Add a download button after the simulation results are displayed
if "results" in st.session_state:
    results = st.session_state["results"]

    # Prepare the CSV data
    csv_data = prepare_csv_data(results)
    csv_file = csv_data.to_csv(index=False)

    # Add a download button
    st.download_button(
        label="Download Simulation Results as CSV",
        data=csv_file,
        file_name="simulation_results.csv",
        mime="text/csv",
    )
