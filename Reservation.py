from sql import SQL
import tkinter as tk
from tkinter import ttk
import tkcalendar as tkcal

class Reservation:
    def __init__(self, parent):
        self.parent = parent
        self.Frame = ttk.Frame(self.parent)
        self.con = SQL()
        self.fill_reservation()
        self.Frame.pack(fill="both", expand=True)

    def fill_reservation(self):
        self.PanedWindow = tk.PanedWindow(self.Frame, orient="vertical", border=3, bg="#111111", sashwidth=2)
        self.top_Pane = tk.PanedWindow(self.PanedWindow, orient="horizontal", border=1, sashwidth=0)
        self.bottom_Pane = tk.Frame(self.PanedWindow)   

        self.create_top_pane()
        self.create_bottom_pane()

        self.PanedWindow.add(self.top_Pane)
        self.PanedWindow.add(self.bottom_Pane)
        self.PanedWindow.pack(fill="both", expand=True)
        
    def create_top_pane(self):
        self.guest_frame = tk.Frame(self.top_Pane, bg="#ffffff", width=50)
        search_label = tk.Label(self.guest_frame, text="Search Guest:", font=("Arial", 12), bg="#ffffff", fg="#000000")
        search_label.pack(padx=5, pady=10, fill="x", expand=True, side="left") 
        self.guest_bar = tk.Entry(self.guest_frame, font=("Arial", 12), bg="#ffffff", fg="#000000")
        self.guest_bar.pack(padx=5, pady=10, fill="x", expand=True, side="left")
        self.searchBtn = tk.Button(self.guest_frame, text="Search", font=("Arial", 10), bg="#ffffff", fg="#000000", height=1)
        self.searchBtn.pack(padx=10, pady=10, expand=False, side = "right")

        self.guest_frame.pack(fill="both", expand=True)

        seperator = ttk.Separator(self.top_Pane, orient="vertical")
        seperator.pack(fill="x", padx=10, pady=5)

        self.filter_frame = tk.Frame(self.top_Pane, bg="#ffffff", width=50)
        filter_label = tk.Label(self.filter_frame, text="Filter by Date:", font=("Arial", 12), bg="#ffffff", fg="#000000")
        filter_label.pack(padx=5, pady=10, fill="x", expand=True, side="left")
        date_Var = tk.StringVar()
        self.date_entry = tkcal.DateEntry(self.filter_frame, textvariable=date_Var, font=("Arial", 12), background="#ffffff", foreground="#000000", borderwidth=2)
        self.date_entry.pack(padx=5, pady=10, fill="x", expand=True, side="left")

        self.clearBtn = tk.Button(self.filter_frame, text="Clear", font=("Arial", 10), bg="#ffffff", fg="#000000", height=1)
        self.clearBtn.pack(padx=10, pady=10, expand=False, side="right")
        self.filter_frame.pack(fill="both", expand=True)

        self.top_Pane.add(self.guest_frame)
        self.top_Pane.add(seperator)
        self.top_Pane.add(self.filter_frame)

    def create_bottom_pane(self):
        self.Treeview = ResList(self.bottom_Pane)

class ResList:
    def __init__(self, parent):
        self.parent = parent
        self.tree = ttk.Treeview(self.parent, columns=("ID", "Guest Name", "Room Number", "Check-in Date", "Check-out Date", "Status"), show="headings")
        