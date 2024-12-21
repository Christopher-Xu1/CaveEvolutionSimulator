impr
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
