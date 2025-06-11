from sql import SQL
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class Room:
    def __init__(self, window):
        self.parent = window
        self.Frame = ttk.Frame(self.parent)
        self.con = SQL()
        self.fillFrame()
        self.Frame.pack(fill="both", expand=True)

    def fillFrame(self):
        self.Pane = tk.PanedWindow(self.Frame, orient="vertical", border=3, sashwidth=2, bg="#000000")
        self.top_pane = tk.Frame(self.Pane, bg="#ffffff")
        self.bottom_pane = tk.Frame(self.Pane)

        self.create_top()
        self.create_bottom()

        self.Pane.add(self.top_pane)
        self.Pane.add(self.bottom_pane)
        self.Pane.pack(fill="both", expand=True)

    def create_top(self):
        tk.Label(self.top_pane, text="Filter by ", font=("Arial", 12), bg="#ffffff").pack(padx=5, pady=2, side="left")
        tk.Label(self.top_pane, text="Status:", font=("Arial", 12), bg="#ffffff").pack(padx=5, pady=2, side="left")

        self.statusVar = tk.StringVar()
        self.statusBox = ttk.Combobox(self.top_pane, textvariable=self.statusVar, values=["All Rooms", "Available", "Booked"], state="readonly")
        self.statusBox.pack(padx=5, pady=2, side="left")
        self.statusBox.current(0)

        self.statusBox.bind("<<ComboboxSelected>>", self.status_select)

        tk.Label(self.top_pane, text="Package:", font=("Arial", 12), bg="#ffffff").pack(padx=5, pady=2, side="left")
        self.packageVar = tk.StringVar()
        self.packageBox = ttk.Combobox(self.top_pane, textvariable=self.packageVar, values=["All Rooms", "Standard", "Deluxe", "Executive", "Suite", "Presidential Suite"], state="readonly")
        self.packageBox.pack(padx=5, pady=2, side="left")
        self.packageBox.current(0)

        self.packageBox.bind("<<ComboboxSelected>>", self.status_select)

        self.top_pane.pack()

    def status_select(self, event):
        self.Tree.fillTree(status=self.statusVar.get(), roomType=self.packageVar.get())

    def create_bottom(self):
        self.Tree = RoomList(self.bottom_pane, self.con)

class RoomList:
    def __init__(self, parent, con):
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
        self.tree["columns"]=("Room Number", "Package", "Price per night", "Availability")
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("Room Number", anchor=tk.CENTER, width=100)
        self.tree.column("Package", anchor=tk.CENTER, width=100)
        self.tree.column("Price per night", anchor=tk.CENTER, width=100)
        self.tree.column("Availability", anchor=tk.CENTER, width=100)

        self.tree.heading("#0", text="", anchor=tk.CENTER)
        self.tree.heading("Room Number", text="Room Number", anchor=tk.CENTER)
        self.tree.heading("Package", text="Package", anchor=tk.CENTER)
        self.tree.heading("Price per night", text="Price per night", anchor=tk.CENTER)
        self.tree.heading("Availability", text="Availability", anchor=tk.CENTER)

    def fillTree(self, status="All Rooms", roomType = "All Rooms"):
        for item in self.tree.get_children():
            self.tree.delete(item)
        results = self.con.get_rooms(status=status, roomType = roomType)
        for row in results:
            roomID, room_type, price, roomStatus = row
            self.tree.insert("", "end", values=(roomID, room_type, price, roomStatus))
