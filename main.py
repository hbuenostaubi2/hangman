import os
import sys
import configparser
from hangman import Hangman
# import hangman

def get_resource_path(relative_path):
    # For external files (like config), always look next to the executable/script
    if getattr(sys, 'frozen', False):
        # Running as compiled executable - look next to the .exe
        base_path = os.path.dirname(sys.executable)
    else:
        # Running as Python script - look next to the .py file
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)


def load_words_from_config():
    config = configparser.ConfigParser()
    config_path = get_resource_path('configuration/words.ini')

    try:
        config.read(config_path)
        word_string = config.get('words', 'word_list') # pick up resource
        # Split by comma and strip whitespace
        words = [word.strip() for word in word_string.split(',')]
        return words
    except Exception as e:
        print(f"Error loading configuration: {e}")
        print(f"Looking for config at: {config_path}")
        return []


def play_round(game, word):
    """Play a single round of hangman"""
    game.start_round(word)
    print(f"\n=== New Word ===")
    print(f"Word length: {len(word)}")

    while not game.is_game_over():
        print()
        game.display_hangman()
        game.display_word()
        print(f"Wrong guesses: {game.wrong_guesses}/{game.max_wrong}")
        print(f"Guessed letters: {', '.join(sorted(game.guessed_letters))}")

        guess = input("\nEnter a letter: ").strip()

        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single letter!")
            continue

        result = game.make_guess(guess)

        if result == "already_guessed":
            print("You already guessed that letter!")
        elif result == "correct":
            print("Correct!")
        else:
            print("Wrong!")

    # Show final result
    print()
    game.display_hangman()
    game.display_word()

    if game.did_win():
        print("\nCongratulations! You won!")
        return True
    else:
        print(f"\nGame Over! The word was: {game.current_word}")
        return False


def main():
    print("=== HANGMAN GAME ===\n")

    # Load words from configuration
    words = load_words_from_config()

    if not words:
        print("No words found in configuration!")
        return

    print(f"Loaded {len(words)} words from configuration")

    # Main game loop
    while True:
        # Ask how many words to play with
        while True:
            try:
                num_words = int(input("\nHow many words would you like to play with? "))
                if num_words > 0:
                    break
                else:
                    print("Please enter a positive number.")
            except ValueError:
                print("Please enter a valid number.")

        # Create game and shuffle words
        game = Hangman(words.copy())
        game.shuffle_words(num_words)

        # Play all rounds
        wins = 0
        losses = 0

        for word in game.word_list:
            if play_round(game, word):
                wins += 1
            else:
                losses += 1

            # Ask to continue if there are more words
            if game.word_list.index(word) < len(game.word_list) - 1:
                input("\nPress Enter to continue to next word...")

        # Show final score
        print("\n=== Final Score ===")
        print(f"Wins: {wins}")
        print(f"Losses: {losses}")

        # Ask to play again
        play_again = input("\nDo you want to play again? (yes/no): ").strip().lower()
        if play_again != "yes" and play_again != "y":
            break

    print("\nThanks for playing!")


if __name__ == "__main__":
    main()
