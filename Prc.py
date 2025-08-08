import random
import time
import os

# Constants
BOARD_SIZE = 4
EMPTY_CELL = ' '
history = []

# Create empty board
def create_board():
    return [[EMPTY_CELL for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# Display the board
def print_board(board):
    print("\nCurrent Board:")
    for row in board:
        print(" | ".join(row))
        print("-" * (BOARD_SIZE * 4 - 1))

# Check if a move is valid
def is_valid_move(board, row, col):
    return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and board[row][col] == EMPTY_CELL

# Check winner
def check_winner(board, player_token):
    for i in range(BOARD_SIZE):
        if all(cell == player_token for cell in board[i]) or all(board[j][i] == player_token for j in range(BOARD_SIZE)):
            return True
    if all(board[i][i] == player_token for i in range(BOARD_SIZE)) or all(board[i][BOARD_SIZE - 1 - i] == player_token for i in range(BOARD_SIZE)):
        return True
    return False

# Check for draw
def is_draw(board):
    return all(all(cell != EMPTY_CELL for cell in row) for row in board)

# Human move
def human_move(board, player_token):
    moves_done = 0
    while moves_done < 2:
        try:
            move = input(f"{player_token} (Move {moves_done+1}): Enter row and col (0-{BOARD_SIZE-1}) separated by space: ").split()
            if len(move) != 2:
                print("Enter two numbers separated by space.")
                continue
            row, col = map(int, move)
            if is_valid_move(board, row, col):
                board[row][col] = player_token
                moves_done += 1
                print_board(board)
            else:
                print("Invalid move, try again.")
        except ValueError:
            print("Invalid input. Use numbers.")

# Smart AI move
def ai_move(board, player_token):
    opponent = 'X'
    print(f"\nAI ({player_token}) is making moves...")
    moves_done = 0
    while moves_done < 2:
        move = find_best_move(board, player_token, opponent)
        if move:
            board[move[0]][move[1]] = player_token
            print_board(board)
            moves_done += 1
            time.sleep(0.5)
        else:
            break

# Find best move for AI
def find_best_move(board, ai, human):
    empty_positions = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if board[i][j] == EMPTY_CELL]

    # Try to win
    for row, col in empty_positions:
        board[row][col] = ai
        if check_winner(board, ai):
            board[row][col] = EMPTY_CELL
            return (row, col)
        board[row][col] = EMPTY_CELL

    # Try to block human
    for row, col in empty_positions:
        board[row][col] = human
        if check_winner(board, human):
            board[row][col] = EMPTY_CELL
            return (row, col)
        board[row][col] = EMPTY_CELL

    # Otherwise random
    return random.choice(empty_positions) if empty_positions else None

# Show match history
def show_history():
    print("\nGame History:")
    if not history:
        print("No games played yet.")
    else:
        for idx, result in enumerate(history, 1):
            print(f"{idx}. {result}")
    print("\nDo you want to clear history?")
    choice = input("Enter 'y' to clear or press Enter to skip: ").lower()
    if choice == 'y':
        history.clear()
        print("History cleared.")

# Main game function
def play_game():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("📌 4x4 Tic-Tac-Toe (2 moves per turn)\n")
        print("Select Mode:")
        print("1. Human vs Human")
        print("2. Human vs AI")
        print("3. Show History")
        print("4. Exit")
        choice = input("Your choice: ")

        if choice == '4':
            print("Thanks for playing!")
            break

        elif choice == '3':
            show_history()
            input("\nPress Enter to continue...")
            continue

        elif choice not in ['1', '2']:
            print("Invalid choice. Try again.")
            continue

        board = create_board()
        print_board(board)

        players = ['X', 'O']
        turn = 0

        while True:
            current_player = players[turn % 2]

            if choice == '1' or (choice == '2' and current_player == 'X'):
                human_move(board, current_player)
            else:
                ai_move(board, current_player)

            if check_winner(board, current_player):
                winner = "Moshiur" if current_player == 'X' else ("Shihab" if choice == '1' else "AI")
                print(f"\n🎉 {winner} wins!")
                history.append(f"{winner} won")
                break

            if is_draw(board):
                print("\nIt's a draw!")
                history.append("Match Draw")
                break

            turn += 1

        print("\nReturning to main menu in 3 seconds...")
        time.sleep(3)

if __name__ == "__main__":
    play_game()