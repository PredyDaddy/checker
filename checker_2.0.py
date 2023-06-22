import tkinter as tk
import random
import tkinter.messagebox as messagebox
import time
from typing import List, Tuple


valid_moves = []

BOARD_SIZE = 8
SQUARE_SIZE = 60
window = tk.Tk()
window.withdraw()
menu = tk.Menu(window)

board = [[None] * 8 for _ in range(8)]
selected_piece = None
ai_difficulty = "Easy"
game_over = False
PLAYER_COLOR = "white"
AI_COLOR = "black"
PLAYER_KING_COLOR = "green"
AI_KING_COLOR = "yellow"

NORMAL_VALUE = 10  # 普通棋子的价值
KING_VALUE = 20  # 升王棋子的价值
EDGE_VALUE = 5  # 边缘棋子的价值
CENTER_VALUE = 3  # 中心棋子的价值

def draw_board():
    # Clear the canvas
    canvas.delete("all")
    # Draw the squares of the checkerboard
    for row in range(8):
        for col in range(8):
            # Calculate the coordinates of the square based on the row and column numbers
            x1, y1 = col * 60, row * 60
            x2, y2 = x1 + 60, y1 + 60
            # Fill the square with gray if it's a black square
            if (row + col) % 2 == 0:
                canvas.create_rectangle(x1, y1, x2, y2, fill="#8B4513")
            # If there's a piece on the square, draw the piece with its color and shape
            piece = board[row][col]
            if piece is not None:
                # Draw a circle with the color of the piece
                color = "white" if piece == "white" else "black" if piece == "black" else "blue" if piece == "green" else "red"
                canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill=color)
            # If the square is a selected piece or a valid move, mark it with a yellow border
            if selected_piece is not None and (row, col) in get_valid_moves(board, selected_piece[0], selected_piece[1]):
                canvas.create_rectangle(x1 + 2, y1 + 2, x2 - 2, y2 - 2, outline="black", width=4)
    # Update the canvas
    canvas.update()


def is_valid_move(game_board, start_row, start_col, end_row, end_col):
    piece_color = game_board[start_row][start_col]

    # Define a list to store all possible colors of the opponent's pieces
    enemy_piece_colors = []
    if piece_color in ["white", "green"]:
        enemy_piece_colors = ["black", "yellow"]
    elif piece_color in ["black", "yellow"]:
        enemy_piece_colors = ["white", "green"]

    # If the target position is not within the range of the board, or is not empty, return False
    if not (0 <= end_row < 8 and 0 <= end_col < 8) or game_board[end_row][end_col] is not None:
        return False

    # If the absolute difference between the target position and the starting position is 1, it means it is a normal move
    if abs(end_row - start_row) == 1:
        # If the piece is a king, it can move one square in any direction
        if piece_color in ["green", "blue"]:
            # If the target position is the opponent's piece, return False
            if game_board[end_row][end_col] in enemy_piece_colors:
                return False
            else:
                return True
        # If the piece is a normal player piece, it can only move one square up
        elif piece_color == "white" and end_row < start_row:
            # If the target position is the opponent's piece, return False
            if game_board[end_row][end_col] in enemy_piece_colors:
                return False
            else:
                return True
        # If the piece is a normal AI piece, it can only move one square down
        elif piece_color == "black" and end_row > start_row:
            # If the target position is the opponent's piece, return False
            if game_board[end_row][end_col] in enemy_piece_colors:
                return False
            else:
                return True

    # If the absolute difference between the target position and the starting position is 2, it means it is a jump move
    elif abs(end_row - start_row) == 2:
        # Calculate the row and column numbers of the middle position of the jump
        mid_row = (start_row + end_row) // 2
        mid_col = (start_col + end_col) // 2

        # If there is an opponent's piece in the middle position, it can jump over it
        if game_board[mid_row][mid_col] is not None and game_board[mid_row][mid_col] in enemy_piece_colors:
            return True

        # If there is own piece in the middle position, it cannot jump over it
        # Define a list to store all possible colors of own pieces
        own_piece_colors = [piece_color, piece_color.upper()]
        if piece_color in ["white", "green"]:
            own_piece_colors.append("green")
        elif piece_color in ["black", "yellow"]:
            own_piece_colors.append("yellow")

        if game_board[mid_row][mid_col] is not None and game_board[mid_row][mid_col] in own_piece_colors:
            return False

    # In all other cases, return False
    return False

