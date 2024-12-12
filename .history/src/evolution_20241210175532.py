from environment import Environment
def update_optimal_traits(patch: dict):
    """
    Update the patch's optimal traits based on its environmental conditions.
    """
    # Retrieve conditions from the patch dictionary
    light_level = patch.get('light_level', 0.0)
    food_availability = patch.get('food_availability', 0.3)

    # Logistic scaling for traits
    patch['optimal_traits']['pigmentation'] = 1 / (1 + pow(2.718, -10 * (light_level - 0.5)))
    patch['optimal_traits']['eye_size'] = 1 / (1 + pow(2.718, -10 * (light_level - 0.5)))

    # Food availability affects metabolic rate and antennae length
    patch['optimal_traits']['metabolic_rate'] = 1 / (1 + pow(2.718, -10 * (food_availability - 0.5)))
    patch['optimal_traits']['antennae_length'] = max(0.5, 1 - food_availability)  # Trade-off with other traits
