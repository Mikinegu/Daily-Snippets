
def print_board(board):
    print("\n   1   2   3")
    print("  -------------")
    for idx, row in enumerate(board):
        print(f"{idx+1} | " + " | ".join(row) + " |")
        print("  -------------")
    print("Available cells:")
    for r in range(3):
        for c in range(3):
            if board[r][c] == ' ':
                print(f"({r+1},{c+1})", end=" ")
    print("\n")

def check_win(board, player):
    # Check rows
    for row in board:
        if all([cell == player for cell in row]):
            return True
    # Check columns
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True
    # Check diagonals
    if all([board[i][i] == player for i in range(3)]):
        return True
    if all([board[i][2 - i] == player for i in range(3)]):
        return True
    return False

def check_draw(board):
    return all([cell != ' ' for row in board for cell in row])

def main():
    while True:
        board = [[' ' for _ in range(3)] for _ in range(3)]
        current_player = 'X'
        move_count = 0
        while True:
            print_board(board)
            print(f"Move {move_count+1}. Player {current_player}'s turn.")
            move = input("Enter row and column (e.g. 2 3), or 'q' to quit: ").strip()
            if move.lower() == 'q':
                print("Exiting game. Goodbye!")
                return
            try:
                row, col = map(int, move.split())
            except ValueError:
                print("Invalid input format. Please enter two numbers.")
                continue
            if row not in [1,2,3] or col not in [1,2,3]:
                print("Invalid input. Please enter numbers between 1 and 3.")
                continue
            row -= 1
            col -= 1
            if board[row][col] != ' ':
                print("Cell already taken. Try again.")
                continue
            board[row][col] = current_player
            move_count += 1
            if check_win(board, current_player):
                print_board(board)
                print(f"Player {current_player} wins!")
                break
            if check_draw(board):
                print_board(board)
                print("No more moves left. It's a draw!")
                break
            current_player = 'O' if current_player == 'X' else 'X'
        again = input("Play again? (y/n): ").strip().lower()
        if again != 'y':
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
