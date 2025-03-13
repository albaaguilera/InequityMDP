import gym
from gym import spaces
import numpy as np
from environment.context import Environment
from environment.agent import Agent

class CitizenHealthMDP(gym.Env):
    def __init__(self, agent_profile=None, environment_context=None):
        super(CitizenHealthMDP, self).__init__()

        self.states = {"sick": 0, "healthier": 1, "sicker": 2}
        self.actions = {"receive_medical_attention": 0, "keep_forward": 1}
        self.action_space = spaces.Discrete(len(self.actions))
        self.observation_space = spaces.Discrete(len(self.states))

        self.agent_profile = agent_profile if agent_profile else Agent
        
        # Transition probabilities and rewards (flexible for expansion)
        self.transition_probs = {
            (self.states["sick"], self.actions["receive_medical_attention"]): (
                1.0 if self.agent_profile["administrative_state"] == "registered" else 0.0,
                self.states["healthier"],
                +10
            ),
            (self.states["sick"], self.actions["keep_forward"]): (1.0, self.states["sicker"], -10),
        }
        
        impossible_actions = [
            action for state, action in self.transition_probs
            if self.transition_probs[(state, action)][0] == 0.0 and state == self.states["sick"]
        ]

        self.environment_context = environment_context if environment_context else Environment
        
        # Current state
        self.state = {"name": "sick", "index": self.states["sick"], "profile": agent_profile, "context": environment_context, "deprived capabilities": impossible_actions}
        
    def step(self, action):
        # Handle invalid actions gracefully
        state_index = self.state["index"]
        if (state_index, action) not in self.transition_probs:
            prob, next_state_index, reward = (0.0, state_index, 0)
        else:
            prob, next_state_index, reward = self.transition_probs[(state_index, action)]
        
        # State transition based on probability
        if np.random.rand() < prob:
            next_state_name = [name for name, idx in self.states.items() if idx == next_state_index][0]
            self.state["name"] = next_state_name
            self.state["index"] = next_state_index

            # Update health state according to the new state
            if next_state_name == "healthier":
                self.state["profile"]["health_state"] = min(4, self.state["profile"]["health_state"] + 1)
            elif next_state_name == "sicker":
                self.state["profile"]["health_state"] = max(0, self.state["profile"]["health_state"] - 1)
        
        # Update environment budget based on the action taken
        action_name = [key for key, val in self.actions.items() if val == action][0]
        self.environment_context.update_budget(action_name)
        
        # Check if episode is done
        done = self.state["index"] in [self.states["healthier"], self.states["sicker"]]
        
        return self.state, reward, done, {}
    
    def reset(self, seed=None, options=None):
        self.state["name"] = "sick"
        self.state["index"] = self.states["sick"]
        self.state["profile"] = self.agent_profile
        self.state["context"] = self.environment_context
        return self.state, {}
    
    def render(self):
        print(f"Current state: {self.state['name']}, Profile: {self.state['profile']}, Context: {self.state['context'].to_dict()}")
