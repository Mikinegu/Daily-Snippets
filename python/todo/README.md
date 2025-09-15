# Enhanced Todo App with Telegram Bot Integration

A comprehensive todo application that combines a modern desktop GUI with Telegram bot functionality for managing tasks from anywhere.

## Features

### Desktop GUI Features
- 📋 **Modern Interface**: Clean, intuitive desktop application with Tkinter
- ➕ **Add Tasks**: Easily add new tasks with descriptions
- ✅ **Mark Complete**: Mark tasks as done with visual indicators
- 🗑️ **Delete Tasks**: Remove unwanted tasks
- 🧹 **Clear Completed**: Bulk remove all completed tasks
- 📊 **Statistics**: Real-time task statistics in status bar
- 🤖 **Bot Integration**: Start/stop Telegram bot directly from GUI

### Telegram Bot Features
- 📱 **Mobile Access**: Manage tasks from your phone via Telegram
- 🎯 **Quick Commands**: Simple commands for all operations
- 🔘 **Inline Buttons**: Interactive buttons for task management
- 📋 **Smart Listing**: Organized task display with status indicators
- ⚡ **Instant Updates**: Real-time synchronization with desktop app

## Installation

### Prerequisites
- Python 3.7 or higher
- Telegram account (for bot functionality)

### Setup Steps

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Telegram Bot** (optional, for bot functionality):
   - Message [@BotFather](https://t.me/BotFather) on Telegram
   - Send `/newbot` command
   - Follow instructions to create your bot
   - Copy the bot token

4. **Configure Bot Token** (choose one method):
   
   **Method 1: Environment Variable**
   ```bash
   # Windows
   set TELEGRAM_BOT_TOKEN=your_bot_token_here
   
   # Linux/Mac
   export TELEGRAM_BOT_TOKEN=your_bot_token_here
   ```
   
   **Method 2: Configuration File**
   - Edit `bot_config.json`
   - Replace `YOUR_BOT_TOKEN_HERE` with your actual bot token

## Usage

### Desktop Application

**Run the GUI application**:
```bash
python todo.py
# or
python todo.py --mode gui
```

**Features**:
- Click "Add Task" to create new tasks
- Select a task and click "Mark Done" to complete it
- Select a task and click "Delete Task" to remove it
- Click "Clear Completed" to remove all finished tasks
- Click "Start Bot" to enable Telegram bot functionality
- View task statistics in the status bar

### Telegram Bot Only

**Run only the Telegram bot**:
```bash
python todo.py --mode bot
```

**Bot Commands**:
- `/start` - Welcome message and help
- `/help` - Show all available commands
- `/list` - Display all tasks with interactive buttons
- `/add <task>` - Add a new task
- `/done <number>` - Mark task number as completed
- `/delete <number>` - Delete task number
- `/clear` - Remove all completed tasks

**Quick Add**: Just type your task description (without any command) to add it quickly!

### Example Bot Usage

```
/start
/add Buy groceries
/add Call mom
/list
/done 1
/delete 2
/clear
```

## File Structure

```
python/todo/
├── todo.py              # Main application (GUI + Bot integration)
├── telegram_bot.py      # Telegram bot implementation
├── tasks.json           # Task storage (auto-created)
├── bot_config.json      # Bot configuration template
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Data Storage

Tasks are stored in `tasks.json` in JSON format:
```json
[
  {
    "title": "Task description",
    "done": false
  }
]
```

The same file is used by both the GUI and Telegram bot, ensuring data synchronization.

## Troubleshooting

### Common Issues

**"Missing Dependencies" Error**:
```bash
pip install -r requirements.txt
```

**"Bot Token Required" Error**:
- Make sure you've set the bot token correctly
- Check that `bot_config.json` contains a valid token
- Verify the token is from @BotFather

**Bot Not Responding**:
- Check your internet connection
- Verify the bot token is correct
- Make sure the bot is not blocked

**Tasks Not Syncing**:
- Both GUI and bot use the same `tasks.json` file
- Make sure both are not running simultaneously (unless intended)
- Check file permissions

### Getting Help

1. Check the console output for error messages
2. Verify all dependencies are installed
3. Ensure bot token is correctly configured
4. Check file permissions for `tasks.json`

## Advanced Usage

### Running Both GUI and Bot Simultaneously

You can run the desktop app and start the bot from within it:
1. Run `python todo.py`
2. Click "Start Bot" in the GUI
3. Use both interfaces simultaneously

### Customization

- Modify `telegram_bot.py` to add custom commands
- Update the GUI in `todo.py` for different layouts
- Change task storage format by modifying the JSON structure

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this application!

## License

This project is open source and available under the MIT License.
