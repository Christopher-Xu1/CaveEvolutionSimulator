import numpy as np
import random
from models.environment import Environment
from organism import Organism
from evolution import update_optimal_traits
import matplotlib.pyplot as plt

def run_simulation(
    num_decades,
    initial_population_size,
    mutation_rate,
    preset_name,
    num_patches,
    egg_count,
    carrying_capacity,
):  
    num_generations = num_decades * 10  # 10 generations per decade
    environment = Environment(num_patches=num_patches, preset=Environment.cave_presets(preset_name))

    # Assign a unique integer ID to each patch
    for idx, patch in enumerate(environment.patches):
        patch['id'] = idx

    population = [Organism() for _ in range(initial_population_size)]

    # Data collection
    population_sizes = []
    average_fitness = []
    trait_averages = {
        "pigmentation": [],
        "eye_size": [],
        "metabolic_rate": [],
        "lateral_line": [],
        "olfactory_bulb": [],
    }
    food_availabitlity_over_time = []

    for generation in range(1, num_generations + 1):
        for patch in environment.patches:
            update_optimal_traits(patch)

        # Move organisms to patches and calculate fitness
        for organism in population:
            organism.move_to_patch(environment)
            organism.calculate_fitness(organism.environment_patch)

        # Collect data for population and fitness
        population_sizes.append(len(population))
        avg_fit = np.mean([org.fitness for org in population]) if population else 0
        average_fitness.append(avg_fit)

        # Collect trait averages
        for trait, values in trait_averages.items():
            if trait != "metabolic_rate":
                avg_trait = np.mean([org.genetics[trait] for org in population]) if population else 0
            else:
                avg_trait = np.mean([org.metabolic_rate for org in population]) if population else 0
            values.append(avg_trait)

        # Track food availability
        for patch in environment.patches:
            patch_id = patch["id"]
            food_availabitlity_over_time.append(patch["food_availability"])

        # Simulate extinction or reproduction
        surviving_population = [org for org in population if random.random() - 0.1 < org.fitness]
        if not surviving_population:
            print(f"Generation {generation}: Population extinct!")
            break

        # Handle offspring population (existing logic)
        offspring_population = []
        for organism in surviving_population:
            offspring_population.append(organism)  # Simplified reproduction logic

        population = offspring_population

    # Return data for Streamlit
    return {
        "population_sizes": population_sizes,
        "average_fitness": average_fitness,
        "trait_averages": trait_averages,
        "food_availability": food_availabitlity_over_time,
    }