# Returns all legal moves for a piece, parameters are the board, row number, and column number
# Function to get all possible legal moves for a given piece
def get_valid_moves(board, row, col):
    piece = board[row][col]
    moves = []

    # Function to check and add valid moves
    def check_and_add_moves(directions):
        for dx, dy in directions:
            new_row, new_col = row + dx, col + dy
            if is_valid_move(board, row, col, new_row, new_col):
                moves.append((new_row, new_col))
            new_row, new_col = row + 2 * dx, col + 2 * dy
            if is_valid_move(board, row, col, new_row, new_col):
                moves.append((new_row, new_col))

    # King pieces can move or jump in any direction
    if piece in ["green", "yellow"]:
        check_and_add_moves([(-1, -1), (-1, 1), (1, -1), (1, 1)])

    # Regular player pieces can only move or jump upwards
    elif piece == "white":
        check_and_add_moves([(-1, -1), (-1, 1)])

    # Regular AI pieces can only move or jump downwards
    elif piece == "black":
        check_and_add_moves([(1, -1), (1, 1)])

    # Return the list of possible moves
    return moves


def can_jump(row, col):
    # Check if a piece has a chance to jump
    piece = board[row][col]

    if piece is None:
        return False

    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dx, dy in directions:
        move_row, move_col = row + dx, col + dy
        jump_row, jump_col = row + 2 * dx, col + 2 * dy

        if is_on_board(jump_row, jump_col) and board[jump_row][jump_col] is None:
            # If the cell after the jump is empty
            if (piece == PLAYER_COLOR or piece == "white king") and move_row < row and board[move_row][move_col] in [AI_COLOR, "black king"]:
                return True
            elif (piece == AI_COLOR or piece == "black king") and move_row > row and board[move_row][move_col] in [PLAYER_COLOR, "white king"]:
                return True

    return False

def is_on_board(x, y):
    # Check if a coordinate is on the board
    return 0 <= x < 8 and 0 <= y < 8

def make_king(x, y):
    # Check if a piece can be promoted to king, and update its status
    piece = board[x][y]

    if piece is None:
        return False

    if piece == PLAYER_COLOR and x == 0:
        board[x][y] = "white king"
        return True

    elif piece == AI_COLOR and x == 7:
        board[x][y] = "black king"
        return True

    return False

# Move a piece, with parameters for the starting position and the target position
def make_move(board, start_row, start_col, end_row, end_col, is_crowning=False):
    # Get the color of the piece
    piece_color = board[start_row][start_col]

    # Check if it's a jump move
    is_jump_move = abs(end_row - start_row) > 1

    if is_jump_move:
        # Calculate the position of the captured piece
        middle_row = (start_row + end_row) // 2
        middle_col = (start_col + end_col) // 2

        # Remove the captured piece
        board[middle_row][middle_col] = None

    # Move the piece to the target position
    board[end_row][end_col] = piece_color

    # Check if it needs to be crowned
    is_player_piece = piece_color == PLAYER_COLOR
    is_ai_piece = piece_color == AI_COLOR
    reached_opponent_end = (is_player_piece and end_row == 0) or (is_ai_piece and end_row == 8 - 1)

    if reached_opponent_end:
        board[end_row][end_col] = PLAYER_KING_COLOR if is_player_piece else AI_KING_COLOR

    # Clear the starting position
    board[start_row][start_col] = None

    return board

def get_all_moves(board: List[List[str]], color: str) -> List[Tuple[int, int, int, int]]:
    all_moves = [(row, col, *move) 
                 for row in range(8) 
                 for col in range(8) 
                 if board[row][col] in {color, color.upper()} 
                 for move in get_valid_moves(board, row, col)]
    # Check if there are any jumps
    jumps = [move for move in all_moves if abs(move[0] - move[2]) > 1]
    if jumps:
        return jumps
    else:
        return all_moves


def evaluate(board: List[List[str]], color: str) -> int:
    color_map = {PLAYER_KING_COLOR: 7, AI_KING_COLOR: -7, PLAYER_COLOR: 1, AI_COLOR: -1}
    return sum(color_map.get(board[row][col], 0) for row in range(8) for col in range(8) if board[row][col])

def deep_copy(obj):
    return [deep_copy(item) for item in obj] if isinstance(obj, list) else obj

