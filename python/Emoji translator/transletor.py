import string

def emoji_translate(sentence):
    emoji_dict = {
        "happy": "😊",
        "sad": "😢",
        "love": "❤️",
        "fire": "🔥",
        "star": "⭐",
        "stars": "⭐"
    }

    words = sentence.split()
    translated_words = []

    for word in words:
        # Remove punctuation from the word (temporarily)
        stripped = word.strip(string.punctuation)
        # Check lowercase version for matching
        lower = stripped.lower()

        if lower in emoji_dict:
            # Preserve any punctuation (e.g., stars!)
            emoji = emoji_dict[lower]
            prefix = word[:word.find(stripped)] if word.find(stripped) != -1 else ""
            suffix = word[word.find(stripped) + len(stripped):] if stripped in word else ""
            translated_words.append(f"{prefix}{emoji}{suffix}")
        else:
            translated_words.append(word)

    return " ".join(translated_words)

