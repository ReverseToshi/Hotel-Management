from sql import SQL
import tkinter as tk
from tkinter import ttk

class Dashboard:
    def __init__(self, parent):
        self.parent = parent
        self.Frame = ttk.Frame(self.parent)
        self.con = SQL()
        self.fill_dashboard()
        self.Frame.pack(fill="both", expand=True)


    def fill_dashboard(self):
        paned_window = tk.PanedWindow(self.Frame, orient="horizontal", border=3, sashwidth=2)
        overview_frame = tk.Frame(paned_window)
        ovHeader = tk.Label(overview_frame, text="Today's Overview", font=("Arial", 22,"bold"))
        ovHeader.pack(padx=10, pady=15, side="top", anchor="center")
        self.ttl_rooms = tk.Label(overview_frame, font=("Arial", 15))
        self.ttl_rooms.pack(padx=10, pady=5, anchor="center")
        self.occ_rooms = tk.Label(overview_frame, font=("Arial", 15))
        self.occ_rooms.pack(padx=10, pady=5, anchor="center")
        self.avl_rooms = tk.Label(overview_frame,  font=("Arial", 15))
        self.avl_rooms.pack(padx=10, pady=5, anchor="center")
        self.occ_rate = tk.Label(overview_frame,  font=("Arial", 15))
        self.occ_rate.pack(padx=10, pady=5, anchor="center")

        overview_frame.pack()
        self.update_overview()

        pending = tk.Frame(paned_window)
        pendingLabel = tk.Label(pending, text="Pending tasks",font=("Arial", 22,"bold"))
        pendingLabel.pack(padx=10, pady=10)
        self.pendingTasks = tk.Listbox(pending, width=250, height=300)
        self.pendingTasks.pack(padx=10, pady=10, fill="both")

        scrollbar = tk.Scrollbar(self.Frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.pendingTasks.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.pendingTasks.yview)
        self.update_list()
        pending.pack()

        paned_window.add(overview_frame)
        paned_window.add(pending)
        paned_window.pack(fill="both", expand=True)

    def update_list(self):
        self.pendingTasks.delete(0, tk.END)
        tasks = self.con.get_tasks()
        for task in tasks:
            task_str = f"{task[0]} | Due: {task[2]}"
            self.pendingTasks.insert(tk.END ,task_str)
        self.parent.after(2000, self.update_list)

    def update_overview(self):
        overview = self.con.get_overview()
        self.ttl_rooms.config(text=f"Total Rooms: {overview[0]}")
        self.occ_rooms.config(text=f"Occupied Rooms: {overview[1]}")
        self.avl_rooms.config(text=f"Available Rooms: {overview[2]}")
        self.occ_rate.config(text=f"Occupancy Rate: {overview[3]}%")
        self.parent.after(1000, self.update_overview)