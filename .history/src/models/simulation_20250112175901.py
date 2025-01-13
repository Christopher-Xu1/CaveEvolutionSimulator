import numpy as np
import random
from environment import Environment
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
        patch["id"] = idx

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
    food_availability_over_time = []

    for generation in range(1, num_generations + 1):
        for patch in environment.patches:
            update_optimal_traits(patch)

        # Move organisms to patches and calculate fitness
        for organism in population:
            organism.move_to_patch(environment)
            organism.calculate_fitness(organism.environment_patch)

        # Collect data
        population_sizes.append(len(population))
        avg_fit = np.mean([org.fitness for org in population]) if population else 0
        average_fitness.append(avg_fit)

        for trait, values in trait_averages.items():
            if trait != "metabolic_rate":
                avg_trait = np.mean([org.genetics[trait] for org in population]) if population else 0
            else:
                avg_trait = np.mean([org.metabolic_rate for org in population]) if population else 0
            values.append(avg_trait)

        # Reproduction and mutation
        surviving_population = [org for org in population if random.random() - 0.1 < org.fitness]
        if not surviving_population:
            print(f"Generation {generation}: Population extinct!")
            break

        offspring_population = []
        offspring_counts = []
        total_potential_offspring = 0

        for organism in surviving_population:
            food_availability = organism.environment_patch.get("food_availability", 1)
            reproductive_capability = (organism.fitness**2) * (
                (egg_count * (5 * food_availability) ** 2) / egg_count
            )
            count = max(0, int(random.gauss(reproductive_capability, 1)))
            offspring_counts.append(count)
            total_potential_offspring += count

        if total_potential_offspring > carrying_capacity:
            scaling_factor = carrying_capacity / total_potential_offspring
            offspring_counts = [int(count * scaling_factor) for count in offspring_counts]

        for organism, num_offspring in zip(surviving_population, offspring_counts):
            for _ in range(num_offspring):
                offspring = organism.reproduce(organism, random.choice(surviving_population))
                offspring.mutate(mutation_rate)
                offspring_population.append(offspring)

        population = offspring_population

        # Update food availability
        for patch in environment.patches:
            food_availability = patch["food_availability"]
            food_availability = max(0, food_availability - 0.01)  # Simulate food depletion
            food_availability_over_time.append(food_availability)

    return {
        "population_sizes": population_sizes,
        "average_fitness": average_fitness,
        "trait_averages": trait_averages,
        "food_availability": food_availability_over_time,
    }
