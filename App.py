from tkinter import messagebox
from sql import SQL
import tkinter as tk
from tkinter import ttk
import time
from Tab_pane import Tab_pane
from datetime import datetime
from tkcalendar import DateEntry
from Tasks import parse_date

class Application:
    """Main application class for the hotel management system."""
    def __init__(self):
        # Main window
        self.Parent = tk.Tk()
        self.Parent.title("Management")
        self.Parent.geometry("1100x650")
        self.Parent.resizable(0,0)
        self.con = SQL()
        self.font = ("Arial", 12)

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

        check_inBtn = tk.Button(top, text="Check-in Guest", bg="#548A75", activebackground="#69b595", borderwidth=0, font=("Arial", 12), width=100, command=self.check_in)
        check_inBtn.pack(padx=10, pady=5)

        check_outBtn = tk.Button(top, text="Check-out Guest", bg="#548A75", activebackground="#69b595", borderwidth=0, font=("Arial", 12), width=100, command=self.check_out)
        check_outBtn.pack(padx=10, pady=5)

        new_resBtn = tk.Button(top, text="New Reservation", bg="#548A75", activebackground="#69b595", borderwidth=0, font=("Arial", 12), width=100, command=self.make_reservation)
        new_resBtn.pack(padx=10, pady=5)
        
        # Bottom frame
        bottom = tk.Frame(left, bg="#9fa1a1")
        reportLabel = tk.Label(bottom, text="Reports", font=("Arial", 14, "bold","underline"), bg="#9fa1a1",height=0)
        reportLabel.pack(padx=10, pady=5)

        occupancyBtn = tk.Button(bottom, text="Occupancy Report", bg="#548A75", activebackground="#69b595", borderwidth=0, font=("Arial", 12), width=100, command=self.occupancy)
        occupancyBtn.pack(padx=10, pady=5)
        
        RevenueBtn = tk.Button(bottom, text="Revenue Report", bg="#548A75", activebackground="#69b595", borderwidth=0, font=("Arial", 12), width=100, command=self.revenue)
        RevenueBtn.pack(padx=10, pady=5)
        
        GuestBtn = tk.Button(bottom, text="Guest Report", bg="#548A75", activebackground="#69b595", borderwidth=0, font=("Arial", 12), width=100, command=self.guest_report)
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

    def check_out(self):
        window = tk.Toplevel(self.Parent)

        tk.Label(window, text="Reservation ID:", font=self.font).grid(column=0, row=0, padx=5, pady=5, sticky="e")

        idVar = tk.StringVar()
        customerVar = tk.StringVar()
        roomVar= tk.StringVar()
        checkinVar = tk.StringVar()
        checkOutVar = tk.StringVar()
        priceVar = tk.DoubleVar()

        def on_select(event):
            row = self.con.get_reservations(reservationID=idVar.get())[0]
            customerVar.set(row[1])
            roomVar.set(row[2])
            checkinVar.set(row[3])

        reservationIDs = ttk.Combobox(window, textvariable=idVar, values=self.con.get_reservation_id_for_checkout())
        reservationIDs.grid(row=0, column=1, pady=5, sticky="we")
        reservationIDs.bind("<<ComboboxSelected>>", on_select)
        
        tk.Label(window, text="Customer ID: ", font=self.font).grid(column=0, row=1, padx=5, pady=5, sticky="e")
        tk.Entry(window, textvariable=customerVar, state="readonly", font=self.font).grid(column=1, row=1, sticky="we")

        tk.Label(window, font=self.font, text="Room ID: ").grid(column=0, row=2, padx=5, pady=5, sticky="e")
        tk.Entry(window, textvariable=roomVar, state="readonly", font=self.font).grid(row=2, column=1, pady=5, sticky="we")

        tk.Label(window, text="Check-In:", font=self.font).grid(column=0, row=3, padx=5, pady=5, sticky="e")
        tk.Entry(window, textvariable=checkinVar, font=self.font, state="readonly").grid(column=1, row=3, pady=5, sticky="we")

        tk.Label(window,text="Check-Out: ", font=self.font).grid(column=0, row=4, padx=5, pady=5, sticky="e")
        DateEntry(window, textvariable=checkOutVar, font=self.font).grid(column = 1, row=4, pady=5, sticky="we")

        def calculate_cost():
            check_in_time = datetime.strptime(checkinVar.get(), "%d-%m-%Y")
            check_out_time = datetime.strptime(checkOutVar.get(), "%d/%m/%y")
            total_time = check_out_time-check_in_time
            days = total_time.days+1
            price = self.con.get_price(roomVar.get())[0]
            cost = price*days
            priceVar.set(cost)

        tk.Label(window, text="Total Cost: ", font=self.font).grid(column=0, row=5, padx=5, pady=5, sticky="e")
        tk.Entry(window, textvariable=priceVar, font=self.font, state="readonly").grid(column=1, row=5, pady=5)
        tk.Button(window, text="Calculate Total", font=self.font, command=calculate_cost).grid(column=2, row=5, padx=5, pady=5, sticky="we")

        def finish_checkout():
            self.con.check_out(reservationID=idVar.get(), check_out=checkOutVar.get())
            window.destroy()
                
        tk.Button(window, text="Check-Out", font=self.font, command=finish_checkout).grid(column=0, row=6, sticky="e", padx=5, pady=5)

    def check_in(self):
        window = tk.Toplevel(self.Parent)

        idVar = tk.StringVar()          # Actual reservation ID (readonly)
        customerVar = tk.StringVar()
        roomVar = tk.StringVar()
        checkinVar = tk.StringVar()

        def on_select(event):
            reservation_id = idVar.get()
            row = self.con.get_reservations(reservationID=reservation_id)[0]
            idVar.set(row[0])
            customerVar.set(row[1])
            roomVar.set(row[2])

        # Reservation selector (dropdown)
        tk.Label(window, text="Select Reservation:", font=self.font).grid(column=0, row=0, padx=5, pady=5, sticky="e")
        reservation_selector = ttk.Combobox(window, textvariable=idVar, values=self.con.get_reservation_id_for_checkin(), font=self.font)
        reservation_selector.grid(row=0, column=1, sticky="we", pady=5)
        reservation_selector.bind("<<ComboboxSelected>>", on_select)

        tk.Label(window, text="Customer ID:", font=self.font).grid(column=0, row=2, padx=5, pady=5, sticky="e")
        tk.Entry(window, textvariable=customerVar, state="readonly", font=self.font).grid(column=1, row=2, sticky="we")

        tk.Label(window, text="Room ID:", font=self.font).grid(column=0, row=3, padx=5, pady=5, sticky="e")
        tk.Entry(window, textvariable=roomVar, state="readonly", font=self.font).grid(column=1, row=3, pady=5, sticky="we")

        tk.Label(window, text="Check-In:", font=self.font).grid(column=0, row=4, padx=5, pady=5, sticky="e")
        DateEntry(window, textvariable=checkinVar, font=self.font, state="readonly").grid(column=1, row=4, pady=5, sticky="we")
        checkinVar.set(datetime.now().strftime("%d/%m/%y"))

        def submit_checkin():
            self.con.check_in(reservationID=idVar.get(), check_in=parse_date(checkinVar.get()))
            window.destroy()

        tk.Button(window, text="Check-In", font=self.font, command=submit_checkin).grid(column=0, row=5, columnspan=2, pady=10)

    def make_reservation(self):
        window = tk.Toplevel(self.Parent)
        idVar = tk.StringVar(value=self.con.get_next_reservation_id())
        customerVar = tk.StringVar()
        roomIDVar= tk.StringVar()
        roomTypeVar = tk.StringVar()

        customers = self.con.get_guests()
        customers = [customer[0] for customer in customers]

        tk.Label(window, text="Reservation ID:", font=self.font).grid(column=0, row=0, padx=5, pady=5, sticky="e")
        tk.Entry(window, textvariable=idVar, state="readonly", font=self.font).grid(column=1, row=0, sticky="we")

        tk.Label(window, text="Customer ID:", font=self.font).grid(column=0, row=1, padx=5, pady=5, sticky="e")
        customerBox = ttk.Combobox(window, textvariable=customerVar, font=self.font, values=customers)
        customerBox.grid(column=1, row=1, sticky="we")

        def on_type(event):
            rooms = self.con.get_rooms(status="Available", roomType=roomTypeVar.get())
            roomIDs = [room[0] for room in rooms]
            roomID["values"]=roomIDs
            roomID.set(roomIDs[0])
        
        tk.Label(window, text="Room Type:", font=self.font).grid(column=0, row=2, padx=5, pady=5, sticky="e")
        roomType = ttk.Combobox(window, textvariable=roomTypeVar, font=self.font, values=("Standard", "Deluxe", "Executive", "Suite", "Presidential Suite"))
        roomType.grid(column=1, row=2, sticky="we")
        roomType.bind("<<ComboboxSelected>>", on_type)

        tk.Label(window, text="Room ID:", font=self.font).grid(column=0, row=3, padx=5, pady=5, sticky="e")
        roomID = ttk.Combobox(window, textvariable=roomIDVar, font=self.font)
        roomID.grid(column=1, row=3, sticky="we")

        def on_submit():
            if customerVar.get() == "":
                messagebox.showerror("Error", "Please select a customer.")
                return
            if self.con.make_reservation(reservationID=idVar.get(), guestID=customerVar.get(), roomID=roomIDVar.get(), check_in=None, check_out=None, status="Pending"):
                window.destroy()
            else:
                messagebox.showerror("Error", "Failed to create reservation. Please try again.")

        tk.Button(window, text="Submit", font=self.font, command=on_submit).grid(column=0, row=4, columnspan=2, pady=10)

    def occupancy(self):
        window = tk.Toplevel(self.Parent)
        startVar = tk.StringVar()
        endVar = tk.StringVar()

        tk.Label(window, text="Start Date:", font=self.font).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        DateEntry(window, textvariable=startVar, font=self.font).grid(row=0, column=1, padx=5, pady=5, sticky="e")
        tk.Label(window, text="End Date: ", font=self.font).grid(row=0, column=2, padx=5 ,pady=5, sticky="e")
        DateEntry(window, font=self.font, textvariable=endVar).grid(row=0, column=3, padx=5 ,pady=5, sticky="e")

        def generate_report():
            startDate = parse_date(startVar.get())
            endDate = parse_date(endVar.get())
            df = self.con.get_occupancy_data(start=startDate, end=endDate)
            tree_frame = tk.Frame(window)
            tree_frame.grid(row=1, column=0, columnspan=5, sticky="nsew", padx=5, pady=5)

            # Expand the frame with the window
            window.grid_rowconfigure(1, weight=1)
            window.grid_columnconfigure(0, weight=1)

            tree = Tree(tree_frame, df)

        tk.Button(window, text="Generate report", font=self.font, command=generate_report).grid(row=0, column=4, columnspan=2, padx=5, pady=5, sticky="we")

    def revenue(self):
        window = tk.Toplevel(self.Parent)
        startVar = tk.StringVar()
        endVar = tk.StringVar()

        tk.Label(window, text="Start Date:", font=self.font).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        DateEntry(window, textvariable=startVar, font=self.font).grid(row=0, column=1, padx=5, pady=5, sticky="e")
        tk.Label(window, text="End Date: ", font=self.font).grid(row=0, column=2, padx=5 ,pady=5, sticky="e")
        DateEntry(window, font=self.font, textvariable=endVar).grid(row=0, column=3, padx=5 ,pady=5, sticky="e")

        def generate_report():
            startDate = parse_date(startVar.get())
            endDate = parse_date(endVar.get())
            df = self.con.get_revenue_data(start=startDate, end=endDate)
            tree_frame = tk.Frame(window)
            tree_frame.grid(row=1, column=0, columnspan=5, sticky="nsew", padx=5, pady=5)

            # Expand the frame with the window
            window.grid_rowconfigure(1, weight=1)
            window.grid_columnconfigure(0, weight=1)

            tree = Tree(tree_frame, df)

        tk.Button(window, text="Generate report", font=self.font, command=generate_report).grid(row=0, column=4, columnspan=2, padx=5, pady=5, sticky="we")

    def guest_report(self):
        window = tk.Toplevel(self.Parent)
        df = self.con.generate_guest_report()
        tree = Tree(window, df)

class Tree:
    def __init__(self, parent, dataframe):
        self.Parent = parent
        self.df = dataframe
        self.tree = ttk.Treeview(self.Parent)
        self.scrollbar = ttk.Scrollbar(self.Parent, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Use the same row, adjacent columns
        self.tree.grid(row=1, column=0, sticky="nsew")
        self.scrollbar.grid(row=1, column=1, sticky="ns")

        # Set weight so the Treeview expands properly
        self.Parent.grid_rowconfigure(0, weight=0)
        self.Parent.grid_columnconfigure(0, weight=0)
        self.Parent.grid_columnconfigure(1, weight=0)  # scrollbar should not expand


        self.define_columns()

        for row in self.df.itertuples(index=False):
            self.tree.insert("", "end", values=row)

    def define_columns(self):
        self.tree["columns"] = list(self.df.columns)
        self.tree["show"] = "headings"
        for heading in self.df.columns:
            self.tree.heading(heading, text=heading)
             # Estimate width: max of header and column content lengths
            max_len = max(
                [len(str(val)) for val in self.df[heading].values] + [len(heading)]
            )
            pixel_width = max(80, min(max_len * 8, 300))  # clamp width between 80 and 300
            self.tree.column(heading, anchor="center", width=pixel_width)

        
