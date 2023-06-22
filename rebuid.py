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
        if piece_color in ["green", "yellow"]:
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