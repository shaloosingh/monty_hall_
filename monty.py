import streamlit as st
import random
import matplotlib.pyplot as plt

# Function to simulate one Monty Hall game
def simulate_game(switch: bool) -> bool:
    doors = [0, 1, 2]
    prize_door = random.choice(doors)
    player_choice = random.choice(doors)

    # Host opens a door that is neither the prize door nor the player's choice
    remaining_doors = [door for door in doors if door != player_choice and door != prize_door]
    if remaining_doors:
        opened_door = random.choice(remaining_doors)
    else:
        opened_door = random.choice([door for door in doors if door != player_choice])

    # If player switches, they pick the remaining unopened door
    if switch:
        player_choice = next(door for door in doors if door != player_choice and door != opened_door)

    return player_choice == prize_door

# Function to run multiple simulations
def run_simulation(num_trials: int, switch: bool) -> float:
    wins = 0
    for _ in range(num_trials):
        if simulate_game(switch):
            wins += 1
    win_rate = wins / num_trials * 100
    return win_rate

# Streamlit app
st.title("🎯 Monty Hall Problem Simulator")

st.sidebar.header("Simulation Settings")
num_trials = st.sidebar.number_input("Number of Simulations", min_value=100, max_value=100000, value=1000, step=100)

st.write("## Strategy Outcomes")

# Run simulations
stay_win_rate = run_simulation(num_trials, switch=False)
switch_win_rate = run_simulation(num_trials, switch=True)

# Display results
st.metric(label="Stay Strategy Win Rate", value=f"{stay_win_rate:.2f}%")
st.metric(label="Switch Strategy Win Rate", value=f"{switch_win_rate:.2f}%")

# Plotting
strategies = ['Stay', 'Switch']
win_rates = [stay_win_rate, switch_win_rate]

fig, ax = plt.subplots()
ax.bar(strategies, win_rates, color=['red', 'green'])
ax.set_ylabel('Win Rate (%)')
ax.set_title('Monty Hall Simulation Results')
ax.set_ylim(0, 100)

st.pyplot(fig)

st.write("""
---
### 📖 About the Monty Hall Problem
- There are 3 doors. Behind one door is a car (prize); behind the others, goats.
- You pick a door.
- The host, who knows what is behind the doors, opens another door, revealing a goat.
- You are then given the choice to **stay** with your original choice or **switch** to the remaining door.
- **Switching** gives you a 2/3 chance of winning, **staying** only a 1/3 chance!
""")
