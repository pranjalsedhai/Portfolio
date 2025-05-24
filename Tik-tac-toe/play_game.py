from noughtsandcrosses import *

def main():
    board = [['1','2','3'],
             ['4','5','6'],
             ['7','8','9']]
    welcome(board)
    total_score = 0
    while True:
        choice = menu()
        if choice == '1':
            score = play_game(board)
            total_score = score
            print('Your current score is:', total_score)
        elif choice == '2':
            total_score = save_score(total_score)
        elif choice == '3':
            leaderboard = load_scores()
            display_leaderboard(leaderboard)
        elif choice == 'q':
            print('Thank you for playing the "Unbeatable Noughts and Crosses" game.')
            print('Goodbye!')
            return
        else:
            print("\nInvalid option.\nEnter valid option (1, 2, 3 or q)")

if __name__ == '__main__':
    main()
