# environment.py

import random

class Environment:
    """
    A class representing the cave environment with optimal traits and conditions.
    """

    def __init__(self, optimal_traits=None, environmental_conditions=None):
        """
        Initialize the environment with optimal traits and environmental conditions.

        :param optimal_traits: A dictionary of optimal trait values.
        :param environmental_conditions: A dictionary of environmental parameters.
        """
        # Set default optimal traits if none are provided
        if optimal_traits is not None:
            self.optimal_traits = optimal_traits
        else:
            self.optimal_traits = {
                'pigmentation': 0.0,     # Optimal is no pigmentation
                'eye_size': 0.0,         # Optimal is reduced eyes
                'antennae_length': 1.0,  # Optimal is long antennae
                'metabolic_rate': 0.3,   # Optimal is lower metabolic rate
            }

        # Set default environmental conditions if none are provided
        if environmental_conditions is not None:
            self.environmental_conditions = environmental_conditions
        else:
            self.environmental_conditions = {
                'light_level': 0.0,      # Darkness level (0 = total darkness)
                'food_availability': 0.3,# How abundant is food (0 = scarce)
                'humidity': 0.8,         # Humidity level
                'temperature': 15.0,     # Temperature in degrees Celsius
            }

    def change_conditions(self, changes):
        """
        Change environmental conditions based on the provided changes.

        :param changes: A dictionary of changes to environmental parameters.
        """
        for key, value in changes.items():
            if key in self.environmental_conditions:
                self.environmental_conditions[key] = value
            else:
                print(f"Warning: {key} is not a recognized environmental condition.")

    def update_optimal_traits(self):
        """
        Update optimal traits based on environmental conditions.
        This method can be customized to simulate environmental influence on optimal traits.
        """
        # Example: Adjust optimal traits based on light_level
        light_level = self.environmental_conditions.get('light_level', 0.0)
        if light_level > 0.5:
            self.optimal_traits['pigmentation'] = 1.0  # In lighter environments, pigmentation is beneficial
            self.optimal_traits['eye_size'] = 1.0       # Larger eyes are beneficial in light
        else:
            self.optimal_traits['pigmentation'] = 0.0  # In darkness, pigmentation is not needed
            self.optimal_traits['eye_size'] = 0.0       # Reduced eyes are beneficial in darkness

        # Example: Adjust optimal metabolic_rate based on food_availability
        food_availability = self.environmental_conditions.get('food_availability', 0.3)
        if food_availability < 0.5:
            self.optimal_traits['metabolic_rate'] = 0.2  # Lower metabolic rate is better when food is scarce
        else:
            self.optimal_traits['metabolic_rate'] = 0.7  # Higher metabolic rate is acceptable when food is abundant

        # You can expand this method to adjust other traits based on environmental conditions

    def __repr__(self):
        return f"Environment(optimal_traits={self.optimal_traits}, conditions={self.environmental_conditions})"
