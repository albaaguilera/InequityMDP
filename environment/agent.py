

class Agent:
    def __init__(self, health_state=2, housing_state="ETHOS_0", administrative_state="registered"):
        self.health_state = health_state
        self.housing_state = housing_state
        self.administrative_state = administrative_state

    def update_health(self, new_state):
        """Update health based on the new environment state."""
        if new_state == "healthier":
            self.health_state = min(4, self.health_state + 1)
        elif new_state == "sicker":
            self.health_state = max(0, self.health_state - 1)
