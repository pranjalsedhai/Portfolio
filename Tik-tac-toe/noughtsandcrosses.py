import random
import os.path
import json
random.seed()

def draw_board(board):
    """
    Displays the Tic-Tac-Toe board.
    
    Parameters:
        board (list): A 3x3 list representing the game board.
    
    Returns:
        None   
    """
    for i in range(len(board)):
        print(" -----------")
        print("| " + " | ".join(board[i]) + " |")
    print(" -----------")


def welcome(board):
    """
    Displays the welcome message and the initial board layout.
    
    Parameters:
        board (list): A 3x3 list representing the game board.
    
    Returns:
        None
    """
    print('Welcome to the "Unbeatable Noughts and Crosses" game.')
    print('The board layour is shown below:')
    draw_board(board)

def initialise_board(board):
    """
    Initializes the board with empty spaces.
    
    Parameters:
        board (list): A 3x3 list representing the game board.
    
    Returns:
        list: The initialized board with empty spaces.
    """
    for i in range(3):
        for j in range(3):
            board[i][j] = ' '
    return board

def get_player_move(board):
    """
    Prompts the player to make a move and validates the input.
    
    Parameters:
        board (list): A 3x3 list representing the game board.
    
    Returns:
        tuple: The row and column indices of the player's chosen move.
    """
    move_mapping = {
        '1': (0, 0), '2': (0, 1), '3': (0, 2),
        '4': (1, 0), '5': (1, 1), '6': (1, 2),
        '7': (2, 0), '8': (2, 1), '9': (2, 2)
    }

    while True:
        move = input("\t\t    1 2 3\n\t\t    4 5 6\nChoose your square: 7 8 9 : ")
        if move in move_mapping:
            row, col = move_mapping[move]
            if board[row][col] not in ('X', 'O'):
                return row, col
            else:
                print("That position is already taken! Try again.")
        else:
            print("Invalid input! Enter a number between 1 and 9.")


def choose_computer_move(board):
    """
    Selects a random available move for the computer.
    
    Parameters:
        board (list): A 3x3 list representing the game board.
    
    Returns:
        tuple: The row and column indices of the computer's chosen move.
    """
    available_moves = [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']
    row, col = random.choice(available_moves)
    return row, col

def check_for_win(board, mark):
    """
    Checks if a given player has won the game.
    
    Parameters:
        board (list): A 3x3 list representing the game board.
        mark (str): The player's mark ('X' or 'O').
    
    Returns:      
        bool: True if the player has won, otherwise False.
    """
    for row in board:
        if all(cell == mark for cell in row):
            return True
    for col in range(3):
        if all(board[row][col] == mark for row in range(3)):
            return True
    if all(board[i][i] == mark for i in range(3)) or all(board[i][2 - i] == mark for i in range(3)):
        return True
    return False

def check_for_draw(board):
    """
    Checks if the game has ended in a draw.
    
    Parameters:
        board (list): A 3x3 list representing the game board.
    
    Returns:
        bool: True if there is at least one empty space, otherwise False.
    """
    if any(cell == ' ' for row in board for cell in row):
        return False
    return True

def play_game(board):
    """
    Manages the game flow, alternating between player and computer moves.
    
    Parameters:
        board (list): A 3x3 list representing the game board.
    
    Returns:
        int: 1 if the player wins, -1 if the computer wins, 0 for a draw.
    """
    board = initialise_board(board)
    draw_board(board)
    while True:
        row, col = get_player_move(board)
        board[row][col] = 'X'
        draw_board(board)
        if check_for_win(board, 'X'):
            print("Congratulations! You won!")
            return 1
        if check_for_draw(board):
            print("It's a draw!")
            return 0
        
        row, col = choose_computer_move(board)
        board[row][col] = 'O'
        draw_board(board)
        if check_for_win(board, 'O'):
            print("Computer wins! Better luck next time.")
            return -1
        if check_for_draw(board):
            print("It's a draw!")
            return 0

def menu():
    """
    Displays the game menu and gets user input.
    
    Returns:
        str: The user's menu choice.
    """
    print("\nEnter one of the following options:")
    print("1 - Play the game")
    print("2 - Save score in file 'leaderboard.txt'")
    print("3 - Load and display the scores from the 'leaderboard.txt'")
    print("q - End the program")
    choice = input("Enter your choice (1, 2, 3 or q): ")
    return choice

def load_scores():
    """
    Loads the leaderboard scores from a file.
    
    Returns:
        dict: A dictionary of player names and their scores.
    """
    leaders = {}
    if os.path.exists("leaderboard.txt"):
        with open("leaderboard.txt", "r") as file:
            try:
                data = file.read().strip()
                if data:
                    leaders = json.loads(data)
            except json.JSONDecodeError:
                print("Error: leaderboard.txt is corrupted. Resetting leaderboard.")
                leaders = {}
    return leaders


def save_score(total_score):
    """
    Saves the player's score to the leaderboard file.
    
    Parameters:
        total_score (int): The score to be saved.
    
    Returns:
        int: Always returns 0.
    """
    if total_score == 0:
        print("\nNo new score to save.")
        return 0

    name = input("Enter your name: ").strip().lower()
    scores = load_scores()

    scores[name] = scores.get(name, 0) + total_score

    with open("leaderboard.txt", "w") as file:
        json.dump(scores, file)

    print(f"Score saved! {name}: {scores[name]}")

    return 0

def display_leaderboard(leaders):
    """
    Displays the leaderboard in descending order of scores.
    
    Parameters:
        leaders (dict): A dictionary of player names and their scores.
    
    Returns:
        None
    """
    sorted_leaders = sorted(leaders.items(), key=lambda x: x[1], reverse=True)

    print("\nLeaderboard:")
    for name, score in sorted_leaders:
        print(f"{name}: {score}")