def alpha_beta_search(board, depth, alpha, beta, is_ai_turn):
    if is_game_over() or depth == 0:
        return evaluate(board, AI_COLOR), None

    moves = get_all_moves(board, AI_COLOR if is_ai_turn else PLAYER_COLOR)
    if not moves:
        return (-float('inf'), None) if is_ai_turn else (float('inf'), None)

    best_score = -float('inf') if is_ai_turn else float('inf')
    best_move = None

    for move in moves:
        new_board = deep_copy(board)
        make_move(new_board, *move)

        score, _ = alpha_beta_search(new_board, depth - 1, alpha, beta, not is_ai_turn)

        if is_ai_turn and score > best_score:
            best_score = score
            best_move = move
            alpha = max(alpha, best_score)

        if not is_ai_turn and score < best_score:
            best_score = score
            best_move = move
            beta = min(beta, best_score)

        if beta <= alpha:
            break

    return best_score, best_move

def ai_move():
    time.sleep(0.2)
    best_move = None
    row, col, is_king = None, None, None

    if ai_difficulty == "Easy":
        moves = [(r, c, move[0], move[1]) for r in range(8) for c in range(8) 
                 if board[r][c] in [AI_COLOR, AI_KING_COLOR] 
                 for move in get_valid_moves(board, r, c)]
        if moves:
            must_jump = any(abs(move[0] - move[2]) > 1 for move in moves)
            moves = [move for move in moves if abs(move[0] - move[2]) > 1] if must_jump else moves
            random_move = random.choice(moves)
            make_move(board, *random_move)
            draw_board()
            row, col = random_move[2], random_move[3]
            is_king = make_king(row, col)

    else:
        depth = 2 if ai_difficulty == "Medium" else 4
        _, best_move = alpha_beta_search(board, depth, -float('inf'), float('inf'), True)
        if best_move:
            make_move(board, *best_move)
            draw_board()
            row, col = best_move[2], best_move[3]
            is_king = make_king(row, col)

    while best_move and not is_king and can_jump(row, col):
        _, best_move = alpha_beta_search(board, 4, -float('inf'), float('inf'), True)
        if best_move:
            make_move(board, *best_move)
            draw_board()
            row, col = best_move[2], best_move[3]
            is_king = make_king(row, col)

    if is_game_over():
        show_game_over_message()
        return True

    return False

def set_difficulty(difficulty):
    # setting the difficulty
    global ai_difficulty
    ai_difficulty = difficulty



def handle_click(event):
    global selected_piece, valid_moves, game_over
    x, y = event.x, event.y
    row, col = y // 60, x // 60

    if game_over or not is_on_board(row, col):
        return

    if selected_piece is None:
        if board[row][col] in (PLAYER_COLOR, PLAYER_KING_COLOR):
            selected_piece = (row, col)
            valid_moves = get_valid_moves(board, row, col)
            if any(abs(move[0] - row) > 1 for move in valid_moves):
                valid_moves = [move for move in valid_moves if abs(move[0] - row) > 1]
    else:
        if (row, col) in valid_moves:
            is_king = make_move(board, selected_piece[0], selected_piece[1], row, col)
            draw_board()
            if not is_king and abs(row - selected_piece[0]) > 1 and can_jump(row, col):
                selected_piece = (row, col)
                valid_moves = [move for move in valid_moves if abs(move[0] - row) > 1]
            else:
                selected_piece = None
                ai_move()
        elif board[row][col] in (PLAYER_COLOR, PLAYER_KING_COLOR):
            selected_piece = (row, col)
            valid_moves = get_valid_moves(board, row, col)
            if any(abs(move[0] - row) > 1 for move in valid_moves):
                valid_moves = [move for move in valid_moves if abs(move[0] - row) > 1]
        else:
            selected_piece = None

    draw_board()

