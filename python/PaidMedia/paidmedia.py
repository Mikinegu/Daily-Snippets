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

def text_to_emoji(text):
    words = text.split()
    return ' '.join(WORD_EMOJI_MAP.get(word.lower(), word) for word in words)

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to Emoji Translator Bot!\n"
        "Send any text and I'll turn words into emojis."
    )

# Message handler: turns text to emojis
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    input_text = update.message.text
    emoji_text = text_to_emoji(input_text)
    await update.message.reply_text(emoji_text)

def main():
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    application = ApplicationBuilder().token('YOUR_BOT_TOKEN').build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Emoji Translator Bot is alive! Waiting for messages...")
    application.run_polling()

# Uncomment to run directly
# if __name__ == '__main__':
#     main()
