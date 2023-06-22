import tkinter as tk
import random
import tkinter.messagebox as messagebox
import time

# Draw the checkerboard
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
                color = "white" if piece == "white" else "black" if piece == "black" else "green" if piece == "green" else "yellow"
                canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill=color)

                # If the piece is a king, draw a star on the circle
                if piece in ("green", "yellow"):
                    canvas.create_polygon(
                        x1 + 25, y1 + 10,   # Top point
                        x1 + 30, y1 + 30,   # Right bottom point
                        x1 + 40, y1 + 30,   # Right top point
                        x1 + 32, y1 + 40,   # Bottom right point
                        x1 + 35, y1 + 55,   # Bottom middle point
                        x1 + 25, y1 + 45,   # Bottom left point
                        x1 + 15, y1 + 55,   # Bottom middle point
                        x1 + 18, y1 + 40,   # Bottom left point
                        x1 + 10, y1 + 30,   # Left top point
                        x1 + 20, y1 + 30,   # Left bottom point
                        fill="blue"
                    )

            # If the square is a selected piece or a valid move, mark it with a yellow border
            if selected_piece is not None and (row, col) in get_valid_moves(board, selected_piece[0], selected_piece[1]):
                canvas.create_rectangle(x1 + 2, y1 + 2, x2 - 2, y2 - 2, outline="yellow", width=4)

    # Update the canvas
    canvas.update()