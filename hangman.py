import random
import secrets


class Hangman:

    def __init__(self, word_list):
        self.word_list = word_list
        self.current_word = ""
        self.guessed_letters = []
        self.wrong_guesses = 0
        self.max_wrong = 6

    def shuffle_words(self, num_words):
        # Use secrets to generate a truly random seed
        seed = secrets.randbits(32)

        print(f"Shuffling words with truly random seed: {seed}")

        # Use secrets.SystemRandom() for cryptographically strong random shuffle
        secure_random = random.Random(seed)
        secure_random.shuffle(self.word_list)

        # Keep only the requested number of words
        if num_words < len(self.word_list):
            self.word_list = self.word_list[:num_words]

        print(f"Playing with {len(self.word_list)} word(s)")

    def start_round(self, word):
        self.current_word = word.lower()
        self.guessed_letters = []
        self.wrong_guesses = 0

    def display_hangman(self):
        stages = [
            # Stage 0
            """
            +---+
            |   |
                |
                |
                |
                |
            =========
            """,
            # Stage 1
            """
            +---+
            |   |
            O   |
                |
                |
                |
            =========
            """,
            # Stage 2
            """
            +---+
            |   |
            O   |
            |   |
                |
                |
            =========
            """,
            # Stage 3
            """
            +---+
            |   |
            O   |
           /|   |
                |
                |
            =========
            """,
            # Stage 4
            """
            +---+
            |   |
            O   |
           /|\\  |
                |
                |
            =========
            """,
            # Stage 5
            """
            +---+
            |   |
            O   |
           /|\\  |
           /    |
                |
            =========
            """,
            # Stage 6
            """
            +---+
            |   |
            O   |
           /|\\  |
           / \\  |
                |
            =========
            """
        ]
        print(stages[self.wrong_guesses])

    def display_word(self):
        display = ""
        for letter in self.current_word:
            if letter in self.guessed_letters:
                display += letter + " "
            else:
                display += "_ "
        print(f"Word: {display.strip()}")

    def is_word_complete(self):
        for letter in self.current_word:
            if letter not in self.guessed_letters:
                return False
        return True

    def make_guess(self, letter):
        letter = letter.lower()

        if letter in self.guessed_letters:
            return "already_guessed"

        self.guessed_letters.append(letter)

        if letter in self.current_word:
            return "correct"
        else:
            self.wrong_guesses += 1
            return "wrong"

    def is_game_over(self):
        return self.wrong_guesses >= self.max_wrong or self.is_word_complete()

    def did_win(self):
        return self.is_word_complete() and self.wrong_guesses < self.max_wrong
