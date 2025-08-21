import random

quotes = [
	"Believe you can and you're halfway there.",
	"Your limitation—it's only your imagination.",
	"Push yourself, because no one else is going to do it for you.",
	"Great things never come from comfort zones.",
	"Dream it. Wish it. Do it.",
	"Success doesn’t just find you. You have to go out and get it.",
	"The harder you work for something, the greater you’ll feel when you achieve it."
]

def print_random_quote():
	print(random.choice(quotes))

if __name__ == "__main__":
	print_random_quote()
