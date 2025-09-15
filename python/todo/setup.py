#!/usr/bin/env python3
"""
Setup script for Enhanced Todo App with Telegram Bot
"""

import os
import sys
import subprocess
import json

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required!")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def setup_bot_config():
    """Setup bot configuration"""
    config_file = "bot_config.json"
    
    if os.path.exists(config_file):
        try:
            with open(config_file, "r") as f:
                config = json.load(f)
                if config.get("bot_token") != "YOUR_BOT_TOKEN_HERE":
                    print("✅ Bot configuration already set up!")
                    return True
        except (json.JSONDecodeError, IOError):
            pass
    
    print("\n🤖 Telegram Bot Setup:")
    print("To use the Telegram bot functionality:")
    print("1. Message @BotFather on Telegram")
    print("2. Send /newbot command")
    print("3. Follow the instructions to create your bot")
    print("4. Copy the bot token")
    print("5. Either:")
    print("   - Set TELEGRAM_BOT_TOKEN environment variable, or")
    print("   - Edit bot_config.json with your token")
    print("\nBot configuration is optional - you can use the desktop app without it!")

def create_sample_tasks():
    """Create sample tasks if none exist"""
    tasks_file = "tasks.json"
    if not os.path.exists(tasks_file):
        sample_tasks = [
            {"title": "Welcome to your Todo App!", "done": False},
            {"title": "Try adding a new task", "done": False},
            {"title": "Test the Telegram bot", "done": False}
        ]
        try:
            with open(tasks_file, "w", encoding="utf-8") as f:
                json.dump(sample_tasks, f, indent=2, ensure_ascii=False)
            print("✅ Sample tasks created!")
        except IOError as e:
            print(f"⚠️  Could not create sample tasks: {e}")

def main():
    """Main setup function"""
    print("🚀 Setting up Enhanced Todo App with Telegram Bot...")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Setup bot configuration
    setup_bot_config()
    
    # Create sample tasks
    create_sample_tasks()
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\nTo run the application:")
    print("• Desktop app: python todo.py")
    print("• Bot only: python todo.py --mode bot")
    print("• Help: python todo.py --help")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
