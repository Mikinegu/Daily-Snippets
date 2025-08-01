
def print_board(board):
    print("\n")
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

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
    board = [[' ' for _ in range(3)] for _ in range(3)]
    current_player = 'X'
    while True:
        print_board(board)
        print(f"Player {current_player}'s turn.")
        try:
            move = input("Enter row and column (1-3 1-3, e.g. 2 3): ")
            row, col = map(int, move.strip().split())
            row -= 1
            col -= 1
            if row not in range(3) or col not in range(3):
                print("Invalid input. Please enter numbers between 1 and 3.")
                continue
            if board[row][col] != ' ':
                print("Cell already taken. Try again.")
                continue
            board[row][col] = current_player
            if check_win(board, current_player):
                print_board(board)
                print(f"Player {current_player} wins!")
                break
            if check_draw(board):
                print_board(board)
                print("It's a draw!")
                break
            current_player = 'O' if current_player == 'X' else 'X'
        except ValueError:
            print("Invalid input format. Please enter two numbers.")

if __name__ == "__main__":
    main()
