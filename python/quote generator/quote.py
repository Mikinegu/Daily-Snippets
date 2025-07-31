# Command: /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Quote Generator Bot Commands:\n"
        "/start - Welcome message\n"
        "/quote - Get a random quote\n"
        "/addquote <your quote> - Add your own quote\n"
        "/myquotes - List your added quotes\n"
        "/removequote <index> - Remove your quote by its number in /myquotes\n"
        "/countquotes - Show total number of quotes\n"
        "/help - Show this help message"
    )

# Command: /removequote <index>
async def remove_quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = update.message.text.split()
    if len(args) != 2 or not args[1].isdigit():
        await update.message.reply_text("Usage: /removequote <index> (see /myquotes for indexes)")
        return
    idx = int(args[1]) - 1
    quotes = USER_QUOTES.get(user_id, [])
    if 0 <= idx < len(quotes):
        removed = quotes.pop(idx)
        # Also remove from global QUOTES
        if removed in QUOTES:
            QUOTES.remove(removed)
        await update.message.reply_text(f"Removed your quote: {removed}")
    else:
        await update.message.reply_text("Invalid index. Use /myquotes to see your quote numbers.")
# Store user-added quotes in a dict by user id
USER_QUOTES = {}

# Command: /myquotes
async def my_quotes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    quotes = USER_QUOTES.get(user_id, [])
    if quotes:
        msg = "Your quotes:\n" + '\n'.join(f"{i+1}. {q}" for i, q in enumerate(quotes))
        await update.message.reply_text(msg)
    else:
        await update.message.reply_text("You haven't added any quotes yet.")
# Command: /countquotes
async def count_quotes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"There are {len(QUOTES)} quotes available.")
# Command: /addquote <your quote>
async def add_quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text[len('/addquote '):].strip()
    if text:
        QUOTES.append(text)
        user_id = update.effective_user.id
        USER_QUOTES.setdefault(user_id, []).append(text)
        await update.message.reply_text("Quote added!")
    else:
        await update.message.reply_text("Please provide a quote after /addquote.")
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import random

# List of quotes
QUOTES = [
    "The best way to get started is to quit talking and begin doing. – Walt Disney",
    "Don’t let yesterday take up too much of today. – Will Rogers",
    "It’s not whether you get knocked down, it’s whether you get up. – Vince Lombardi",
    "If you are working on something exciting, it will keep you motivated. – Steve Jobs",
    "Success is not in what you have, but who you are. – Bo Bennett",
    "The harder you work for something, the greater you’ll feel when you achieve it.",
    "Dream bigger. Do bigger.",
    "Don’t watch the clock; do what it does. Keep going. – Sam Levenson",
    "Great things never come from comfort zones.",
    "Push yourself, because no one else is going to do it for you."
    ,"Opportunities don't happen, you create them. – Chris Grosser"
    ,"Success is not the key to happiness. Happiness is the key to success. – Albert Schweitzer"
    ,"The only place where success comes before work is in the dictionary. – Vidal Sassoon"
    ,"Don’t be afraid to give up the good to go for the great. – John D. Rockefeller"
    ,"I find that the harder I work, the more luck I seem to have. – Thomas Jefferson"
    ,"Success usually comes to those who are too busy to be looking for it. – Henry David Thoreau"
    ,"The way to get started is to quit talking and begin doing. – Walt Disney"
    ,"Don’t let what you cannot do interfere with what you can do. – John Wooden"
    ,"The future depends on what you do today. – Mahatma Gandhi"
    ,"It always seems impossible until it’s done. – Nelson Mandela"
]

def get_random_quote():
    return random.choice(QUOTES)

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to the Quote Generator Bot!\nSend /quote or any message to get a random quote."
    )

# Command: /quote
async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_random_quote())

# Message handler: reply with a random quote
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_random_quote())

def main():
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    application = ApplicationBuilder().token('YOUR_BOT_TOKEN').build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('quote', quote))
    application.add_handler(CommandHandler('addquote', add_quote))
    application.add_handler(CommandHandler('countquotes', count_quotes))
    application.add_handler(CommandHandler('myquotes', my_quotes))
    application.add_handler(CommandHandler('removequote', remove_quote))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Quote Generator Bot is alive! Waiting for messages...")
    application.run_polling()

# Uncomment to run directly
# if __name__ == '__main__':
#     main()
