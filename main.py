import typing
import random
import copy

MAX_DEPTH = 2  # Maximum depth for the minimax algorithm


def info() -> typing.Dict:
    print("INFO")
    return {
        "apiversion": "1",
        "author": "Gruppe 17",  # Our Team
        "color": "#FF0000",  # Choose color
        "head": "mlh-gene",  # Choose head
        "tail": "ice-skate",  # Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# when your Battlesnake is trying to move to a square and checks if it is safe to move there
def is_safe(pos, my_body, opponents, board_width, board_height):
    if not (0 <= pos["x"] < board_width and 0 <= pos["y"] < board_height):
        return False
    if pos in my_body:
        return False
    for snake in opponents:
        if pos in snake["body"]:
            return False
    return True


# Check if the snake is in danger of colliding with another snake's head
def head_collision_danger(pos, opponents, my_length):
    danger = 0
    for snake in opponents:
        enemy_head = snake["body"][0]
        if abs(pos["x"] - enemy_head["x"]) + abs(pos["y"] - enemy_head["y"]) == 1:
            if len(snake["body"]) >= my_length:
                danger += 1
    return danger


# Get the neighbors position
def get_neighbors(pos):
    return [
        {"x": pos["x"] + 1, "y": pos["y"]},  # Right
        {"x": pos["x"] - 1, "y": pos["y"]},  # Left
        {"x": pos["x"], "y": pos["y"] + 1},  # Up
        {"x": pos["x"], "y": pos["y"] - 1}  # Down
    ]


# Calculate distance between two points
def manhattan_dist(p1, p2):
    return abs(p1["x"] - p2["x"]) + abs(p1["y"] - p2["y"])


# Evaluate the state of the game
def eval_state(my_head, my_body, opponents, food_list, board_width, board_height):
    if not food_list:  # If there is not food on the board
        return 0
    # Find the move that brings the snake closest to the nearest food
    nearest_food = min(food_list, key=lambda f: manhattan_dist(my_head, f))
    dist_tofood = manhattan_dist(my_head, nearest_food)
    # Calculate the number of safe spaces
    space_score = sum(
        1 for neighbor in get_neighbors(my_head)
        if is_safe(neighbor, my_body, opponents, board_width, board_height))
    # Calculate the danger of colliding with another snake
    danger = head_collision_danger(my_head, opponents, len(my_body))

    # Return the evaluation score
    return -3 * dist_tofood + 2 * space_score - 6 * danger


# Minimax algorithm and Alpha-Beta Pruning
def minimax(game_state, depth, alpha, beta, maximizing_player):
    my_body = game_state["you"]["body"]
    my_head = my_body[0]
    board = game_state["board"]
    food_list = board["food"]
    opponents = board["snakes"]
    board_width = board["width"]
    board_height = board["height"]

    # if the game is over or the maximum depth is reached
    if depth == 0 or not food_list:
        return eval_state(my_head, my_body, opponents, food_list, board_width, board_height), None

    # Define the possible moves
    direction = {
        "up": {"x": my_head["x"], "y": my_head["y"] + 1},
        "down": {"x": my_head["x"], "y": my_head["y"] - 1},
        "left": {"x": my_head["x"] - 1, "y": my_head["y"]},
        "right": {"x": my_head["x"] + 1, "y": my_head["y"]}
    }
    best_move = None  # Initialize the best move

    # Maximizing player
    if maximizing_player:
        max_eval = float('-inf')
        for move, new_head in direction.items():
            if not is_safe(new_head, my_body, opponents, board_width, board_height):
                continue  # If the move is not safe, skip it

            new_body = [new_head] + my_body[:-1]  # Update the body of the snake
            new_state = copy.deepcopy(game_state)  # Create a copy of the game state
            new_state['you']['body'] = new_body  # Update the body of the snake in the new game state
            new_state["you"]["health"] -= 1  # Decrease the health of the snake

            eval, _ = minimax(new_state, depth - 1, alpha, beta, False)  # Recursive call
            if eval > max_eval:
                max_eval = eval
                best_move = move
            elif eval == max_eval:
                best_move = random.choice([best_move, move])

            alpha = max(alpha, eval)  # Update alpha
            if beta <= alpha:  # Alpha-Beta Pruning
                break
        return max_eval, best_move  # Return the maximum evaluation score and the best move

    else:  # Minimizing player
        min_eval = float('inf')
        for move, new_head in direction.items():
            new_body = [new_head] + my_body[:-1]
            new_state = copy.deepcopy(game_state)  # Create a copy of the game state
            new_state['you']['body'] = new_body
            new_state["you"]["health"] -= 1
            eval, _ = minimax(new_state, depth - 1, alpha, beta, True)  # Recursive call
            min_eval = min(min_eval, eval)  # Update the minimum evaluation score
            beta = min(beta, eval)  # Update beta
            if beta <= alpha:  # Alpha-Beta Pruning
                break
        return min_eval, None  # Return the minimum evaluation score and None


# snake move function
def move(game_state: typing.Dict) -> typing.Dict:
    # Call the minimax algorithm to find the best move
    _, best_move = minimax(game_state, MAX_DEPTH, float('-inf'), float('inf'), True)
    # If no best move is found, choose a random move
    if not best_move:
        best_move = random.choice(["up", "down", "left", "right"])

    print(f"MOVE {game_state['turn']}: {best_move}")
    return {"move": best_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
