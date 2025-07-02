from sql import SQL
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class Room:
    """This class is used to manage the room management window."""
    def __init__(self, window):
        """Initialize the room management window."""
        self.parent = window
        self.Frame = ttk.Frame(self.parent)
        self.con = SQL()
        self.fillFrame()
        self.Frame.pack(fill="both", expand=True)

    def fillFrame(self):
        """Fill the frame with the room management components."""
        # Create a PanedWindow to hold the top and bottom panes
        self.Pane = tk.PanedWindow(self.Frame, orient="vertical", border=3, sashwidth=2, bg="#000000")
        # Set the background color of the panes
        self.top_pane = tk.Frame(self.Pane, bg="#ffffff")
        self.bottom_pane = tk.Frame(self.Pane)
    
        # Create the top and bottom panes
        self.create_top()
        self.create_bottom()

        # Add the panes to the PanedWindow
        self.Pane.add(self.top_pane)
        self.Pane.add(self.bottom_pane)
        self.Pane.pack(fill="both", expand=True)

    def create_top(self):
        """Create the top pane with filter options."""
        tk.Label(self.top_pane, text="Filter by ", font=("Arial", 12), bg="#ffffff").pack(padx=5, pady=2, side="left")
        tk.Label(self.top_pane, text="Status:", font=("Arial", 12), bg="#ffffff").pack(padx=5, pady=2, side="left")

        # Create a Combobox for status selection
        self.statusVar = tk.StringVar()
        self.statusBox = ttk.Combobox(self.top_pane, textvariable=self.statusVar, values=["All Rooms", "Available", "Booked"], state="readonly")
        self.statusBox.pack(padx=5, pady=2, side="left")
        # Set the default value for the status combobox
        self.statusBox.current(0)
        # Bind the selection event to update the room list
        self.statusBox.bind("<<ComboboxSelected>>", self.status_select)

        # Create a Combobox for package selection
        tk.Label(self.top_pane, text="Package:", font=("Arial", 12), bg="#ffffff").pack(padx=5, pady=2, side="left")
        self.packageVar = tk.StringVar()
        self.packageBox = ttk.Combobox(self.top_pane, textvariable=self.packageVar, values=["All Rooms", "Standard", "Deluxe", "Executive", "Suite", "Presidential Suite"], state="readonly")
        self.packageBox.pack(padx=5, pady=2, side="left")
        self.packageBox.current(0)

        # Bind the selection event to update the room list
        self.packageBox.bind("<<ComboboxSelected>>", self.status_select)

        self.top_pane.pack()

    def status_select(self, event):
        """Update the room list based on the selected status and package."""
        self.Tree.fillTree(status=self.statusVar.get(), roomType=self.packageVar.get())

    def create_bottom(self):
        self.Tree = RoomList(self.bottom_pane, self.con)

class RoomList:
    """This class is used to display the list of rooms in a Treeview."""
    def __init__(self, parent, con):
        """Initialize the room list Treeview."""
        # Create the Treeview and scrollbar
        self.parent = parent
        self.tree = ttk.Treeview(self.parent)
        self.scrollbar = ttk.Scrollbar(self.parent, orient="vertical", command=self.tree.yview)
        self.define_columns()
        self.con = con
        self.scrollbar.pack(side="right",fill="y")
        self.tree.pack(fill="both", expand=True)
        self.tree.config(yscrollcommand=self.scrollbar.set)
        self.fillTree()

    def define_columns(self):
        """Define the columns for the Treeview."""
        # Define the columns for the Treeview
        self.tree["columns"]=("Room Number", "Package", "Price per night", "Availability")
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("Room Number", anchor=tk.CENTER, width=100)
        self.tree.column("Package", anchor=tk.CENTER, width=100)
        self.tree.column("Price per night", anchor=tk.CENTER, width=100)
        self.tree.column("Availability", anchor=tk.CENTER, width=100)

        # Set the headings for the columns
        self.tree.heading("#0", text="", anchor=tk.CENTER)
        self.tree.heading("Room Number", text="Room Number", anchor=tk.CENTER)
        self.tree.heading("Package", text="Package", anchor=tk.CENTER)
        self.tree.heading("Price per night", text="Price per night", anchor=tk.CENTER)
        self.tree.heading("Availability", text="Availability", anchor=tk.CENTER)

    def fillTree(self, status="All Rooms", roomType = "All Rooms"):
        """Fill the Treeview with room data based on the selected status and package."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        results = self.con.get_rooms(status=status, roomType = roomType)
        for row in results:
            roomID, room_type, price, roomStatus = row
            self.tree.insert("", "end", values=(roomID, room_type, price, roomStatus))
