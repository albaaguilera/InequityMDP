

Governmental_costs = {
    "Hospitalization": 1000, # every time a person is hospitalized
    "VisitCAP": 30, # every time a person receives medical attention
    "SocialServiceWorker": 1000  #for every social service worker added in the simulation
    }

Resources = {
    "Number_shelters": 5,
    "Number_socialserviceworkers": 5,
    "Healthcare budget": 100000,
    "Social service budget": 50000
    }


class Environment:
    def __init__(self, resources = None, grid_position=(0, 0)):

        resources = resources if resources else Resources

        self.shelters_available = resources.get("Number_shelters", 5)
        self.government_healthcare_budget = resources.get("Healthcare budget", 100000)
        self.government_social_service_budget = resources.get("Social service budget", 50000)

        self.grid_position = grid_position
        self.deprived_capabilities = []
    
    def update_budget(self, action):
        """Update governmental budget based on agent actions."""
        if action == "receive_medical_attention":
            self.government_healthcare_budget -= Governmental_costs["VisitCAP"]
        elif action == "hospitalization":
            self.government_healthcare_budget -= Governmental_costs["Hospitalization"]
        elif action == "add_social_worker":
            self.government_social_service_budget -= Governmental_costs["SocialServiceWorker"]
        
        # Ensure budgets don’t go negative
        self.government_healthcare_budget = max(0, self.government_healthcare_budget)
        self.government_social_service_budget = max(0, self.government_social_service_budget)

    def to_dict(self):
        """Convert the environment context to a dictionary for printing."""
        return {
            "shelters_available": self.shelters_available,
            "government_healthcare_budget": self.government_healthcare_budget,
            "government_social_service_budget": self.government_social_service_budget,
            "grid_position": self.grid_position,
            "deprived_capabilities": self.deprived_capabilities
        }