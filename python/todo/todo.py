# To-Do App with Tkinter UI and persistent storage
import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

DATA_FILE = "tasks.json"

def load_tasks():
	if os.path.exists(DATA_FILE):
		with open(DATA_FILE, "r", encoding="utf-8") as f:
			return json.load(f)
	return []

def save_tasks(tasks):
	with open(DATA_FILE, "w", encoding="utf-8") as f:
		json.dump(tasks, f, indent=2)

class TodoApp:
	def __init__(self, root):
		self.root = root
		self.root.title("To-Do App")
		self.tasks = load_tasks()

		self.frame = tk.Frame(root)
		self.frame.pack(padx=10, pady=10)

		self.listbox = tk.Listbox(self.frame, width=40, height=10)
		self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)
		self.update_listbox()

		btn_frame = tk.Frame(self.frame)
		btn_frame.pack(side=tk.RIGHT, fill=tk.Y)

		tk.Button(btn_frame, text="Add Task", command=self.add_task).pack(fill=tk.X)
		tk.Button(btn_frame, text="Mark as Done", command=self.mark_done).pack(fill=tk.X)
		tk.Button(btn_frame, text="Delete Task", command=self.delete_task).pack(fill=tk.X)
		tk.Button(btn_frame, text="Exit", command=self.root.quit).pack(fill=tk.X)

	def update_listbox(self):
		self.listbox.delete(0, tk.END)
		for idx, task in enumerate(self.tasks):
			status = "✔" if task["done"] else "✗"
			self.listbox.insert(tk.END, f"{idx+1}. {task['title']} [{status}]")

	def add_task(self):
		title = simpledialog.askstring("Add Task", "Task description:")
		if title:
			self.tasks.append({"title": title, "done": False})
			save_tasks(self.tasks)
			self.update_listbox()

	def mark_done(self):
		sel = self.listbox.curselection()
		if not sel:
			messagebox.showwarning("No selection", "Select a task to mark as done.")
			return
		idx = sel[0]
		self.tasks[idx]["done"] = True
		save_tasks(self.tasks)
		self.update_listbox()

	def delete_task(self):
		sel = self.listbox.curselection()
		if not sel:
			messagebox.showwarning("No selection", "Select a task to delete.")
			return
		idx = sel[0]
		if messagebox.askyesno("Delete Task", f"Delete '{self.tasks[idx]['title']}'?"):
			del self.tasks[idx]
			save_tasks(self.tasks)
			self.update_listbox()

if __name__ == "__main__":
	root = tk.Tk()
	app = TodoApp(root)
	root.mainloop()
