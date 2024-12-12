from environment import Environment
from organism import Organism
from evolution import update_optimal_traits

def run_simulation(num_generations, initial_population_size, mutation_rate, num_patches=1):
    environment = Environment(num_patches=num_patches)
    population = [Organism() for _ in range(initial_population_size)]

    for generation in range(1, num_generations + 1):
        print(f"\n--- Generation {generation} ---")

        # Update environmental conditions and optimal traits
        environment.change_conditions()
        for patch in environment.patches:
            update_optimal_traits(patch)

        # Assign organisms to random patches
        for organism in population:
            organism.move_to_patch(environment)

        # Calculate fitness and reproduce
        for organism in population:
            organism.calculate_fitness(organism.environment_patch)

        total_fitness = sum(org.fitness for org in population)
        reproduction_probabilities = [org.fitness / total_fitness for org in population]

        new_population = []
        for _ in range(len(population)):
            parents = random.choices(population, weights=reproduction_probabilities, k=2)
            offspring = Organism.reproduce(parents[0], parents[1])
            offspring.mutate(mutation_rate)
            offspring.move_to_patch(environment)
            offspring.calculate_fitness(offspring.environment_patch)
            new_population.append(offspring)

        population = new_population

        # Log evolutionary metrics
        print(f"Average fitness: {sum(org.fitness for org in population) / len(population):.4f}")
        for trait in population[0].genetics:
            avg_trait = sum(org.genetics[trait] for org in population) / len(population)
            print(f"Average {trait}: {avg_trait:.4f}")

if __name__ == "__main__":
    num_generations = 10
    initial_population_size = 20
    mutation_rate = 0.05
    num_patches = 3
    run_simulation(num_generations, initial_population_size, mutation_rate, num_patches)
