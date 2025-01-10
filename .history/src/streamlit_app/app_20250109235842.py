import streamlit as st
from models.simulation import run_simulation  # Import your simulation logic

# Title and Description
st.title("Troglobite Evolution Simulation")
st.write("Simulate the evolution of troglobite traits in cave environments over generations.")

# Input Parameters
st.sidebar.header("Simulation Parameters")
num_generations = st.sidebar.number_input("Number of Generations", min_value=1, value=10)
population_size = st.sidebar.number_input("Initial Population Size", min_value=1, value=100)
mutation_rate = st.sidebar.slider("Mutation Rate", 0.0, 1.0, 0.01)
light_level = st.sidebar.slider("Light Level (0 = Dark, 1 = Bright)", 0.0, 1.0, 0.1)
food_availability = st.sidebar.slider("Food Availability (0 = Scarce, 1 = Abundant)", 0.0, 1.0, 0.5)

# Run Simulation Button
if st.sidebar.button("Run Simulation"):
    st.subheader("Simulation Results")
    results = run_simulation(
        num_generations=int(num_generations),
        initial_population_size=int(population_size),
        mutation_rate=float(mutation_rate),
        light_level=float(light_level),
        food_availability=float(food_availability),
    )
    # Display Results
    st.write("Population Traits Over Generations:")
    st.line_chart(results["trait_trends"])  # Assuming the simulation returns a dictionary with trait trends

    st.write("Population Fitness:")
    st.line_chart(results["fitness_trends"])  # Assuming the simulation returns fitness trends
