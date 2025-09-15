"""
Telegram Bot for Todo Management
Provides a Telegram bot interface for managing todo tasks
"""

import logging
import json
import os
from typing import List, Dict, Any
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

DATA_FILE = "tasks.json"

class TodoBot:
    def __init__(self, bot_token: str):
        """Initialize the Todo Bot with the provided token"""
        self.bot_token = bot_token
        self.application = Application.builder().token(bot_token).build()
        self.setup_handlers()
    
    def load_tasks(self) -> List[Dict[str, Any]]:
        """Load tasks from JSON file"""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                logger.error(f"Error loading tasks: {e}")
                return []
        return []
    
    def save_tasks(self, tasks: List[Dict[str, Any]]) -> None:
        """Save tasks to JSON file"""
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(tasks, f, indent=2, ensure_ascii=False)
        except IOError as e:
            logger.error(f"Error saving tasks: {e}")
    
    def setup_handlers(self) -> None:
        """Setup all bot command and message handlers"""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("list", self.list_tasks))
        self.application.add_handler(CommandHandler("add", self.add_task_command))
        self.application.add_handler(CommandHandler("done", self.mark_done_command))
        self.application.add_handler(CommandHandler("delete", self.delete_task_command))
        self.application.add_handler(CommandHandler("clear", self.clear_completed))
        
        # Callback query handler for inline buttons
        self.application.add_handler(CallbackQueryHandler(self.button_callback))
        
        # Message handler for adding tasks
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /start command"""
        welcome_message = """
🎯 *Welcome to Todo Bot!*

I can help you manage your tasks efficiently. Here are the available commands:

📋 `/list` - Show all tasks
➕ `/add <task>` - Add a new task
✅ `/done <number>` - Mark task as completed
🗑️ `/delete <number>` - Delete a task
🧹 `/clear` - Clear completed tasks
❓ `/help` - Show this help message

You can also just type a task description to add it quickly!

