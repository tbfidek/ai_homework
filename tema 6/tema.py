import numpy as np
import random
import matplotlib.pyplot as plt

# grid
num_rows = 7
num_cols = 10

# nr of actions (up, down, left, right)
num_actions = 4

# init Q-table with 0 
Q_table = np.zeros((num_rows, num_cols, num_actions))

# learning_rate, discount_factor, exploration probability 
alpha = 0.5 
gamma = 0.95  
epsilon = 0.1  

# init state
initial_state = (3, 0)

# wind for each column
wind = [0, 0, 0, 1, 1, 1, 2, 2, 1, 0]

def transition_state(s, a):
    # 0 = up, 1 = down, 2 = left, 3 = right
    actions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    # taken action:
    next_s = (s[0] + actions[a][0], s[1] + actions[a][1])

    # if action falls outside of the grid:
    # row:
    if next_s[0] < 0:
        next_s = (0, next_s[1])
    elif next_s[0] >= num_rows:
        next_s = (num_rows - 1, next_s[1])
    # column:
    if next_s[1] < 0:
        next_s = (next_s[0], 0)
    elif next_s[1] >= num_cols:
        next_s = (next_s[0], num_cols - 1)

    # apply the wind
    next_s = (next_s[0] - wind[next_s[1]], next_s[1])

    return next_s


# nr of episodes
num_episodes = 5000

# policy init with 0
policy = np.zeros((num_rows, num_cols))

# reward per episod
rewards_per_episode = []

for episode in range(num_episodes):
    # init state and overall reward
    s = initial_state
    total_reward = 0

    for step in range(100):  # limit nr of steps per episode
        if random.uniform(0, 1) < epsilon:
            # exploration: choose a random action
            a = random.choice(range(num_actions))
        else:
            # exploitation: choose the action with the highest Q-value
            a = np.argmax(Q_table[s[0], s[1]])

        # next state and reward
        s_prime = transition_state(s, a)
        reward = -1  # the reward is -1 for all transitions

        # update the Q-value
        old_value = Q_table[s[0], s[1], a]
        next_max = np.max(Q_table[s_prime[0], s_prime[1]])
        # Bellman equation
        new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
        Q_table[s[0], s[1], a] = new_value

        # update the current state
        s = s_prime

        # update the total reward
        total_reward += reward

        # check if goal was reached
        if s == (3, 7):
            break

    # total reward per episode
    rewards_per_episode.append(total_reward)

# for each state, choose max Q-value
for i in range(num_rows):
    for j in range(num_cols):
        policy[i, j] = np.argmax(Q_table[i, j])

print(policy)

arrow_symbols = ['↑', '↓', '←', '→']
new_policy = [['' for _ in range(num_cols)] for _ in range(num_rows)]

# map numeric actions to arrow symbols
for i in range(num_rows):
    for j in range(num_cols):
        action_index = int(policy[i, j])  # Get the numeric action
        new_policy[i][j] = arrow_symbols[action_index]  # Map to arrow symbol

for row in new_policy:
    print(' '.join(row))
    
# plot the total rewards per episode
plt.plot(rewards_per_episode)
plt.xlabel('Episode')
plt.ylabel('Total Reward')
plt.show()