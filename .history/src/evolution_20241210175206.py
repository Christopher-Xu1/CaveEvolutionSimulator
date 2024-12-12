from environment import Environment

def update_optimal_traits(environment: Environment):
    """
    Update the environment's optimal traits based on its current environmental conditions.
    This function works with an instance of the Environment class.
    """
    # Retrieve conditions from the environment
    light_level = environment.environmental_conditions.get('light_level', 0.0)
    food_availability = environment.environmental_conditions.get('food_availability', 0.3)

    # Logistic scaling for traits
    environment.optimal_traits['pigmentation'] = 1 / (1 + pow(2.718, -10 * (light_level - 0.5)))
    environment.optimal_traits['eye_size'] = 1 / (1 + pow(2.718, -10 * (light_level - 0.5)))

    # Food availability affects metabolic rate and antennae length
    environment.optimal_traits['metabolic_rate'] = 1 / (1 + pow(2.718, -10 * (food_availability - 0.5)))
    environment.optimal_traits['antennae_length'] = max(0.5, 1 - food_availability)  # Trade-off with other traits
