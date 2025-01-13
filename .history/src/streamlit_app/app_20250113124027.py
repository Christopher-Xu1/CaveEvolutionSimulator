# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models')))

import streamlit as st
from models.simulation import run_simulation
from models.environment import Environment
import pandas as pd
import json

# Page Config
st.set_page_config(
    page_title="Troglobite Evolution Simulator",
    page_icon="🦑",
    layout="wide",
)

# Title and Description
st.title("Troglobite Evolution Simulator")

if "simulation_ran" not in st.session_state:
    st.session_state["simulation_ran"] = False

if not st.session_state["simulation_ran"]:
    st.write("""
        ## Welcome to the Troglobite Evolution Simulator!
        Explore the fascinating evolution of cave-dwelling organisms. Configure the environment, set simulation parameters, and observe how populations adapt over time.
        
        ### How to Use:
        1. Select an **Environment** (preset or custom).
        2. Adjust parameters like mutation rate, decades, and carrying capacity in the sidebar.
        3. Click **Run Simulation** and analyze the results.
        
        ---
    """)

# Sidebar for Parameters
st.sidebar.header("Simulation Parameters")
num_decades = st.sidebar.number_input("Number of Decades", min_value=1, value=10)
population_size = st.sidebar.number_input("Initial Population Size", min_value=100, value=500)
mutation_rate = st.sidebar.number_input("Mutation Rate", min_value=0.0, value=0.00185, step=0.00001, format="%.5f")
carrying_capacity = st.sidebar.number_input("Carrying Capacity", min_value=100, value=2000)

# Sidebar for Environment Configuration
st.sidebar.header("Environment Configuration")
environment_option = st.sidebar.radio("Choose Environment Setup:", ["Preset Environment", "Custom Environment"])

if environment_option == "Preset Environment":
    preset_name = st.sidebar.selectbox("Cave Preset", ["default_cave", "rich_cave", "harsh_cave"])
    num_patches = st.sidebar.number_input("Number of Patches", min_value=1, value=1)
    light_level = None
    food_availability = None
else:
    st.sidebar.write("Custom Environment Settings:")
    num_patches = st.sidebar.number_input("Number of Patches", min_value=1, value=3)
    light_level = st.sidebar.slider("Light Level (0 = Dark, 0.5 = Lit)", 0.0, 0.5, 0.1)
    food_availability = st.sidebar.slider("Food Availability (0 = Scarce, 1 = Abundant)", 0.0, 1.0, 0.5)
    preset_name = None

# Save and Load Configuration
if st.sidebar.button("Save Configuration"):
    config = {
        "num_decades": num_decades,
        "population_size": population_size,
        "mutation_rate": mutation_rate,
        "carrying_capacity": carrying_capacity,
        "num_patches": num_patches,
        "light_level": light_level,
        "food_availability": food_availability,
        "preset_name": preset_name,
    }
    config_json = json.dumps(config)
    st.download_button("Download Configuration", config_json, "config.json", "application/json")

uploaded_file = st.sidebar.file_uploader("Load Configuration", type="json")
if uploaded_file is not None:
    config = json.load(uploaded_file)
    num_decades = config["num_decades"]
    population_size = config["population_size"]
    mutation_rate = config["mutation_rate"]
    carrying_capacity = config["carrying_capacity"]
    num_patches = config["num_patches"]
    light_level = config["light_level"]
    food_availability = config["food_availability"]
    preset_name = config["preset_name"]

# Run Simulation
if st.sidebar.button("Run Simulation"):
    with st.spinner("Running simulation..."):
        results = run_simulation(
            num_decades=num_decades,
            initial_population_size=population_size,
            mutation_rate=mutation_rate,
            preset_name=preset_name,
            num_patches=num_patches,
            egg_count=50,
            carrying_capacity=carrying_capacity,
        )
        st.session_state["results"] = results
        st.session_state["simulation_ran"] = True
        st.success("Simulation Complete!")
        st.balloons()

# Display Results
if st.session_state["simulation_ran"]:
    results = st.session_state["results"]

    # Summary Section
    st.write("### Simulation Summary")
    st.write(f"- Final Population Size: {results['population_sizes'][-1]}")
    st.write(f"- Final Average Fitness: {results['average_fitness'][-1]:.4f}")
    for trait, values in results["trait_averages"].items():
        st.write(f"- Final Average {trait.capitalize()}: {values[-1]:.4f}")

    # Graphs
    st.write("### Population Dynamics Over Generations")
    st.line_chart(results["population_sizes"])

    st.write("### Average Fitness Over Generations")
    st.line_chart(results["average_fitness"])

    st.write("### Food Availability Over Generations")
    st.line_chart(results["food_availability"])

    st.write("### Trait Evolution Over Generations")
    trait_toggles = {
        trait: st.checkbox(f"Show {trait.capitalize()}", value=True)
        for trait in results["trait_averages"].keys()
    }
    selected_traits = {trait: values for trait, values in results["trait_averages"].items() if trait_toggles[trait]}
    if selected_traits:
        st.line_chart(selected_traits)

    # Download Results
    csv_data = prepare_csv_data(results)
    csv_file = csv_data.to_csv(index=False)
    st.download_button("Download Results as CSV", csv_file, "simulation_results.csv", "text/csv")