*Example:* `/add Buy groceries`
        """
        await update.message.reply_text(welcome_message, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /help command"""
        help_text = """
📚 *Todo Bot Commands:*

📋 `/list` - Show all your tasks
➕ `/add <task>` - Add a new task
✅ `/done <number>` - Mark task number as completed
🗑️ `/delete <number>` - Delete task number
🧹 `/clear` - Remove all completed tasks
❓ `/help` - Show this help

*Quick Add:* Just type your task description without any command!

*Examples:*
• `/add Call mom`
• `/done 2` (marks task #2 as done)
• `/delete 1` (deletes task #1)
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def list_tasks(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /list command"""
        tasks = self.load_tasks()
        
        if not tasks:
            await update.message.reply_text("📝 *No tasks found!*\n\nAdd a task using `/add <task>` or just type your task description.", parse_mode='Markdown')
            return
        
        message = "📋 *Your Tasks:*\n\n"
        keyboard_buttons = []
        
        for idx, task in enumerate(tasks, 1):
            status = "✅" if task["done"] else "⏳"
            message += f"{idx}. {task['title']} {status}\n"
            
            # Create inline buttons for each task
            if not task["done"]:
                keyboard_buttons.append([
                    InlineKeyboardButton(f"✅ Done #{idx}", callback_data=f"done_{idx-1}"),
                    InlineKeyboardButton(f"🗑️ Delete #{idx}", callback_data=f"delete_{idx-1}")
                ])
        
        # Add clear completed button if there are completed tasks
        completed_tasks = [task for task in tasks if task["done"]]
        if completed_tasks:
            keyboard_buttons.append([InlineKeyboardButton("🧹 Clear Completed", callback_data="clear_completed")])
        
        reply_markup = InlineKeyboardMarkup(keyboard_buttons) if keyboard_buttons else None
        
        await update.message.reply_text(message, parse_mode='Markdown', reply_markup=reply_markup)
    
    async def add_task_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /add command"""
        if not context.args:
            await update.message.reply_text("❌ Please provide a task description.\n\n*Usage:* `/add <task description>`", parse_mode='Markdown')
            return
        
        task_title = " ".join(context.args)
        await self.add_task(update, task_title)
    
    async def add_task(self, update: Update, task_title: str) -> None:
        """Add a new task"""
        tasks = self.load_tasks()
        tasks.append({"title": task_title, "done": False})
        self.save_tasks(tasks)
        
        await update.message.reply_text(f"✅ *Task added:* {task_title}\n\nUse `/list` to see all tasks.", parse_mode='Markdown')
    
    async def mark_done_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /done command"""
        if not context.args:
            await update.message.reply_text("❌ Please provide a task number.\n\n*Usage:* `/done <number>`", parse_mode='Markdown')
            return
        
        try:
            task_num = int(context.args[0])
            await self.mark_task_done(update, task_num)
        except ValueError:
            await update.message.reply_text("❌ Please provide a valid task number.", parse_mode='Markdown')
    
    async def mark_task_done(self, update: Update, task_num: int) -> None:
        """Mark a task as done"""
        tasks = self.load_tasks()
        
        if not tasks:
            await update.message.reply_text("📝 No tasks found!")
            return
        
        if 1 <= task_num <= len(tasks):
            tasks[task_num - 1]["done"] = True
            self.save_tasks(tasks)
            task_title = tasks[task_num - 1]["title"]
            await update.message.reply_text(f"✅ *Task completed:* {task_title}", parse_mode='Markdown')
        else:
            await update.message.reply_text(f"❌ Invalid task number. Please use 1-{len(tasks)}.", parse_mode='Markdown')
    
    async def delete_task_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /delete command"""
        if not context.args:
            await update.message.reply_text("❌ Please provide a task number.\n\n*Usage:* `/delete <number>`", parse_mode='Markdown')
            return
        
        try:
            task_num = int(context.args[0])
            await self.delete_task(update, task_num)
        except ValueError:
            await update.message.reply_text("❌ Please provide a valid task number.", parse_mode='Markdown')
    
    async def delete_task(self, update: Update, task_num: int) -> None:
        """Delete a task"""
        tasks = self.load_tasks()
        
        if not tasks:
            await update.message.reply_text("📝 No tasks found!")
            return
        
        if 1 <= task_num <= len(tasks):
            task_title = tasks[task_num - 1]["title"]
            del tasks[task_num - 1]
            self.save_tasks(tasks)
            await update.message.reply_text(f"🗑️ *Task deleted:* {task_title}", parse_mode='Markdown')
        else:
            await update.message.reply_text(f"❌ Invalid task number. Please use 1-{len(tasks)}.", parse_mode='Markdown')
    
    async def clear_completed(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /clear command"""
        tasks = self.load_tasks()
        original_count = len(tasks)
        
        # Remove completed tasks
        tasks = [task for task in tasks if not task["done"]]
        self.save_tasks(tasks)
        
        cleared_count = original_count - len(tasks)
        
        if cleared_count > 0:
            await update.message.reply_text(f"🧹 *Cleared {cleared_count} completed task(s)!*", parse_mode='Markdown')
        else:
            await update.message.reply_text("📝 No completed tasks to clear.", parse_mode='Markdown')
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle inline button callbacks"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data.startswith("done_"):
            task_idx = int(data.split("_")[1])
            await self.mark_task_done(query, task_idx + 1)
        elif data.startswith("delete_"):
            task_idx = int(data.split("_")[1])
            await self.delete_task(query, task_idx + 1)
        elif data == "clear_completed":
            await self.clear_completed(query, context)
        
        # Update the message with new task list
        await self.list_tasks(query, context)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle regular text messages as task additions"""
        task_title = update.message.text.strip()
        if task_title:
            await self.add_task(update, task_title)
    
    def run(self) -> None:
        """Start the bot"""
        logger.info("Starting Todo Bot...")
        self.application.run_polling()

def main():
    """Main function to run the bot"""
    # Get bot token from environment variable or config file
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not bot_token:
        # Try to load from config file
        config_file = "bot_config.json"
        if os.path.exists(config_file):
            try:
                with open(config_file, "r") as f:
                    config = json.load(f)
                    bot_token = config.get("bot_token")
            except (json.JSONDecodeError, IOError):
                pass
    
    if not bot_token:
        print("❌ Error: Telegram bot token not found!")
        print("Please set TELEGRAM_BOT_TOKEN environment variable or create bot_config.json")
        print("\nTo get a bot token:")
        print("1. Message @BotFather on Telegram")
        print("2. Send /newbot command")
        print("3. Follow the instructions")
        print("4. Copy the token and set it as environment variable or in bot_config.json")
        return
    
    try:
        bot = TodoBot(bot_token)
        bot.run()
    except Exception as e:
        logger.error(f"Error running bot: {e}")
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
