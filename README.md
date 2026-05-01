# Battlesnake AI Bot

## Project Overview
This project implements an intelligent Battlesnake bot using Python.  
The bot participates in a multiplayer environment where it competes against other AI agents by making real-time decisions based on the game state.

The primary goal of the bot is to survive as long as possible while strategically navigating the board, avoiding collisions, and collecting food when necessary.

---

## AI & Decision Making

The core logic of the bot is based on a **Minimax algorithm with Alpha-Beta Pruning**, allowing it to evaluate possible future game states and choose the optimal move.

### Key Features:
- Game state evaluation function
  - Considers distance to food
  - Evaluates available safe space
  - Detects potential head-to-head collisions
- Safe movement validation
  - Avoids walls, self-collisions, and enemy bodies
- Adaptive strategy
  - Prioritizes food when health is low
  - Focuses on survival and space control when large enough

---

## Tech Stack

- Python  
- Flask  
- Minimax Algorithm  
- Alpha-Beta Pruning  

---

## How It Works

The Battlesnake game engine sends HTTP requests to the bot:

- `/start` → initializes the game  
- `/move` → requests the next move  
- `/end` → signals the end of the game  

The bot processes the game state and responds with one of the following moves:

up, down, left, right

---

## Running the Project


Install dependencies using pip

```sh
pip install -r requirements.txt
```

Start the Battlesnake

```sh
main.py
```

Die funktionierende URL unserer Schlange ist wie folgt:

https://763dd6aa-1260-4428-8b34-04e2145edb2d-00-3lw55kw01ihn2.sisko.replit.dev/



