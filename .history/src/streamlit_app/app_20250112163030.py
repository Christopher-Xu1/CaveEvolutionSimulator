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

# Title and Description
st.title("Troglobite Evolution Simulation")
st.write("Simulate the evolution of troglobite traits in cave environments over generations.")

# Sidebar for Input Parameters
st.sidebar.header("Simulation Parameters")
num_decades = st.sidebar.number_input("Number of Decades", min_value=1, value=10)
population_size = st.sidebar.number_input("Initial Population Size", min_value=100, value=500)
mutation_rate = st.sidebar.number_input("Mutati", min_value=100, value=500)
light_level = st.sidebar.slider("Light Level (0 = Dark, 1 = Bright)", 0.0, 0.5, 0.1)
food_availability = st.sidebar.slider("Food Availability (0 = Scarce, 1 = Abundant)", 0.0, 0.5, 0.1)

# Run Simulation Button
if st.sidebar.button("Run Simulation"):
    st.subheader("Simulation Results")
    
    # Run the simulation
    with st.spinner("Running simulation..."):
        results = run_simulation(
            num_generations=int(num_generations),
            initial_population_size=int(population_size),
            mutation_rate=float(mutation_rate),
            light_level=float(light_level),
            food_availability=float(food_availability),
        )
    
    # Check if results are returned
    if results:
        st.success("Simulation Complete!")
        
        # Display Trait Trends
        st.write("### Trait Evolution Over Generations")
        trait_data = pd.DataFrame(results["trait_trends"])  # Assuming traits are in a dictionary
        st.line_chart(trait_data)

        # Display Fitness Trends
        st.write("### Average Fitness Over Generations")
        fitness_data = pd.DataFrame({"Fitness": results["fitness_trends"]})
        st.line_chart(fitness_data)

        # Option to Download Results
        st.write("### Download Results")
        csv_data = trait_data.to_csv(index=False)
        st.download_button(
            label="Download Trait Data as CSV",
            data=csv_data,
            file_name="trait_data.csv",
            mime="text/csv",
        )
    else:
        st.error("No results returned. Please check your simulation logic.")
