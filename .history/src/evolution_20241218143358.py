def update_optimal_traits(patch: dict):

    # Logistic scaling for traits
    patch['optimal_traits']['pigmentation'] = 1 / (1 + pow(2.718, -10 * (light_level - 0.5)))
    patch['optimal_traits']['eye_size'] = 1 / (1 + pow(2.718, -10 * (light_level - 0.5)))
    patch['optimal_traits']['metabolic_rate'] = max(0.1, food_availability)
