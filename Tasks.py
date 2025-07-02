from sql import SQL
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime
from tkinter import messagebox

# Function to parse date from "dd/mm/yy" format to "YYYY-MM-DD"
def parse_date(date):
    """Converts a date string from 'dd/mm/yy' format to 'YYYY-MM-DD' format."""
    if not date:
        return ""
    # Ensure the date is in the correct format
    parse_date=datetime.strptime(date, "%d/%m/%y")
    # Return the date in "YYYY-MM-DD" format
    return parse_date.strftime("%Y-%m-%d")


class Task:
    """A class to manage tasks in a task management application."""
    def __init__(self, window):
        """Initializes the Task class with a parent window."""
        self.selected = None  # To keep track of the selected task
        self.parent = window
        # Create a frame to hold the task management interface
        self.Frame = ttk.Frame(self.parent)
        # Initialize the SQL connection
        self.con = SQL()
        self.fillFrame()
        self.Frame.pack(fill="both", expand=True)

    def fillFrame(self):
        """Fills the frame with a PanedWindow containing the task management interface."""
        # Create a PanedWindow to hold the top and bottom panes
        self.Pane = tk.PanedWindow(self.Frame, orient="vertical", border=3, sashwidth=2, bg="#000000")
        self.top_pane = tk.Frame(self.Pane, bg="#ffffff")
        self.bottom_pane = tk.Frame(self.Pane)

        # Create the top and bottom sections of the task management interface
        self.create_top()
        self.create_bottom()

        # Add the top and bottom panes to the PanedWindow
        self.Pane.add(self.top_pane)
        self.Pane.add(self.bottom_pane)
        self.Pane.pack(fill="both", expand=True)

    def create_top(self):
        """Creates the top section of the task management interface."""
        # Variables
        self.due_date_var = tk.StringVar()
        self.hour_var = tk.StringVar(value=datetime.now().strftime("%H"))
        self.minute_var = tk.StringVar(value=datetime.now().strftime("%M"))

        font_style = ("Arial", 10)

        # "Due:" Label
        tk.Label(self.top_pane, text="Due:", font=font_style, bg="#ffffff").grid(row=0, column=0, padx=5, pady=5, sticky="e")

        # DateEntry
        due_date_entry = DateEntry(
            self.top_pane,
            textvariable=self.due_date_var,
            font=font_style,
            width=12
        )
        due_date_entry.set_date(datetime.now().date())  # default to today
        due_date_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Hour Spinbox
        tk.Spinbox(
            self.top_pane,
            from_=0,
            to=23,
            textvariable=self.hour_var,
            width=3,
            font=font_style,
            format="%02.0f"
        ).grid(row=0, column=2, padx=(10, 2), pady=5)

        # ":" separator
        tk.Label(self.top_pane, text=":", font=font_style).grid(row=0, column=3)

        # Minute Spinbox
        tk.Spinbox(
            self.top_pane,
            from_=0,
            to=59,
            textvariable=self.minute_var,
            width=3,
            font=font_style,
            format="%02.0f"
        ).grid(row=0, column=4, padx=(2, 5), pady=5)

        # Optional: Add a Submit Button to test output (remove in final if not needed)
        def show_due_datetime():
            dateEntry = parse_date(self.due_date_var.get())
            timeEntry = self.hour_var.get()+":"+self.minute_var.get()+":00"
            self.tasks.fillTree(date=dateEntry, time=timeEntry)

        # Submit Button
        tk.Button(self.top_pane, text="Submit", font=font_style, command=show_due_datetime).grid(row=0, column=5, columnspan=1, pady=10)
        # Add Task Button
        tk.Button(self.top_pane, font=font_style, text="Add task", bg="#28a745", command=self.add_task).grid(row=0, column= 6, columnspan=1, pady=10, padx=10)
        # Edit Status Button
        self.edit_Btn = tk.Button(self.top_pane, font=font_style, text="Mark Completed/Pending", state="disabled", command=self.edit_status)
        self.edit_Btn.grid(row=0, column=7, columnspan=1, padx=10, pady=10)

    def create_bottom(self):
        self.tasks = TaskList(self.bottom_pane, self.con, self.due_date_var.get(), self.hour_var.get()+":"+self.minute_var.get(), self.on_select)

    def add_task(self):
        """Creates a new window to add a task."""
        # Create a new window for adding a task
        new_window = tk.Toplevel(self.parent)
        new_window.title("New Task")

        # Variables for task details
        descriptionVar = tk.StringVar()
        createdVar = tk.StringVar(value=datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
        dueDateVar = tk.StringVar()
        dueHourVar = tk.StringVar(value=datetime.now().strftime("%H"))
        dueMinVar = tk.StringVar(value=datetime.now().strftime("%M"))
        statusVar = tk.StringVar()

        # Set the due date to today's date
        def submit():
            """Submits the task details and adds the task to the database."""
            duedatetime = parse_date(dueDateVar.get())+" "+dueHourVar.get()+":"+dueMinVar.get()+":00"
            # Validate the due date and time
            if descriptionVar.get()=="":
                messagebox.showerror("No description", "Description is Empty")
                return
            
            if self.con.add_task(description=descriptionVar.get(), created=createdVar.get(), due=duedatetime, status=statusVar.get()):
                self.tasks.fillTree()
                new_window.destroy()
            else:
                messagebox.showerror("Failed to Add", "Failed to add the task")

        # Description
        tk.Label(new_window, text="Description:", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(new_window, textvariable=descriptionVar, font=("Arial", 10)).grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky="we")

        # Created At
        tk.Label(new_window, text="Created At:", font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Label(new_window, textvariable=createdVar, font=("Arial", 10)).grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="w")

        # Due Date and Time
        tk.Label(new_window, text="Due:", font=("Arial", 10)).grid(row=2, column=0, padx=5, pady=5, sticky="e")
        DateEntry(new_window, textvariable=dueDateVar, font=("Arial", 10)).grid(row=2, column=1, padx=2, pady=5, sticky="w")
        tk.Spinbox(new_window, from_=0, to=23, textvariable=dueHourVar, font=("Arial", 10), width=5).grid(row=2, column=2, padx=2, pady=5)
        tk.Spinbox(new_window, from_=0, to=59, textvariable=dueMinVar, font=("Arial", 10), width=5).grid(row=2, column=3, padx=2, pady=5)

        # Status
        tk.Label(new_window, text="Status:", font=("Arial", 10)).grid(row=3, column=0, padx=5, pady=5, sticky="e")
        combobox = ttk.Combobox(new_window, textvariable=statusVar, values=("Pending", "Completed"), font=("Arial", 10))
        combobox.current(0)
        combobox.grid(row=3, column=1, columnspan=3, padx=5, pady=5, sticky="we")

        # Submit Button
        tk.Button(new_window, text="Submit", command=submit, font=("Arial", 10)).grid(row=4, column=0, columnspan=4, padx=5, pady=10)

    def on_select(self, selected_row = None):
        """Handles the selection of a task in the task list."""
        if selected_row:
            # Enable the edit button if a task is selected
            self.edit_Btn.config(state="active")
            self.selected = selected_row
        else:
            # Disable the edit button if no task is selected
            self.edit_Btn.config(state="disabled")
            self.selected = selected_row

    def edit_status(self):
        """Edits the status of the selected task."""
        if self.selected[3]=="Pending":
            status="Completed"
        else:
            status="Pending"

        # Confirm the status change
        if self.con.change_status(self.selected[0], self.selected[1], self.selected[2], status=status):
            # Update the selected task in the task list
            self.tasks._unselect()
            self.on_select(None)
            dateEntry = parse_date(self.due_date_var.get())
            timeEntry = self.hour_var.get()+":"+self.minute_var.get()+":00"
            self.tasks.fillTree(date=dateEntry, time=timeEntry)


class TaskList:
    """A class to manage a list of tasks in a task management application."""
    def __init__(self, parent, con, date, time, callback):
        """Initializes the TaskList with a parent window, SQL connection, date, time, and a callback function."""
        self.parent = parent
        self.callback = callback
        # Create a Treeview widget to display tasks
        self.tree = ttk.Treeview(self.parent)
        # Create a vertical scrollbar for the Treeview
        self.scrollbar = ttk.Scrollbar(self.parent, orient="vertical", command=self.tree.yview)
        self.define_columns()
        # Set the style for the Treeview
        self.current_date = parse_date(date)
        self.current_time = time
        self.con = con
        self.scrollbar.pack(side="right",fill="y")
        self.tree.pack(fill="both", expand=True)
        self.tree.config(yscrollcommand=self.scrollbar.set)
        self.fillTree()
        # Bind the Treeview selection event to a handler
        self.tree.bind("<<TreeviewSelect>>", self._handle_selection)

    def define_columns(self):
        """Defines the columns for the Treeview widget."""
        # Define the columns for the Treeview
        self.tree["columns"]=("Description", "Created At", "Due", "Status")
        self.tree.column("#0",width=0, stretch=tk.NO)
        self.tree.column("Description", anchor="w", width=200)
        self.tree.column("Created At", anchor="center", width=100)
        self.tree.column("Due", anchor="center", width=100)
        self.tree.column("Status", anchor="center", width=100)

        # Set the headings for the columns
        self.tree.heading("#0",text="", anchor="center")
        self.tree.heading("Description", text="Description", anchor="w")
        self.tree.heading("Created At", text="Created At", anchor="center")
        self.tree.heading("Due", text="Due", anchor="center")
        self.tree.heading("Status", text="Status", anchor="center")

    def fillTree(self, date=None, time=None):
        """Fills the Treeview with tasks from the database."""
        # Clear the Treeview before filling it with new data
        for item in self.tree.get_children():
            self.tree.delete(item)
        # If no date is provided, use the current date
        if date==None:
            date=self.current_date
        tasks = self.con.get_tasks(date, time)
        # Insert tasks into the Treeview
        for task in tasks:
            description, created, due, status = task
            self.tree.insert("", "end", values=(description, created, due, status))

    def _handle_selection(self, event):
        """Handles the selection of a task in the Treeview."""
        selected_rows = self.tree.selection()
        # If a row is selected, get its values and call the callback function
        if selected_rows:
            values = self.tree.item(selected_rows[0], "values")
            self.callback(values)
        else:
            self.callback(None)

    def _unselect(self):
        self.tree.selection_set()
