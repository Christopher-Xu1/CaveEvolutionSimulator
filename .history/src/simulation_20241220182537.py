import numpy as np
import random
from environment import Environment
from organism import Organism
from evolution import update_optimal_traits
import matplotlib.pyplot as plt


def run_simulation(
    num_decades,
    initial_population_size,
    preset_name,
    num_patches,
    fitness_threshold,
    egg_count,
    carrying_capacity
):
    mutation_rate = 0.0026
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
        "olfactory_bulb": []
    }

    # Tracking resource usage (optional)
    resource_usage_over_time = []

    for generation in range(1, num_generations + 1):
        for patch in environment.patches:
            update_optimal_traits(patch)

        # Move organisms to patches and calculate fitness
        for organism in population:
            organism.move_to_patch(environment)
            organism.calculate_fitness(organism.environment_patch)
            
        # Calculate and store average fitness
        if population:
            avg_fit = np.mean([org.fitness for org in population])
        else:
            avg_fit = 0
        average_fitness.append(avg_fit)
        
        # Inside your simulation loop, replace the trait collection with:
        for trait, values in trait_averages.items():
            if trait != 'metabolic_rate':
                avg_trait = (
                    np.mean([org.genetics[trait] for org in population]) if population else 0
                )
            else:
                avg_trait = (
                    np.mean([org.metabolic_rate for org in population]) if population else 0
                )
            values.append(avg_trait)


        # Print generation information
        print(f"Generation {generation}:")
        print(f"  Population Size: {len(population)}")
        print(f"  Average Fitness: {avg_fit:.4f}")
        print("  Trait Averages:")
        for trait, values in trait_averages.items():
            print(f"    {trait}: {values[-1]:.4f}")

        # Calculate surviving probabilities using probabilistic selection based on fitness
        surviving_population = [org for org in population if random.random()-0.1 < org.fitness]

        if not surviving_population:
            print(f"Generation {generation}: Population extinct!")
            break

        # Reproduction and mutation
        offspring_population = []
        offspring_counts = []
        total_potential_offspring = 0

        # Calculate potential offspring counts
        for organism in surviving_population:
            # Get food availability of the current patch
            food_availability = organism.environment_patch.get('food_availability')
            # Calculate reproductive capability
            reproductive_capability = (organism.fitness ** 2) * ((egg_count) * (5*food_availability) / egg_count)
            # Introduce slight randomness to offspring count
            count = max(0,int(random.gauss(reproductive_capability, 1)))
            offspring_counts.append(count)
            total_potential_offspring+=count
            
        if  total_potential_offspring>carring_capacity:
            total_potential_offspring=carring_capacity
        
        # Initialize a set to track organisms that have already reproduced
        reproduced_set = set()

        # Create offspring using adjusted counts
        for organism, num_offspring in zip(surviving_population, offspring_counts):
            if organism in reproduced_set:
                continue  # Skip if already reproduced
            for _ in range(num_offspring):
                # Select a parent who has not yet reproduced and is not the current organism
                eligible_parents = [p for p in surviving_population if p not in reproduced_set and p != organism]
                if eligible_parents:
                    parent = random.choice(eligible_parents)
                else:
                    parent = organism  # If no eligible parents, reproduce with self
                # Reproduce to create an offspring
                offspring = organism.reproduce(organism, parent)
                offspring.environment_patch = parent.environment_patch.copy()  # Use a copy to prevent shared references
                offspring.mutate(mutation_rate)
                offspring_population.append(offspring)
            # Mark the organism as having reproduced
            reproduced_set.add(organism)

        # Update population with offspring
        population = offspring_population

        # Initialize a dictionary to count organisms per patch using patch IDs
        patch_population = {patch['id']: 0 for patch in environment.patches}

        for org in population:
            patch_id = org.environment_patch['id']
            patch_population[patch_id] += 1

        # Reduce food availability in each patch based on population and metabolic rate
        for patch in environment.patches:
            patch_id = patch['id']
            count = patch_population[patch_id]
            food_consumed = (count * patch['food_availability'] *  trait_averages["metabolic_rate"][- 1]) / carrying_capacity
            patch['food_availability'] = max(patch['food_availability'] - food_consumed, 0)
            print(f"Patch {patch_id}: Food consumed = {food_consumed:.4f}, Remaining food = {patch['food_availability']:.4f}")

        # Track resource usage
        resource_usage = (sum(patch['food_availability'] for patch in environment.patches) * np.mean(trait_averages["metabolic_rate"])) / carrying_capacity
        resource_usage_over_time.append(resource_usage)
        
        environment.replenish_food()

        # Collect population size data
        population_sizes.append(len(population))

    # Plotting Results
    plot_results_separate(population_sizes, average_fitness, trait_averages, resource_usage_over_time)


def plot_results_separate(population_sizes, average_fitness, trait_averages, resource_usage_over_time):
    generations = range(1, len(population_sizes) + 1)

    # Plot Population Size
    plt.figure(figsize=(10, 6))
    plt.plot(generations, population_sizes, label="Population Size", color="blue", linewidth=2)
    plt.xlabel("Generation")
    plt.ylabel("Population Size")
    plt.title("Population Dynamics Over Generations")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
    # Plot Resource Usage Over Generations
    plt.figure(figsize=(10, 6))
    plt.plot(generations, resource_usage_over_time, label="Resource Usage", color="purple", linewidth=2)
    plt.xlabel("Generation")
    plt.ylabel("Resource Usage")
    plt.title("Resource Usage Over Generations")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Plot Average Fitness
    plt.figure(figsize=(10, 6))
    plt.plot(generations, average_fitness, label="Average Fitness", color="green", linewidth=2)
    plt.xlabel("Generation")
    plt.ylabel("Average Fitness")
    plt.title("Fitness Trends Over Generations")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Plot Trait Averages Together
    plt.figure(figsize=(10, 6))
    for trait, averages in trait_averages.items():
        plt.plot(generations, averages, label=f"Average {trait.capitalize()}", linewidth=2)
    plt.xlabel("Generation")
    plt.ylabel("Average Trait Value")
    plt.title("Trait Evolution Over Generations")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Uncomment the following block to enable user inputs
    """
    try:
        num_decades = int(input("Enter simulation runtime in decades: "))
        initial_population_size = int(input("Enter initial population size: "))
        preset_name = input("Enter cave preset (default_cave, rich_cave, harsh_cave): ")
        fitness_threshold = float(input("Enter minimum fitness threshold (e.g., 0.2): "))
        num_patches=int(input("Enter number of cave patches (1-5): "))
        egg_count = int(input("Enter egg count per reproduction event (e.g., 3000 for Astyanax mexicanus, 50 for mammoth cave fish): "))
        carrying_capacity = int(input("Enter carrying capacity (usually 500-5000): "))
    except ValueError as e:
        print(f"Invalid input: {e}")
        exit(1)
    """

    # Run the simulation with predefined parameters
    run_simulation(
        num_decades=10,
        initial_population_size=500,
        preset_name="harsh_cave",
        num_patches=1,
        fitness_threshold=0.7,
        egg_count=50,
        carrying_capacity=2000
    )
    # To use user inputs, comment out the above run_simulation call and uncomment the block above.
