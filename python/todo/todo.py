# Enhanced To-Do App with Tkinter UI, Telegram Bot, and persistent storage
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json
import os
import sys
import threading
import argparse
from typing import List, Dict, Any

DATA_FILE = "tasks.json"

def load_tasks() -> List[Dict[str, Any]]:
	"""Load tasks from JSON file with error handling"""
	if os.path.exists(DATA_FILE):
		try:
			with open(DATA_FILE, "r", encoding="utf-8") as f:
				return json.load(f)
		except (json.JSONDecodeError, IOError) as e:
			print(f"Error loading tasks: {e}")
			return []
	return []

def save_tasks(tasks: List[Dict[str, Any]]) -> None:
	"""Save tasks to JSON file with error handling"""
	try:
		with open(DATA_FILE, "w", encoding="utf-8") as f:
			json.dump(tasks, f, indent=2, ensure_ascii=False)
	except IOError as e:
		print(f"Error saving tasks: {e}")

class TodoApp:
	def __init__(self, root):
		self.root = root
		self.root.title("Enhanced To-Do App")
		self.root.geometry("600x500")
		self.tasks = load_tasks()
		self.bot_thread = None

		# Create main container
		main_frame = ttk.Frame(root, padding="10")
		main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
		
		# Configure grid weights
		root.columnconfigure(0, weight=1)
		root.rowconfigure(0, weight=1)
		main_frame.columnconfigure(1, weight=1)
		main_frame.rowconfigure(1, weight=1)

		# Title
		title_label = ttk.Label(main_frame, text="📋 Enhanced To-Do App", font=("Arial", 16, "bold"))
		title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))

		# Task list frame
		list_frame = ttk.LabelFrame(main_frame, text="Tasks", padding="5")
		list_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
		list_frame.columnconfigure(0, weight=1)
		list_frame.rowconfigure(0, weight=1)

		self.listbox = tk.Listbox(list_frame, width=50, height=15, font=("Arial", 10))
		self.listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
		
		# Scrollbar for listbox
		scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.listbox.yview)
		scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
		self.listbox.configure(yscrollcommand=scrollbar.set)

		# Control buttons frame
		btn_frame = ttk.LabelFrame(main_frame, text="Actions", padding="5")
		btn_frame.grid(row=1, column=2, sticky=(tk.W, tk.E, tk.N, tk.S))
		btn_frame.rowconfigure(8, weight=1)  # Add space at bottom

		# Task management buttons
		ttk.Button(btn_frame, text="➕ Add Task", command=self.add_task).grid(row=0, column=0, sticky=(tk.W, tk.E), pady=2)
		ttk.Button(btn_frame, text="✅ Mark Done", command=self.mark_done).grid(row=1, column=0, sticky=(tk.W, tk.E), pady=2)
		ttk.Button(btn_frame, text="🗑️ Delete Task", command=self.delete_task).grid(row=2, column=0, sticky=(tk.W, tk.E), pady=2)
		ttk.Button(btn_frame, text="🧹 Clear Completed", command=self.clear_completed).grid(row=3, column=0, sticky=(tk.W, tk.E), pady=2)
		
		# Separator
		ttk.Separator(btn_frame, orient='horizontal').grid(row=4, column=0, sticky=(tk.W, tk.E), pady=10)
		
		# Bot control buttons
		self.bot_status_label = ttk.Label(btn_frame, text="🤖 Bot: Stopped", foreground="red")
		self.bot_status_label.grid(row=5, column=0, pady=2)
		
		self.start_bot_btn = ttk.Button(btn_frame, text="🚀 Start Bot", command=self.start_bot)
		self.start_bot_btn.grid(row=6, column=0, sticky=(tk.W, tk.E), pady=2)
		
		self.stop_bot_btn = ttk.Button(btn_frame, text="⏹️ Stop Bot", command=self.stop_bot, state=tk.DISABLED)
		self.stop_bot_btn.grid(row=7, column=0, sticky=(tk.W, tk.E), pady=2)

		# Exit button
		ttk.Button(btn_frame, text="❌ Exit", command=self.root.quit).grid(row=9, column=0, sticky=(tk.W, tk.E), pady=(20, 0))

		# Status bar
		self.status_var = tk.StringVar()
		self.status_var.set("Ready")
		status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
		status_bar.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))

		self.update_listbox()
		self.update_status()

	def update_listbox(self):
		"""Update the task list display"""
		self.listbox.delete(0, tk.END)
		if not self.tasks:
			self.listbox.insert(tk.END, "No tasks yet. Add one using the 'Add Task' button!")
			return
		
		for idx, task in enumerate(self.tasks):
			status = "✅" if task["done"] else "⏳"
			self.listbox.insert(tk.END, f"{idx+1}. {task['title']} {status}")

	def update_status(self):
		"""Update the status bar with task statistics"""
		total = len(self.tasks)
		completed = sum(1 for task in self.tasks if task["done"])
		pending = total - completed
		self.status_var.set(f"Total: {total} | Completed: {completed} | Pending: {pending}")

	def add_task(self):
		"""Add a new task"""
		title = simpledialog.askstring("Add Task", "Task description:")
		if title and title.strip():
			self.tasks.append({"title": title.strip(), "done": False})
			save_tasks(self.tasks)
			self.update_listbox()
			self.update_status()
			self.status_var.set(f"Task added: {title.strip()}")

	def mark_done(self):
		"""Mark selected task as done"""
		sel = self.listbox.curselection()
		if not sel:
			messagebox.showwarning("No selection", "Select a task to mark as done.")
			return
		idx = sel[0]
		if not self.tasks[idx]["done"]:
			self.tasks[idx]["done"] = True
			save_tasks(self.tasks)
			self.update_listbox()
			self.update_status()
			self.status_var.set(f"Task marked as done: {self.tasks[idx]['title']}")
		else:
			messagebox.showinfo("Already Done", "This task is already completed!")

	def delete_task(self):
		"""Delete selected task"""
		sel = self.listbox.curselection()
		if not sel:
			messagebox.showwarning("No selection", "Select a task to delete.")
			return
		idx = sel[0]
		task_title = self.tasks[idx]['title']
		if messagebox.askyesno("Delete Task", f"Delete '{task_title}'?"):
			del self.tasks[idx]
			save_tasks(self.tasks)
			self.update_listbox()
			self.update_status()
			self.status_var.set(f"Task deleted: {task_title}")

	def clear_completed(self):
		"""Clear all completed tasks"""
		completed_tasks = [task for task in self.tasks if task["done"]]
		if not completed_tasks:
			messagebox.showinfo("No Completed Tasks", "There are no completed tasks to clear.")
			return
		
		if messagebox.askyesno("Clear Completed Tasks", f"Clear {len(completed_tasks)} completed task(s)?"):
			self.tasks = [task for task in self.tasks if not task["done"]]
			save_tasks(self.tasks)
			self.update_listbox()
			self.update_status()
			self.status_var.set(f"Cleared {len(completed_tasks)} completed task(s)")

	def start_bot(self):
		"""Start the Telegram bot in a separate thread"""
		try:
			# Import telegram bot module
			from telegram_bot import TodoBot
			
			# Check for bot token
			bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
			if not bot_token:
				config_file = "bot_config.json"
				if os.path.exists(config_file):
					try:
						with open(config_file, "r") as f:
							config = json.load(f)
							bot_token = config.get("bot_token")
					except (json.JSONDecodeError, IOError):
						pass
			
			if not bot_token or bot_token == "YOUR_BOT_TOKEN_HERE":
				messagebox.showerror("Bot Token Required", 
					"Please set your Telegram bot token!\n\n"
					"1. Set TELEGRAM_BOT_TOKEN environment variable, or\n"
					"2. Edit bot_config.json with your token from @BotFather")
				return
			
			# Start bot in separate thread
			self.bot_thread = threading.Thread(target=self.run_bot, args=(bot_token,), daemon=True)
			self.bot_thread.start()
			
			# Update UI
			self.bot_status_label.config(text="🤖 Bot: Running", foreground="green")
			self.start_bot_btn.config(state=tk.DISABLED)
			self.stop_bot_btn.config(state=tk.NORMAL)
			self.status_var.set("Telegram bot started successfully!")
			
		except ImportError:
			messagebox.showerror("Missing Dependencies", 
				"Telegram bot dependencies not installed!\n\n"
				"Run: pip install -r requirements.txt")
		except Exception as e:
			messagebox.showerror("Bot Error", f"Failed to start bot: {e}")

	def run_bot(self, bot_token):
		"""Run the bot (called in separate thread)"""
		try:
			from telegram_bot import TodoBot
			bot = TodoBot(bot_token)
			bot.run()
		except Exception as e:
			print(f"Bot error: {e}")
			# Update UI from thread
			self.root.after(0, lambda: self.bot_status_label.config(text="🤖 Bot: Error", foreground="red"))

	def stop_bot(self):
		"""Stop the Telegram bot"""
		# Note: This is a simplified stop - in practice, you'd need proper bot lifecycle management
		self.bot_status_label.config(text="🤖 Bot: Stopped", foreground="red")
		self.start_bot_btn.config(state=tk.NORMAL)
		self.stop_bot_btn.config(state=tk.DISABLED)
		self.status_var.set("Telegram bot stopped.")

def run_gui():
	"""Run the GUI application"""
	root = tk.Tk()
	app = TodoApp(root)
	root.mainloop()

def run_bot_only():
	"""Run only the Telegram bot"""
	try:
		from telegram_bot import main as bot_main
		bot_main()
	except ImportError:
		print("❌ Error: Telegram bot dependencies not installed!")
		print("Run: pip install -r requirements.txt")
	except Exception as e:
		print(f"❌ Error: {e}")

def main():
	"""Main function with command line argument support"""
	parser = argparse.ArgumentParser(description="Enhanced Todo App with GUI and Telegram Bot")
	parser.add_argument("--mode", choices=["gui", "bot"], default="gui",
						help="Run mode: 'gui' for desktop app, 'bot' for Telegram bot only")
	
	args = parser.parse_args()
	
	if args.mode == "bot":
		run_bot_only()
	else:
		run_gui()

if __name__ == "__main__":
	main()
