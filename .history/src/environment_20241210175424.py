import random
import numpy as np

class Environment:
    def __init__(self, optimal_traits=None, environmental_conditions=None, num_patches=1):
        self.num_patches = num_patches
        self.patches = []
        
        class Environment:
    def __init__(self, num_patches=1):
        self.patches = []
        for _ in range(num_patches):
            self.patches.append({
                'light_level': random.uniform(0, 1),
                'food_availability': random.uniform(0, 1),
                'humidity': random.uniform(0.6, 1.0),
                'temperature': random.uniform(10, 20),
                'optimal_traits': {
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
