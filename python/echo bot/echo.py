
import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters


# Replace 'YOUR_BOT_TOKEN' with your actual bot token
BOT_TOKEN = 'YOUR_BOT_TOKEN'

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='bot.log',
    filemode='a'
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    first_name = update.effective_user.first_name or "there"
    greet = f"Hello, {first_name}! Send me any message and I'll echo it back. Use /help to see available commands."
    await update.message.reply_text(greet)
    logger.info(f"/start used by {first_name} (id: {update.effective_user.id})")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "Available commands:\n"
        "/start - Welcome message\n"
        "/help - Show this help message\n"
        "Just send any message and I'll echo it back!"
    )
    await update.message.reply_text(help_text)
    logger.info(f"/help used by {update.effective_user.first_name} (id: {update.effective_user.id})")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text
    await update.message.reply_text(text)
    logger.info(f"Echoed message from {user.first_name} (id: {user.id}): {text}")



def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("Bot is running...")
    try:
        app.run_polling()
    except Exception as e:
        logger.error(f"Bot crashed: {e}")

if __name__ == '__main__':
    main()