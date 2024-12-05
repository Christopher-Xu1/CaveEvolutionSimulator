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
    def __repr__(self):
        return f"Environment(optimal_traits={self.optimal_traits}, conditions={self.environmental_conditions})"
