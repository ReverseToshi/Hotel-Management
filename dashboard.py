from sql import SQL
import tkinter as tk
from tkinter import ttk

class Dashboard:
    """This class is used to create the dashboard frame in the main window."""
    def __init__(self, parent):
        """Initialize the dashboard frame."""
        self.parent = parent
        self.Frame = ttk.Frame(self.parent)
        self.con = SQL()
        self.fill_dashboard()
        self.Frame.pack(fill="both", expand=True)


    def fill_dashboard(self):
        """This method creates the dashboard layout with an overview of today's reservations and a list of pending tasks."""
        # Create the main frame for the dashboard
        self.Frame.pack_propagate(False)
        paned_window = tk.PanedWindow(self.Frame, orient="horizontal", border=3, sashwidth=2)
        # Create the overview section and pending tasks section
        overview_frame = tk.Frame(paned_window)
        ovHeader = tk.Label(overview_frame, text="Today's Overview", font=("Arial", 22,"bold"))
        ovHeader.pack(padx=10, pady=15, side="top", anchor="center")
        # Create labels for total rooms, occupied rooms, available rooms, and occupancy rate
        self.ttl_rooms = tk.Label(overview_frame, font=("Arial", 15))
        self.ttl_rooms.pack(padx=10, pady=5, anchor="center")
        self.occ_rooms = tk.Label(overview_frame, font=("Arial", 15))
        self.occ_rooms.pack(padx=10, pady=5, anchor="center")
        self.avl_rooms = tk.Label(overview_frame,  font=("Arial", 15))
        self.avl_rooms.pack(padx=10, pady=5, anchor="center")
        self.occ_rate = tk.Label(overview_frame,  font=("Arial", 15))
        self.occ_rate.pack(padx=10, pady=5, anchor="center")

        # Pack the overview frame and update the overview information
        overview_frame.pack()
        self.update_overview()

        # Create the pending tasks section
        pending = tk.Frame(paned_window)
        pendingLabel = tk.Label(pending, text="Pending tasks",font=("Arial", 22,"bold"))
        pendingLabel.pack(padx=10, pady=10)
        # Create a Listbox to display pending tasks
        self.pendingTasks = tk.Listbox(pending, width=250, height=300)
        self.pendingTasks.pack(padx=10, pady=10, fill="both")
        # Create a scrollbar for the Listbox
        scrollbar = tk.Scrollbar(self.Frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the Listbox to use the scrollbar
        self.pendingTasks.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.pendingTasks.yview)
        self.update_list()
        pending.pack()

        paned_window.add(overview_frame)
        paned_window.add(pending)
        paned_window.pack(fill="both", expand=True)

    def update_list(self):
        """Update the list of pending tasks every 2 seconds."""
        self.pendingTasks.delete(0, tk.END)
        # Fetch the pending tasks from the database
        tasks = self.con.get_tasks()
        # If there are no tasks, display a message
        if not tasks:
            self.pendingTasks.insert(tk.END, "No pending tasks")
            return
        # Insert each task into the Listbox
        for task in tasks:
            task_str = f"{task[0]} | Due: {task[2]}"
            self.pendingTasks.insert(tk.END ,task_str)
        self.parent.after(2000, self.update_list)

    def update_overview(self):
        """Update the overview information every second."""
        overview = self.con.get_overview()
        self.ttl_rooms.config(text=f"Total Rooms: {overview[0]}")
        self.occ_rooms.config(text=f"Occupied Rooms: {overview[1]}")
        self.avl_rooms.config(text=f"Available Rooms: {overview[2]}")
        self.occ_rate.config(text=f"Occupancy Rate: {overview[3]}%")
        # Schedule the next update
        self.parent.after(1000, self.update_overview)