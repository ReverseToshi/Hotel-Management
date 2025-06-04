from sql import SQL
import tkinter as tk
from tkinter import ttk
import time
from Tab_pane import Tab_pane

class Application:
    """Main application class for the hotel management system."""
    def __init__(self):
        # Main window
        self.Parent = tk.Tk()
        self.Parent.title("Management")
        self.Parent.geometry("1100x650")
        self.Parent.resizable(0,0)


        # Menu ribbon
        self.menu_bar = tk.Menu(self.Parent)
        self.map_menu()
        self.Parent.config(menu=self.menu_bar) 
        self.menu_bar.config(bg="#72757a",
                             activebackground="#484a4d")
        
        # Layout
        self.wrapper = tk.Frame(self.Parent)
        self.wrapper.pack(fill="both", expand=True)

        # Header
        self.Header = tk.Label(self.wrapper, 
                                    bg="#2c3e50",
                                    fg="#ffffff",
                                    text="Hotel Management System",
                                    font=("Arial", 20, "bold")
                                    )
        self.Header.pack(fill="x")

        self.Pane = tk.PanedWindow(self.wrapper, orient="horizontal", sashwidth=2)
        

        # Panes
        self.left_pane()
        self.right_pane()

        # Footer (now inside wrapper, safely below pane)
        self.Footer = tk.LabelFrame(
            self.wrapper,
            bg="#2c3e50",
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.Footer.pack(fill="x", side="bottom")

        self.clock = tk.Label(self.Footer, text="HELLO", font=("Arial", 12), fg="white", bg="#2c3e50")
        self.clock.pack(side="right")
        self.update_clock()

        self.Pane.pack(fill="both", expand=True)
        
        self.Parent.mainloop()

    def left_pane(self):
        left = tk.Frame(self.Pane, bg="#9fa1a1", width=200)
        left.pack_propagate(False)
        # Top Frame
        top = tk.Frame(left, bg="#9fa1a1")
        QALabel = tk.Label(master=top, text="Quick Actions", font=("Arial", 14, "bold", "underline"), bg="#9fa1a1", height=0)
        QALabel.pack(padx =10, pady= 5)

        check_inBtn = tk.Button(top, text="Check-in Guest", bg="#548A75", activebackground="#69b595", borderwidth=0, font=("Arial", 12), width=100)
        check_inBtn.pack(padx=10, pady=5)

        check_outBtn = tk.Button(top, text="Check-out Guest", bg="#548A75", activebackground="#69b595", borderwidth=0, font=("Arial", 12), width=100)
        check_outBtn.pack(padx=10, pady=5)

        new_resBtn = tk.Button(top, text="New Reservation", bg="#548A75", activebackground="#69b595", borderwidth=0, font=("Arial", 12), width=100)
        new_resBtn.pack(padx=10, pady=5)
        
        # Bottom frame
        bottom = tk.Frame(left, bg="#9fa1a1")
        reportLabel = tk.Label(bottom, text="Reports", font=("Arial", 14, "bold","underline"), bg="#9fa1a1",height=0)
        reportLabel.pack(padx=10, pady=5)

        occupancyBtn = tk.Button(bottom, text="Occupancy Report", bg="#548A75", activebackground="#69b595", borderwidth=0, font=("Arial", 12), width=100)
        occupancyBtn.pack(padx=10, pady=5)
        
        RevenueBtn = tk.Button(bottom, text="Revenue Report", bg="#548A75", activebackground="#69b595", borderwidth=0, font=("Arial", 12), width=100)
        RevenueBtn.pack(padx=10, pady=5)
        
        GuestBtn = tk.Button(bottom, text="Guest Report", bg="#548A75", activebackground="#69b595", borderwidth=0, font=("Arial", 12), width=100)
        GuestBtn.pack(padx=10, pady=5)

        top.pack()
        ttk.Separator(left, orient="horizontal").pack(fill="x", pady=5)
        bottom.pack()
        self.Pane.add(left)

    def right_pane(self):
        right = tk.Frame(self.Pane, bg="#000000", width=900)
        tabs = Tab_pane(right)

        self.Pane.add(right)

    def map_menu(self):
        # File Menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Export report", command=self.hotel_info)
        file_menu.add_command(label="Backup Data")
        file_menu.add_separator()
        file_menu.add_command(label="Exit")

        # View Menu
        view_menu = tk.Menu(self.menu_bar, tearoff=0)
        view_menu.add_command(label="Refresh")
        view_menu.add_command(label="Settings")

        # Help Menu
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="App Info")
        help_menu.add_command(label="Hotel Info")
        help_menu.add_command(label="User Manual")


        self.menu_bar.add_cascade(label="File", menu=file_menu)
        self.menu_bar.add_cascade(label="View", menu=view_menu)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

    def hotel_info(self):
        info_window = tk.Toplevel(self.Parent)
        info_window.title("Hotel Information")

    def update_clock(self):
        current_time = time.strftime("%d-%m-%Y\t%H:%M:%S")
        self.clock.config(text=current_time)
        self.Parent.after(1000, self.update_clock)