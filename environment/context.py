
class EnvironmentContext:
    def __init__(self, shelters=5, healthcare_budget=100000, social_service_budget=50000, grid_position=(0, 0)):
        self.shelters_available = shelters
        self.government_healthcare_budget = healthcare_budget
        self.government_social_service_budget = social_service_budget
        self.grid_position = grid_position
        self.deprived_capabilities = []