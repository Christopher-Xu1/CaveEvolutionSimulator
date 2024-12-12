import random
import numpy as np

class Environment:
    def __init__(self, optimal_traits=None, environmental_conditions=None, num_patches=1):
        self.num_patches = num_patches
        self.patches = []
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

        
        for _ in range(num_patches):
            self.patches.append({
                'light_level': random.uniform(0, 1),
                'food_availability': random.uniform(0, 1),
                'humidity': random.uniform(0.6, 1.0),
                'temperature': random.uniform(10, 20),
                'optimal_traits': optimal_traits or {
                    'pigmentation': 0.0,
                    'eye_size': 0.0,
                    'antennae_length': 1.0,
                    'metabolic_rate': 0.3,
                }
            })

    def change_conditions(self, changes=None):
        """
        Randomly modify environmental conditions for variability or based on user-defined changes.
        """
        for patch in self.patches:
            if changes:
                for key, value in changes.items():
                    patch[key] = value
            else:
                patch['light_level'] = max(0, min(1, patch['light_level'] + random.uniform(-0.1, 0.1)))
                patch['food_availability'] = max(0, min(1, patch['food_availability'] + random.uniform(-0.1, 0.1)))

    def get_patch(self):
        """
        Select a random patch to simulate spatial heterogeneity.
        """
        return random.choice(self.patches)
