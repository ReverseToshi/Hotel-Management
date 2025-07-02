from tkinter import ttk
import tkinter as tk
from sql import SQL
from dashboard import Dashboard as Dash
from Reservation import Reservation as Res
from Room_management import Room
from Guest_management import Guest
from Tasks import Task

class Tab_pane:
    """Class to manage the main tab pane of the application."""
    def __init__(self, pane):
        """Initialize the Tab_pane with a parent pane."""
        self.Parent = pane
        # Create a Notebook widget to hold the tabs
        self.window = ttk.Notebook(self.Parent)
        self.window.pack(fill='both', expand=True)
        self.con = SQL()
        self.create_tabs()
        
    def create_tabs(self):
        """Create tabs for the application."""
        # Create instances of each tab's frame
        dashboard = Dash(self.window)
        reservation = Res(self.window)
        room_mgmt = Room(self.window)
        guest_mgmt = Guest(self.window)
        tasks = Task(self.window)

        # Add each frame to the Notebook as a tab
        self.window.add(dashboard.Frame, text="Dashboard")
        self.window.add(reservation.Frame, text="Reservations")
        self.window.add(room_mgmt.Frame, text="Room Management")
        self.window.add(guest_mgmt.Frame, text="Guest Management")
        self.window.add(tasks.Frame, text="Task Management")

    