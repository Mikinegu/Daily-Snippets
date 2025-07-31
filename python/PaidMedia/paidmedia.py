import os
try:
    from transformers import pipeline
    nlp = pipeline("sentiment-analysis")
except ImportError:
    nlp = None

# Map sentiment to emojis
SENTIMENT_EMOJI = {
    "POSITIVE": "😊👍❤️",
    "NEGATIVE": "😢💔😞",
    "NEUTRAL": "😐"
}

def nlp_emoji_suggestion(text):
    if nlp is None:
        return "(NLP model not installed) " + text_to_emoji(text)
    result = nlp(text)
    label = result[0]["label"].upper()
    emojis = SENTIMENT_EMOJI.get(label, "😐")
    return f"{text}\nSuggested emojis: {emojis}"
# Reverse mapping: emoji to word
EMOJI_WORD_MAP = {v: k for k, v in WORD_EMOJI_MAP.items()}

def emoji_to_text(text):
    chars = text.split()
    return ' '.join(EMOJI_WORD_MAP.get(char, char) for char in chars)

# Command: /text <emojis>
async def text_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text[len('/text '):]
    word_text = emoji_to_text(text)
    await update.message.reply_text(word_text)
# Command: /emoji <text>
async def emoji_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text[len('/emoji '):]
    emoji_text = text_to_emoji(text)
    await update.message.reply_text(emoji_text)
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import logging

# Simple word-to-emoji mapping
WORD_EMOJI_MAP = {
    "happy": "😊",
    "sad": "😢",
    "love": "❤️",
    "fire": "🔥",
    "star": "⭐",
    "cool": "😎",
    "ok": "👌",
    "thumbs": "👍",
    "cat": "🐱",
    "dog": "🐶",
    "sun": "☀️",
    "moon": "🌙",
    "food": "🍔",
    "car": "🚗",
    "tree": "🌳",
    "music": "🎵",
    "heart": "💖",
    "smile": "😄",
    "laugh": "😂",
    "cry": "😭",
    # Add more mappings as needed
}

# Reverse mapping: emoji to word
EMOJI_WORD_MAP = {v: k for k, v in WORD_EMOJI_MAP.items()}

def emoji_to_text(text):
    chars = text.split()
    return ' '.join(EMOJI_WORD_MAP.get(char, char) for char in chars)

# Command: /text <emojis>
async def text_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text[len('/text '):]
    word_text = emoji_to_text(text)
    await update.message.reply_text(word_text)

def text_to_emoji(text):
    words = text.split()
    return ' '.join(WORD_EMOJI_MAP.get(word.lower(), word) for word in words)

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to Emoji Translator Bot!\n"
        "Send any text and I'll turn words into emojis."
    ),    

# Message handler: turns text to emojis
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    input_text = update.message.text
    # Use NLP-powered suggestion
    emoji_text = nlp_emoji_suggestion(input_text)
    await update.message.reply_text(emoji_text)

def main():
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    application = ApplicationBuilder().token('YOUR_BOT_TOKEN').build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('emoji', emoji_command))
    application.add_handler(CommandHandler('text', text_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Emoji Translator Bot is alive! Waiting for messages...")
    application.run_polling()

# Uncomment to run directly
# if __name__ == '__main__':
#     main()
