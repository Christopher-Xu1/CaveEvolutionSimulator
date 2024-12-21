import random
class Environment:
    def __init__(self, num_patches=1, preset=None):
        self.patches = []
        if preset:
            for _ in range(num_patches):
                patch = preset.copy()
                patch['optimal_traits'] = preset['optimal_traits'].copy()
                self.patches.append(patch)
        else:
            for _ in range(num_patches):
                self.patches.append({
                    'light_level': random.uniform(0, 1),
                    'food_availability': random.uniform(0, 1),
                    'temperature': random.uniform(10, 20),
                    'optimal_traits': {
                        'pigmentation': 0.0,
                        'eye_size': 0.0,
                        'metabolic_rate': 0.3,
                        'lateral_line': 0.7,
                        'olfactory_bulb': 0.8,
                    }
                })

    def change_conditions(self, changes=None):
        for patch in self.patches:
            if changes:
                for key, value in changes.items():
                    patch[key] = value
            else:
                patch['light_level'] = max(0, min(1, patch['light_level'] + random.uniform(-0.1, 0.1)))
                patch['food_availability'] = max(0, min(1, patch['food_availability'] + random.uniform(-0.1, 0.1)))

    def get_patch(self):
        if not self.patches:
            raise ValueError("Environment has no patches available.")
        return random.choice(self.patches)

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
                    'pigmentation': 0.0,          # Energy-saving regressive trait
                    'eye_size': 0.0,             # Energy-saving regressive trait
                    'metabolic_rate': 0.2,       # Moderate energy requirement
                    'lateral_line': 0.7,         # Enhanced sensory adaptation
                    'olfactory_bulb': 0.8        # High olfactory adaptation
                }
            },
            "rich_cave": {
                'light_level': 0.1,
                'food_availability': 0.7,
                'temperature': 18.0,
                'optimal_traits': {
                    'pigmentation': 0.1,          # Slight energy savings
                    'eye_size': 0.1,             # Minimal eye regression
                    'metabolic_rate': 0.4,       # Higher metabolic cost (rich resources)
                    'lateral_line': 0.8,         # Strong lateral line adaptation
                    'olfactory_bulb': 0.9        # Very high olfactory adaptation
                }
            },
            "harsh_cave": {
                'light_level': 0.0,
                'food_availability': 0.1,
                'temperature': 12.0,
                'optimal_traits': {
                    'pigmentation': 0.0,          # Full regression
                    'eye_size': 0.0,             # Full regression
                    'metabolic_rate': 0.1,       # Low energy cost (scarce resources)
                    'lateral_line': 0.6,         # Moderate sensory adaptation
                    'olfactory_bulb': 0.7        # High olfactory adaptation
                }
            }
        }
        return presets.get(preset_name, presets["default_cave"])
