
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

