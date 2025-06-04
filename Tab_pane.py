from tkinter import ttk
import tkinter as tk
from sql import SQL
from Dashboard import Dashboard as Dash
from Reservation import Reservation as Res

class Tab_pane:
    def __init__(self, pane):
        self.Parent = pane

        self.window = ttk.Notebook(self.Parent)
        self.window.pack(fill='both', expand=True)
        self.con = SQL()
        self.create_tabs()
        
    def create_tabs(self):
        dashboard = Dash(self.window)
        reservation = Res(self.window)
        room_mgmt = ttk.Frame(self.window)
        guest_mgmt = ttk.Frame(self.window)
        tasks = ttk.Frame(self.window)

        self.window.add(dashboard.Frame, text="Dashboard")
        self.window.add(reservation.Frame, text="Reservations")
        self.window.add(room_mgmt, text="Room Management")
        self.window.add(guest_mgmt, text="Guest Management")
        self.window.add(tasks, text="Task Management")

    