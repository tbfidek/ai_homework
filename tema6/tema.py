import numpy as np
import random
import matplotlib.pyplot as plt

# Dimensiunile grilei
num_rows = 7
num_cols = 10

# Numărul de acțiuni posibile (sus, jos, stânga, dreapta)
num_actions = 4

# Inițializarea tabelei Q cu zero
Q_table = np.zeros((num_rows, num_cols, num_actions))

# Parametrii algoritmului
alpha = 0.5  # Rata de învățare
gamma = 0.95  # Factorul de discount
epsilon = 0.1  # Probabilitatea de a alege o acțiune aleatoare (explorare)

# Starea inițială
initial_state = (3, 0)

# Vântul sub fiecare coloană
wind = [0, 0, 0, 1, 1, 1, 2, 2, 1, 0]


def transition_state(s, a):
    # Acțiunile sunt codificate ca: 0 = sus, 1 = jos, 2 = stânga, 3 = dreapta
    actions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    # Aplicăm acțiunea
    next_s = (s[0] + actions[a][0], s[1] + actions[a][1])

    # Verificăm dacă starea următoare este în afara grilei
    if next_s[0] < 0:
        next_s = (0, next_s[1])
    elif next_s[0] >= num_rows:
        next_s = (num_rows - 1, next_s[1])

    if next_s[1] < 0:
        next_s = (next_s[0], 0)
    elif next_s[1] >= num_cols:
        next_s = (next_s[0], num_cols - 1)

    # Aplicăm vântul
    next_s = (next_s[0] - wind[next_s[1]], next_s[1])

    return next_s


# Numărul de episoade
num_episodes = 5000

for episode in range(num_episodes):
    # Inițializăm starea curentă
    s = initial_state

    for step in range(100):  # Limităm numărul de pași pe episod la 100
        # Selectăm o acțiune
        if random.uniform(0, 1) < epsilon:
            # Explorare: alegem o acțiune aleatoare
            a = random.choice(range(num_actions))
        else:
            # Exploatare: alegem acțiunea cu cea mai mare valoare Q
            a = np.argmax(Q_table[s[0], s[1]])

        # Obținem starea următoare și recompensa
        s_prime = transition_state(s, a)
        reward = -1  # Recompensa este -1 pentru toate tranzițiile

        # Actualizăm valoarea Q
        old_value = Q_table[s[0], s[1], a]
        next_max = np.max(Q_table[s_prime[0], s_prime[1]])
        new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
        Q_table[s[0], s[1], a] = new_value

        # Actualizăm starea curentă
        s = s_prime

        # Verificăm dacă am ajuns la obiectiv
        if s == (3, 7):
            break

# Inițializăm politica cu zero
policy = np.zeros((num_rows, num_cols))

# Pentru fiecare stare, alegem acțiunea cu cea mai mare valoare Q
for i in range(num_rows):
    for j in range(num_cols):
        policy[i, j] = np.argmax(Q_table[i, j])

# Afișăm politica
print(policy)

# Initialize the list to store the total rewards per episode
rewards_per_episode = []

for episode in range(num_episodes):
    # Initialize the current state and the total reward
    s = initial_state
    total_reward = 0

    for step in range(100):  # Limit the number of steps per episode to 100
        # Select an action
        if random.uniform(0, 1) < epsilon:
            # Exploration: choose a random action
            a = random.choice(range(num_actions))
        else:
            # Exploitation: choose the action with the highest Q-value
            a = np.argmax(Q_table[s[0], s[1]])

        # Get the next state and reward
        s_prime = transition_state(s, a)
        reward = -1  # The reward is -1 for all transitions

        # Update the Q-value
        old_value = Q_table[s[0], s[1], a]
        next_max = np.max(Q_table[s_prime[0], s_prime[1]])
        new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
        Q_table[s[0], s[1], a] = new_value

        # Update the current state
        s = s_prime

        # Update the total reward
        total_reward += reward

        # Check if we have reached the goal
        if s == (3, 7):
            break

    # Append the total reward for this episode to the list
    rewards_per_episode.append(total_reward)

# Plot the total rewards per episode
plt.plot(rewards_per_episode)
plt.xlabel('Episode')
plt.ylabel('Total Reward')
plt.show()
