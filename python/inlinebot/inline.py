import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Replace with your bot token
BOT_TOKEN = 'YOUR_BOT_TOKEN'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Sample Text 1", callback_data='btn1')],
        [InlineKeyboardButton("Sample Text 2", callback_data='btn2')],
        [InlineKeyboardButton("Open Google", url='https://google.com')],
        [InlineKeyboardButton("Switch Inline Query", switch_inline_query='dummy inline query')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Choose an option:", reply_markup=reply_markup
    )
    logger.info(f"/start used by {update.effective_user.first_name} (id: {update.effective_user.id})")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'btn1':
        await query.edit_message_text(text="You pressed Sample Text 1!")
    elif query.data == 'btn2':
        await query.edit_message_text(text="You pressed Sample Text 2!")
    else:
        await query.edit_message_text(text=f"Unknown button: {query.data}")
    logger.info(f"Button pressed: {query.data} by {update.effective_user.first_name} (id: {update.effective_user.id})")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Inline bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
