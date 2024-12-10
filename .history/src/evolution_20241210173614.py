# evolution.py

def update_optimal_traits(environment):
    """
    Update the environment's optimal traits based on its current environmental conditions.
    
    This function encapsulates the logic for how environmental parameters affect 
    the optimal traits of organisms.
    """
    # Retrieve conditions from the environment
    light_level = environment.environmental_conditions.get('light_level', 0.0)
    food_availability = environment.environmental_conditions.get('food_availability', 0.3)

    # Adjust traits based on light level
    if light_level > 0.5:
        environment.optimal_traits['pigmentation'] = 1.0   # Pigmentation beneficial in lighter conditions
        environment.optimal_traits['eye_size'] = 1.0        # Larger eyes are beneficial in light
    else:
        environment.optimal_traits['pigmentation'] = 0.0    # No need for pigmentation in darkness
        environment.optimal_traits['eye_size'] = 0.0         # Reduced eyes beneficial in darkness

    # Adjust metabolic_rate based on food availability
    if food_availability < 0.5:
        environment.optimal_traits['metabolic_rate'] = 0.2   # Lower metabolic rate when food is scarce
    else:
        environment.optimal_traits['metabolic_rate'] = 0.7   # Higher metabolic rate acceptable when food is abundant

    # Extend this logic for other traits as needed.
