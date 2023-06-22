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