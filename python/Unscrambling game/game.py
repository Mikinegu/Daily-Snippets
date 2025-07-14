import random
import time
import Levenshtein

# Sentence bank (increasing difficulty)
sentences = [
    "Hello world",
    "Python is fun to learn",
    "The quick brown fox jumps over the lazy dog",
    "Artificial intelligence is transforming the world",
    "Creativity thrives when boundaries are removed"
]

time_limit = 30  # seconds
hints_used = 0


def scramble_sentence(sentence):
    words = sentence.split()
    scrambled = words[:]
    random.shuffle(scrambled)
    return words, scrambled


def show_hint(correct_words, revealed):
    for i in range(len(correct_words)):
        if not revealed[i]:
            print(f"💡 Hint: Word {i + 1} is '{correct_words[i]}'")
            revealed[i] = True
            return
    print("No more hints available!")


def play_game():
    global hints_used
    for level, sentence in enumerate(sentences, 1):
        print(f"\n--- Level {level} ---")
        correct_words, scrambled = scramble_sentence(sentence)
        revealed = [False] * len(correct_words)

        print("Scrambled Sentence:")
        print(" ".join(scrambled))

        start_time = time.time()
        hints_used = 0

        while True:
            time_elapsed = int(time.time() - start_time)
            time_left = max(0, time_limit - time_elapsed)

            print(f"\n⏳ Time left: {time_left} seconds")
            user_input = input("Type your answer (or type 'hint'): ").strip()

            if user_input.lower() == "hint":
                hints_used += 1
                show_hint(correct_words, revealed)
                continue

            distance = Levenshtein.distance(user_input.lower(), sentence.lower())
            print(f"🔍 Levenshtein Distance: {distance}")

            if user_input.lower() == sentence.lower():
                total_time = int(time.time() - start_time)
                score = max(0, 100 - distance * 5 - total_time - (hints_used * 10))
                print(f"\n🎉 Correct! Score: {score}")
                break

            if time_left <= 0:
                print("⏱ Time's up! Game Over!")
                print(f"The correct sentence was: '{sentence}'")
                return

    print("\n🏁 You completed all levels!")


if __name__ == "__main__":
    print("🎮 Welcome to the Sentence Unscramble Game!")
    print("Type the sentence in the correct order. Use 'hint' to reveal a word.")
    play_game()
