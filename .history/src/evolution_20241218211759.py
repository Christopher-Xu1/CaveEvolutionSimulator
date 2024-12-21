def update_optimal_traits(patch: dict):
    light_level = patch.get('light_level')
    food_availability = patch.get('food_availability')

    # Logistic scaling for traits
    patch['optimal_traits']['metabolic_rate'] = max(0.1, food_availability)
