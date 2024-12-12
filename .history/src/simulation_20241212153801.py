def run_simulation(
    num_decades,
    initial_population_size,
    preset_name,
    num_patches=1,
    fitness_threshold=0.2,
    egg_count=3000,
    carrying_capacity=1000
):
    mutation_rate = 5.97e-9
    num_generations = num_decades * 10  # 10 generations per decade
    environment = Environment(num_patches=num_patches, preset=Environment.cave_presets(preset_name))
    population = [Organism() for _ in range(initial_population_size)]

    population_sizes = []
    trait_averages = {"pigmentation": [], "eye_size": [], "metabolic_rate": []}

    for generation in range(1, num_generations + 1):
        environment.change_conditions()
        for patch in environment.patches:
            update_optimal_traits(patch)

        for organism in population:
            organism.move_to_patch(environment)  # Assign a valid patch

        for organism in population:
            organism.calculate_fitness(organism.environment_patch)  # Calculate fitness

        viable_population = [org for org in population if org.fitness >= fitness_threshold]

        if not viable_population:
            print("Population extinct!")
            break

        total_offspring = sum(
            int(egg_count / (1 + egg_count / 50)) for _ in viable_population
        )
        if total_offspring > carrying_capacity:
            total_offspring = carrying_capacity

        parents = random.choices(
            viable_population,
            weights=[org.fitness for org in viable_population],
            k=total_offspring * 2
        )
        offspring_population = []
        for i in range(0, len(parents), 2):
            if i + 1 < len(parents):
                offspring = Organism.reproduce(parents[i], parents[i + 1])
                offspring.mutate(mutation_rate)
                offspring.move_to_patch(environment)
                offspring.calculate_fitness(offspring.environment_patch)
                offspring_population.append(offspring)

        population = offspring_population[:carrying_capacity]
        population_sizes.append(len(population))

        for trait in trait_averages:
            avg_trait = (
                np.mean([org.genetics[trait] for org in population]) if population else 0
            )
            trait_averages[trait].append(avg_trait)

    plt.figure(figsize=(12, 8))
    generations = range(len(population_sizes))
    plt.plot(generations, population_sizes, label="Population Size", color="blue", linewidth=2)

    for trait, averages in trait_averages.items():
        plt.plot(generations, averages, label=f"Average {trait.capitalize()}", linewidth=2)

    plt.xlabel("Generation")
    plt.ylabel("Values")
    plt.title("Population Growth and Trait Evolution")
    plt.legend()
    plt.grid()
    plt.show()
