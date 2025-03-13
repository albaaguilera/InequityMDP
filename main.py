from environment.mdp_env import CitizenHealthMDP
from environment.agent import Agent
from environment.context import EnvironmentContext
from utils.render import render

# Create agent and context
agent = Agent()
context = EnvironmentContext()

# Initialize environment
env = CitizenHealthMDP(agent_profile=agent.__dict__, environment_context=context.__dict__)

# Run environment
state, _ = env.reset()
render(state)

for _ in range(5):
    action = env.action_space.sample()
    state, reward, done, _ = env.step(action)
    render(state)
    if done:
        print("Episode finished.")
        break
