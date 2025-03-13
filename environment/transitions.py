def get_transition_probabilities(agent):
    """Define transition probabilities dynamically based on agent properties."""
    return {
        ("sick", "receive_medical_attention"): (1.0 if agent.administrative_state == "registered" else 0.0, "healthier", +10),
        ("sick", "keep_forward"): (1.0, "sicker", -10),
    }
