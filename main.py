import pygame
import sys
import queue
import threading
import detection
import random

# Initialize Pygame
pygame.init()

# Constants and setup
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (118, 150, 86)
BEIGE = (238, 238, 210)
HIGHLIGHT = (186, 202, 68)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

# Load images
PIECES = {}
pieces = ['bB', 'bK', 'bN', 'bP', 'bQ', 'bR', 'wB', 'wK', 'wN', 'wP', 'wQ', 'wR']
for piece in pieces:
    PIECES[piece] = pygame.transform.scale(pygame.image.load(f'images\\{piece}.png'), (SQUARE_SIZE, SQUARE_SIZE))

# Draw chessboard
def draw_board(WIN):
    WIN.fill(BEIGE)
    for row in range(ROWS):
        for col in range(COLS):
            if (row + col) % 2 == 1:
                pygame.draw.rect(WIN, BROWN, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Draw pieces
def draw_pieces(WIN, board):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != "--":
                try:
                    WIN.blit(PIECES[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))
                except KeyError:
                    print(f"Error: Invalid piece code '{piece}' at position ({row}, {col})")

# Highlight possible moves
def highlight_moves(WIN, possible_moves):
    for move in possible_moves:
        pygame.draw.rect(WIN, HIGHLIGHT, (move[1] * SQUARE_SIZE, move[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def evaluate_board(board, color):
    """Evaluate the board from the perspective of the given color."""
    score = 0
    piece_square_values = {
        'P': [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [5, 5, 5, 5, 5, 5, 5, 5],
            [1, 1, 2, 3, 3, 2, 1, 1],
            [0.5, 0.5, 1, 2.5, 2.5, 1, 0.5, 0.5],
            [0, 0, 0, 2, 2, 0, 0, 0],
            [0.5, -0.5, -1, 0, 0, -1, -0.5, 0.5],
            [0.5, 1, 1, -2, -2, 1, 1, 0.5],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ],
        'N': [
            [-5, -4, -3, -3, -3, -3, -4, -5],
            [-4, -2, 0, 0, 0, 0, -2, -4],
            [-3, 0, 1, 1.5, 1.5, 1, 0, -3],
            [-3, 0.5, 1.5, 2, 2, 1.5, 0.5, -3],
            [-3, 0, 1.5, 2, 2, 1.5, 0, -3],
            [-3, 0.5, 1, 1.5, 1.5, 1, 0.5, -3],
            [-4, -2, 0, 0.5, 0.5, 0, -2, -4],
            [-5, -4, -3, -3, -3, -3, -4, -5]
        ],
        'B': [
            [-2, -1, -1, -1, -1, -1, -1, -2],
            [-1, 0, 0, 0, 0, 0, 0, -1],
            [-1, 0, 0.5, 1, 1, 0.5, 0, -1],
            [-1, 0.5, 0.5, 1, 1, 0.5, 0.5, -1],
            [-1, 0, 1, 1, 1, 1, 0, -1],
            [-1, 1, 1, 1, 1, 1, 1, -1],
            [-1, 0.5, 0, 0, 0, 0, 0.5, -1],
            [-2, -1, -1, -1, -1, -1, -1, -2]
        ],
        'R': [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0.5, 1, 1, 1, 1, 1, 1, 0.5],
            [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
            [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
            [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
            [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
            [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
            [0, 0, 0, 0.5, 0.5, 0, 0, 0]
        ],
        'Q': [
            [-2, -1, -1, -0.5, -0.5, -1, -1, -2],
            [-1, 0, 0, 0, 0, 0, 0, -1],
            [-1, 0, 0.5, 0.5, 0.5, 0.5, 0, -1],
            [-0.5, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5],
            [0, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5],
            [-1, 0.5, 0.5, 0.5, 0.5, 0.5, 0, -1],
            [-1, 0, 0.5, 0, 0, 0, 0, -1],
            [-2, -1, -1, -0.5, -0.5, -1, -1, -2]
        ],
        'K': [
            [-3, -4, -4, -5, -5, -4, -4, -3],
            [-3, -4, -4, -5, -5, -4, -4, -3],
            [-3, -4, -4, -5, -5, -4, -4, -3],
            [-3, -4, -4, -5, -5, -4, -4, -3],
            [-2, -3, -3, -4, -4, -3, -3, -2],
            [-1, -2, -2, -2, -2, -2, -2, -1],
            [2, 2, 0, 0, 0, 0, 2, 2],
            [2, 3, 1, 0, 0, 1, 3, 2]
        ]
    }
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != "--":
                piece_color = piece[0]
                piece_type = piece[1]
                piece_value = get_piece_value(piece)
                if piece_color == color:
                    score += piece_value + piece_square_values.get(piece_type, [[0]*8])[row][col]
                else:
                    score -= piece_value + piece_square_values.get(piece_type, [[0]*8])[row][col]
    return score


def minimax_with_alpha_beta(board, depth, alpha, beta, is_maximizing, color):
    """Minimax algorithm with alpha-beta pruning."""
    if depth == 0 or check_game_over(board, color):
        return evaluate_board(board, color), None

    best_move = None
    if is_maximizing:
        best_value = -float('inf')
        for row in range(ROWS):
            for col in range(COLS):
                piece = board[row][col]
                if piece != "--" and piece[0] == color:
                    possible_moves = get_possible_moves(piece, (row, col), board)
                    for move in possible_moves:
                        new_board = [r[:] for r in board]
                        new_board[move[0]][move[1]] = new_board[row][col]
                        new_board[row][col] = "--"
                        value, _ = minimax_with_alpha_beta(new_board, depth - 1, alpha, beta, False, color)
                        if value > best_value:
                            best_value = value
                            best_move = ((row, col), move)
                        alpha = max(alpha, best_value)
                        if beta <= alpha:
                            break
    else:
        best_value = float('inf')
        for row in range(ROWS):
            for col in range(COLS):
                piece = board[row][col]
                if piece != "--" and piece[0] != color:
                    possible_moves = get_possible_moves(piece, (row, col), board)
                    for move in possible_moves:
                        new_board = [r[:] for r in board]
                        new_board[move[0]][move[1]] = new_board[row][col]
                        new_board[row][col] = "--"
                        value, _ = minimax_with_alpha_beta(new_board, depth - 1, alpha, beta, True, color)
                        if value < best_value:
                            best_value = value
                            best_move = ((row, col), move)
                        beta = min(beta, best_value)
                        if beta <= alpha:
                            break

    return best_value, best_move

def iterative_deepening(board, color, max_depth):
    """Iterative deepening with increasing depth."""
    best_move = None
    for depth in range(1, max_depth + 1):
        _, move = minimax_with_alpha_beta(board, depth, -float('inf'), float('inf'), True, color)
        best_move = move
    return best_move

transposition_table = {}

def minimax_with_transposition(board, depth, alpha, beta, is_maximizing, color):
    """Minimax with transposition table."""
    board_key = str(board)
    if board_key in transposition_table:
        return transposition_table[board_key]
    
    if depth == 0 or check_game_over(board, color):
        score = evaluate_board(board, color)
        transposition_table[board_key] = (score, None)
        return score, None

    best_move = None
    if is_maximizing:
        best_value = -float('inf')
        for row in range(ROWS):
            for col in range(COLS):
                piece = board[row][col]
                if piece != "--" and piece[0] == color:
                    possible_moves = get_possible_moves(piece, (row, col), board)
                    for move in possible_moves:
                        new_board = [r[:] for r in board]
                        new_board[move[0]][move[1]] = new_board[row][col]
                        new_board[row][col] = "--"
                        value, _ = minimax_with_transposition(new_board, depth - 1, alpha, beta, False, color)
                        if value > best_value:
                            best_value = value
                            best_move = ((row, col), move)
                        alpha = max(alpha, best_value)
                        if beta <= alpha:
                            break
    else:
        best_value = float('inf')
        for row in range(ROWS):
            for col in range(COLS):
                piece = board[row][col]
                if piece != "--" and piece[0] != color:
                    possible_moves = get_possible_moves(piece, (row, col), board)
                    for move in possible_moves:
                        new_board = [r[:] for r in board]
                        new_board[move[0]][move[1]] = new_board[row][col]
                        new_board[row][col] = "--"
                        value, _ = minimax_with_transposition(new_board, depth - 1, alpha, beta, True, color)
                        if value < best_value:
                            best_value = value
                            best_move = ((row, col), move)
                        beta = min(beta, best_value)
                        if beta <= alpha:
                            break

    transposition_table[board_key] = (best_value, best_move)
    return best_value, best_move

def is_valid_move(piece, start_pos, end_pos, board):
    if end_pos is None:
        return False
    piece_type = piece[1]
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    if board[end_row][end_col] != "--" and board[end_row][end_col][0] == piece[0]:
        return False  # Can't capture own piece

    if piece_type == 'P':
        direction = -1 if piece[0] == 'w' else 1
        if start_col == end_col and board[end_row][end_col] == "--":
            if end_row == start_row + direction:
                return True
            if (piece[0] == 'w' and start_row == 6) or (piece[0] == 'b' and start_row == 1):
                if end_row == start_row + 2 * direction and board[start_row + direction][start_col] == "--":
                    return True
        elif abs(start_col - end_col) == 1 and end_row == start_row + direction and board[end_row][end_col] != "--" and board[end_row][end_col][0] != piece[0]:
            return True
    elif piece_type == 'R':
        if start_row == end_row or start_col == end_col:
            if start_row == end_row:
                for col in range(min(start_col, end_col) + 1, max(start_col, end_col)):
                    if board[start_row][col] != "--":
                        return False
            if start_col == end_col:
                for row in range(min(start_row, end_row) + 1, max(start_row, end_row)):
                    if board[row][start_col] != "--":
                        return False
            return True
    elif piece_type == 'N':
        if (abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1) or (abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2):
            return True
    elif piece_type == 'B':
        if abs(start_row - end_row) == abs(start_col - end_col):
            step_row = 1 if end_row > start_row else -1
            step_col = 1 if end_col > start_col else -1
            for i in range(1, abs(start_row - end_row)):
                if board[start_row + i * step_row][start_col + i * step_col] != "--":
                    return False
            return True
    elif piece_type == 'Q':
        if start_row == end_row or start_col == end_col:
            if start_row == end_row:
                for col in range(min(start_col, end_col) + 1, max(start_col, end_col)):
                    if board[start_row][col] != "--":
                        return False
            if start_col == end_col:
                for row in range(min(start_row, end_row) + 1, max(start_row, end_row)):
                    if board[row][start_col] != "--":
                        return False
            return True
        elif abs(start_row - end_row) == abs(start_col - end_col):
            step_row = 1 if end_row > start_row else -1
            step_col = 1 if end_col > start_col else -1
            for i in range(1, abs(start_row - end_row)):
                if board[start_row + i * step_row][start_col + i * step_col] != "--":
                    return False
            return True
    elif piece_type == 'K':
        if abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1:
            return True
    return False

def get_possible_moves(piece, pos, board):
    possible_moves = []
    start_row, start_col = pos
    for row in range(ROWS):
        for col in range(COLS):
            if is_valid_move(piece, pos, (row, col), board):
                possible_moves.append((row, col))
    return possible_moves

def is_in_check(board, king_pos, king_color):
    if king_pos is None:
        return False
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != "--" and piece[0] != king_color:
                if is_valid_move(piece, (row, col), king_pos, board):
                    return True
    return False

def find_king(board, color):
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == f'{color}K':
                return (row, col)
    return None

def check_game_over(board, color):
    king_pos = find_king(board, color)
    if king_pos is None:
        print("King not found for color:", color)
        pygame.quit()  # Properly quit Pygame
        sys.exit()     # Terminate the program
        return False
    if is_in_check(board, king_pos, color):
        for row in range(ROWS):
            for col in range(COLS):
                if board[row][col] != "--" and board[row][col][0] == color:
                    piece = board[row][col]
                    for move in get_possible_moves(piece, (row, col), board):
                        new_board = [r[:] for r in board]
                        new_board[move[0]][move[1]] = piece
                        new_board[row][col] = "--"
                        if not is_in_check(new_board, find_king(new_board, color), color):
                            return False
        print("Checkmate detected for color:", color)
        return True
    return False

# Display WINning/losing screen
def display_game_over(WIN, text):
    font = pygame.font.SysFont('Arial', 64)
    game_over_text = font.render(text, True, WHITE)
    WIN.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)

# Queue for hand tracking data
hands_queue = queue.Queue()
click_queue = queue.Queue()

# Main menu function
def main_menu(hands_queue, click_queue):
    clock = pygame.time.Clock()
    cursor_x, cursor_y = WIDTH // 2, HEIGHT // 2

    # Sensitivity factor
    sensitivity = 2
    moving_average_points = []

    # Menu options
    options = ["Play with Bot", "Play with Friend"]
    option_rects = []
    font = pygame.font.SysFont('Arial', 36)

    for i, option in enumerate(options):
        text = font.render(option, True, WHITE)
        rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 50))
        option_rects.append((text, rect))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not hands_queue.empty():
            raw_x, raw_y = hands_queue.get()
            moving_average_points.append((raw_x * sensitivity, raw_y * sensitivity))
            if len(moving_average_points) > 5:
                moving_average_points.pop(0)
            cursor_x = int(sum([p[0] for p in moving_average_points]) / len(moving_average_points))
            cursor_y = int(sum([p[1] for p in moving_average_points]) / len(moving_average_points))

        click = not click_queue.empty() and click_queue.get()

        row, col = cursor_y // SQUARE_SIZE, cursor_x // SQUARE_SIZE

        # Check if cursor is over any option
        selected_option = None
        for i, (text, rect) in enumerate(option_rects):
            if rect.collidepoint(cursor_x, cursor_y):
                pygame.draw.rect(WIN, (255, 0, 0), rect, 2)  # Highlight selected option
                if click:
                    selected_option = i
                    break

        if selected_option is not None:
            return selected_option  # Return the selected option

        WIN.fill(BLACK)
        for text, rect in option_rects:
            WIN.blit(text, rect)

        # Draw cursor
        pygame.draw.circle(WIN, WHITE, (cursor_x, cursor_y), 10)

        pygame.display.flip()
        clock.tick(60)

def get_piece_value(piece):
    """Returns the value of the given piece for prioritizing moves."""
    if piece[1] == 'P':
        return 1
    elif piece[1] == 'N' or piece[1] == 'B':
        return 3
    elif piece[1] == 'R':
        return 5
    elif piece[1] == 'Q':
        return 9
    elif piece[1] == 'K':
        return 1000
    return 0

def bot_move(board, color):
    """Decide the bot's move."""
    global transposition_table
    
    # Set maximum depth for search
    max_depth = 3  # You can adjust this based on performance needs
    
    # Perform iterative deepening to find the best move
    best_move = iterative_deepening(board, color, max_depth)
    
    if best_move is not None:
        start_pos, end_pos = best_move
        # Return the move in a format that applies it to the board
        return start_pos, end_pos
    else:
        # If no move is found, return a random legal move
        possible_moves = []
        for row in range(ROWS):
            for col in range(COLS):
                piece = board[row][col]
                if piece != "--" and piece[0] == color:
                    possible_moves.extend(get_possible_moves(piece, (row, col), board))
        if possible_moves:
            return random.choice(possible_moves)
        return None

def main(hands_queue, click_queue):
    # Show main menu and get option
    option = main_menu(hands_queue, click_queue)
    
    if option == 0:
        # Play with Bot
        clock = pygame.time.Clock()

        board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

        selected_piece = None
        selected_pos = None
        possible_moves = []
        turn = 'w'
        game_over = False
        winner = ""

        cursor_x, cursor_y = WIDTH // 2, HEIGHT // 2

        sensitivity = 2
        moving_average_points = []

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if not hands_queue.empty():
                raw_x, raw_y = hands_queue.get()
                moving_average_points.append((raw_x * sensitivity, raw_y * sensitivity))
                if len(moving_average_points) > 5:
                    moving_average_points.pop(0)
                cursor_x = int(sum([p[0] for p in moving_average_points]) / len(moving_average_points))
                cursor_y = int(sum([p[1] for p in moving_average_points]) / len(moving_average_points))

            click = not click_queue.empty() and click_queue.get()

            row, col = cursor_y // SQUARE_SIZE, cursor_x // SQUARE_SIZE

            if click:
                if selected_piece is None:
                    if board[row][col] != "--" and board[row][col][0] == turn:
                        selected_piece = board[row][col]
                        selected_pos = (row, col)
                        possible_moves = get_possible_moves(selected_piece, selected_pos, board)
                else:
                    if (row, col) in possible_moves:
                        board[selected_pos[0]][selected_pos[1]] = "--"
                        board[row][col] = selected_piece
                        if check_game_over(board, 'w' if turn == 'b' else 'b'):
                            game_over = True
                            winner = 'White' if turn == 'w' else 'Black'
                        turn = 'b' if turn == 'w' else 'w'
                    selected_piece = None
                    selected_pos = None
                    possible_moves = []

                if turn == 'b':
                    bot_start, bot_end = bot_move(board, 'b')
                    board[bot_end[0]][bot_end[1]] = board[bot_start[0]][bot_start[1]]
                    board[bot_start[0]][bot_start[1]] = "--"
                    if check_game_over(board, 'w'):
                        game_over = True
                        winner = 'Black'
                    turn = 'w'
                    
                    if check_game_over(board, 'w'):
                        game_over = True
                        winner = 'Black'
                    turn = 'w'

            draw_board(WIN)
            highlight_moves(WIN, possible_moves)
            draw_pieces(WIN, board)

            pygame.draw.circle(WIN, BLACK, (cursor_x, cursor_y), 10)

            pygame.display.flip()

            if game_over:
                WIN.fill(BLACK)
                font = pygame.font.SysFont('Arial', 72)
                text = font.render(f"{winner} wins!", True, WHITE)
                rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                WIN.blit(text, rect)
                pygame.display.flip()
                pygame.time.wait(3000)
                break

            clock.tick(60)
    else:
        # Play with Friend
        clock = pygame.time.Clock()

        board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

        selected_piece = None
        selected_pos = None
        possible_moves = []
        turn = 'w'
        game_over = False
        winner = ""

        cursor_x, cursor_y = WIDTH // 2, HEIGHT // 2

        sensitivity = 2
        moving_average_points = []

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if not hands_queue.empty():
                raw_x, raw_y = hands_queue.get()
                moving_average_points.append((raw_x * sensitivity, raw_y * sensitivity))
                if len(moving_average_points) > 5:
                    moving_average_points.pop(0)
                cursor_x = int(sum([p[0] for p in moving_average_points]) / len(moving_average_points))
                cursor_y = int(sum([p[1] for p in moving_average_points]) / len(moving_average_points))

            click = not click_queue.empty() and click_queue.get()

            row, col = cursor_y // SQUARE_SIZE, cursor_x // SQUARE_SIZE

            if click:
                if selected_piece is None:
                    if board[row][col] != "--" and board[row][col][0] == turn:
                        selected_piece = board[row][col]
                        selected_pos = (row, col)
                        possible_moves = get_possible_moves(selected_piece, selected_pos, board)
                else:
                    if (row, col) in possible_moves:
                        board[selected_pos[0]][selected_pos[1]] = "--"
                        board[row][col] = selected_piece
                        if check_game_over(board, 'w' if turn == 'b' else 'b'):
                            game_over = True
                            winner = 'White' if turn == 'w' else 'Black'
                        turn = 'b' if turn == 'w' else 'w'
                    selected_piece = None
                    selected_pos = None
                    possible_moves = []

            draw_board(WIN)
            highlight_moves(WIN, possible_moves)
            draw_pieces(WIN, board)

            pygame.draw.circle(WIN, BLACK, (cursor_x, cursor_y), 10)

            pygame.display.flip()

            if game_over:
                WIN.fill(BLACK)
                font = pygame.font.SysFont('Arial', 72)
                text = font.render(f"{winner} wins!", True, WHITE)
                rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                WIN.blit(text, rect)
                pygame.display.flip()
                pygame.time.wait(3000)
                break

            clock.tick(60)

if __name__ == "__main__":
    main(hands_queue, click_queue)