def is_game_over():
    # Initialize two variables to store the number of pieces for the player and the AI
    player_pieces, ai_pieces = 0, 0
    player_has_valid_moves, ai_has_valid_moves = False, False
    player_can_capture_king, ai_can_capture_king = False, False

    # Traverse the board to count the number of pieces and check for valid moves
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece in (PLAYER_COLOR, PLAYER_KING_COLOR):
                player_pieces += 1
                if not player_has_valid_moves and get_valid_moves(board, row, col):
                    player_has_valid_moves = True
                if piece == PLAYER_COLOR and not player_can_capture_king:
                    if is_valid_move(board, row, col, row - 2, col - 2) and board[row - 1][col - 1] == AI_KING_COLOR:
                        player_can_capture_king = True
                    elif is_valid_move(board, row, col, row - 2, col + 2) and board[row - 1][col + 1] == AI_KING_COLOR:
                        player_can_capture_king = True
            elif piece in (AI_COLOR, AI_KING_COLOR):
                ai_pieces += 1
                if not ai_has_valid_moves and get_valid_moves(board, row, col):
                    ai_has_valid_moves = True
                if piece == AI_COLOR and not ai_can_capture_king:
                    if is_valid_move(board, row, col, row + 2, col - 2) and board[row + 1][col - 1] == PLAYER_KING_COLOR:
                        ai_can_capture_king = True
                    elif is_valid_move(board, row, col, row + 2, col + 2) and board[row + 1][col + 1] == PLAYER_KING_COLOR:
                        ai_can_capture_king = True

    # If the number of pieces for the player or the AI is 0, return True, indicating the game is over
    if player_pieces == 0 or ai_pieces == 0:
        return True

    # If neither the player nor the AI has valid moves, return True, indicating the game is over
    if not player_has_valid_moves and not ai_has_valid_moves:
        return True

    # If either the player or the AI can capture the opponent's king, return True, indicating the game is over
    if player_can_capture_king or ai_can_capture_king:
        return True

    # If none of the above conditions are met, return False, indicating the game is not over
    return False


import tkinter as tk
from tkinter import messagebox


def display_rules():
    # Display rule descriptions
    messagebox.showinfo("Game Rules",
                        "This is a game of International 64-square Draughts.\n"
                        "The game rules are as follows:\n"
                        "1. Each player occupies one corner with a different color.\n"
                        "2. Pieces can move or jump over other pieces in any of the six adjacent directions connected in a straight line.\n"
                        "3. The first player to occupy all the positions directly opposite wins.\n"
                        "4. If a player's piece captures the opponent's king, it will immediately be crowned king and the game ends.\n"
                        "5. The king is produced when one's piece reaches the last line on the opposite side.\n"
                        "6. The king can move or jump over other pieces in any direction.\n"
                        "Enjoy your game!")


def restart_game():
    global board, game_over
    board = [[None] * 8 for _ in range(8)]
    initialize_board()

    game_over = False

    draw_board()


def show_game_over_message():
    # Display game over message
    player_pieces = 0
    ai_pieces = 0
    for row in range(8):
        for col in range(8):
            if board[row][col] == PLAYER_COLOR or board[row][col] == 'white king':
                player_pieces += 1
            elif board[row][col] == AI_COLOR or board[row][col] == 'black king':
                ai_pieces += 1

    if player_pieces == 0:
        message = 'AI won!'
    else:
        message = 'You won!'

    show_message_in_new_window(message)

    game_over = True


def show_message_in_new_window(message):
    top = tk.Toplevel()
    top.title('Game Over')

    label = tk.Label(top, text=message, font=('Arial', 24))
    label.pack(padx=20, pady=20)

    close_button = tk.Button(top, text='Close Window', command=top.destroy)
    close_button.pack(pady=10)

    restart_button = tk.Button(top, text='Restart Game', command=lambda: restart_game_and_destroy(top))
    restart_button.pack(pady=10)


def restart_game_and_destroy(top):
    top.destroy()
    restart_game()


def initialize_board():
    # Initialize the board state
    for row in range(3):
        for col in range(8):
            if (row + col) % 2 == 1:
                board[row][col] = AI_COLOR
    for row in range(5, 8):
        for col in range(8):
            if (row + col) % 2 == 1:
                board[row][col] = PLAYER_COLOR


def create_menu(window):
    # Create menu
    menu = tk.Menu(window)
    window.config(menu=menu)

    # Add menu items
    rules_menu = tk.Menu(menu)
    menu.add_cascade(label="Game Rules", menu=rules_menu)
    rules_menu.add_command(label="View Rules", command=display_rules)

    difficulty_menu = tk.Menu(menu)
    menu.add_cascade(label="Difficulty Level", menu=difficulty_menu)
    difficulty_menu.add_command(label="Easy", command=lambda: set_difficulty("Easy"))
    difficulty_menu.add_command(label="Medium", command=lambda: set_difficulty("Medium"))
    difficulty_menu.add_command(label="Hard", command=lambda: set_difficulty("Hard"))
    menu.add_command(label="Restart Game", command=restart_game)


if __name__ == "__main__":
    # Create window and canvas
    window = tk.Tk()
    window.title("Checkers")
    canvas = tk.Canvas(window, width=8 * 60, height=8 * 60)
    canvas.pack()

    # Initialize board and bind event
    initialize_board()
    canvas.bind("<Button-1>", handle_click)

    # Create menu and draw board
    create_menu(window)
    draw_board()

    window.mainloop()
