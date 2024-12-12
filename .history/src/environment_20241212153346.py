import random

class Environment:
    def __init__(self, num_patches=1, preset=None):
        """
        Initialize the environment with a specified number of patches.
        Each patch represents a separate area with environmental conditions.
        
        :param num_patches: Number of environmental patches.
        :param preset: Preset environmental configuration (optional).
        """
        self.patches = []
        if preset:
            # Initialize environment based on a preset
            for _ in range(num_patches):
                # Ensure a deep copy of the preset to avoid shared references
                patch = preset.copy()
                patch['optimal_traits'] = preset['optimal_traits'].copy()
                self.patches.append(patch)
        else:
            # Default random initialization for patches
            for _ in range(num_patches):
                self.patches.append({
                    'light_level': random.uniform(0, 1),
                    'food_availability': random.uniform(0, 1),
                    'temperature': random.uniform(10, 20),
                    'optimal_traits': {
                        'pigmentation': 0.0,
                        'eye_size': 0.0,
                        'metabolic_rate': 0.3,
                    }
                })

    def change_conditions(self, changes=None):
        """
        Update environmental conditions for all patches.
        
        :param changes: Dictionary of condition updates (optional).
                        If None, random changes are applied.
        """
        for patch in self.patches:
            if changes:
                for key, value in changes.items():
                    patch[key] = value
            else:
                # Apply random changes within bounds
                patch['light_level'] = max(0, min(1, patch['light_level'] + random.uniform(-0.1, 0.1)))
                patch['food_availability'] = max(0, min(1, patch['food_availability'] + random.uniform(-0.1, 0.1)))

def move_to_patch(self, environment):
    """
    Assign the organism to a random patch from the environment.
    """
    self.environment_patch = environment.get_patch()


    @staticmethod
    def cave_presets(preset_name):
        """
        Retrieve predefined cave presets for environmental conditions.
        
        :param preset_name: Name of the preset to retrieve.
        :return: A dictionary representing the preset configuration.
        """
        presets = {
            "default_cave": {
                'light_level': 0.0,
                'food_availability': 0.3,
                'temperature': 15.0,
                'optimal_traits': {
                    'pigmentation': 0.0,
                    'eye_size': 0.0,
                    'metabolic_rate': 0.2,
                }
            },
            "rich_cave": {
                'light_level': 0.1,
                'food_availability': 0.7,
                'temperature': 18.0,
                'optimal_traits': {
                    'pigmentation': 0.1,
                    'eye_size': 0.1,
                    'metabolic_rate': 0.4,
                }
            },
            "harsh_cave": {
                'light_level': 0.0,
                'food_availability': 0.1,
                'temperature': 12.0,
                'optimal_traits': {
                    'pigmentation': 0.0,
                    'eye_size': 0.0,
                    'metabolic_rate': 0.1,
                }
            }
        }
        return presets.get(preset_name, presets["default_cave"])
