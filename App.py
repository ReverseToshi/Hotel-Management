from tkinter import messagebox
from sql import SQL
import tkinter as tk
from tkinter import ttk
import time
from Tab_pane import Tab_pane
from datetime import datetime
from tkcalendar import DateEntry
from Tasks import parse_date

# MAIN APPLICATION
class Application:
    """Main application class for the hotel management system."""
    def __init__(self):
        # Create the main application window
        self.Parent = tk.Tk()
        self.Parent.title("Management")
        self.Parent.geometry("1100x650")
        self.Parent.resizable(0, 0)  # Disable window resizing

        # Initialize database connection and font settings
        self.con = SQL()
        self.font = ("Arial", 12)
        
        # Create main wrapper frame to hold all content
        self.wrapper = tk.Frame(self.Parent)
        self.wrapper.pack(fill="both", expand=True)

        # Header section with application title
        self.Header = tk.Label(
            self.wrapper, 
            bg="#2c3e50",
            fg="#ffffff",
            text="Hotel Management System",
            font=("Arial", 20, "bold")
        )
        self.Header.pack(fill="x")  # Stretch header across width

        # Horizontal pane to separate left and right sections
        self.Pane = tk.PanedWindow(self.wrapper, orient="horizontal", sashwidth=2)

        # Load left and right panes (defined elsewhere)
        self.left_pane()
        self.right_pane()

        # Footer frame at the bottom for status/info
        self.Footer = tk.LabelFrame(
            self.wrapper,
            bg="#2c3e50",
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.Footer.pack(fill="x", side="bottom")  # Align footer to bottom

        # Clock label inside footer (can be updated live)
        self.clock = tk.Label(self.Footer, text="HELLO", font=("Arial", 12), fg="white", bg="#2c3e50")
        self.clock.pack(side="right")

        # Start the clock update loop
        self.update_clock()

        # Pack the horizontal pane containing the main UI
        self.Pane.pack(fill="both", expand=True)
        
        # Start the Tkinter event loop
        self.Parent.mainloop()

    def left_pane(self):
        # Create left panel inside the PanedWindow
        left = tk.Frame(self.Pane, bg="#9fa1a1", width=200)
        left.pack_propagate(False)  # Prevent auto-resizing based on content

        # ----- Top Section: Quick Actions -----
        top = tk.Frame(left, bg="#9fa1a1")

        # Section title
        tk.Label(master=top, text="Quick Actions", font=("Arial", 14, "bold", "underline"), bg="#9fa1a1").pack(padx=10, pady=5)

        # Button to check in a guest
        tk.Button(top, text="Check-in Guest", bg="#548A75", activebackground="#69b595",
                borderwidth=0, font=("Arial", 12), width=100, command=self.check_in).pack(padx=10, pady=5)

        # Button to check out a guest
        tk.Button(top, text="Check-out Guest", bg="#548A75", activebackground="#69b595",
                borderwidth=0, font=("Arial", 12), width=100, command=self.check_out).pack(padx=10, pady=5)

        # Button to make a new reservation
        tk.Button(top, text="New Reservation", bg="#548A75", activebackground="#69b595",
                borderwidth=0, font=("Arial", 12), width=100, command=self.make_reservation).pack(padx=10, pady=5)

        # ----- Bottom Section: Reports -----
        bottom = tk.Frame(left, bg="#9fa1a1")

        # Section title
        tk.Label(bottom, text="Reports", font=("Arial", 14, "bold", "underline"), bg="#9fa1a1").pack(padx=10, pady=5)

        # Button to view occupancy report
        tk.Button(bottom, text="Occupancy Report", bg="#548A75", activebackground="#69b595",
                borderwidth=0, font=("Arial", 12), width=100, command=self.occupancy).pack(padx=10, pady=5)

        # Button to view revenue report
        tk.Button(bottom, text="Revenue Report", bg="#548A75", activebackground="#69b595",
                borderwidth=0, font=("Arial", 12), width=100, command=self.revenue).pack(padx=10, pady=5)

        # Button to view guest report
        tk.Button(bottom, text="Guest Report", bg="#548A75", activebackground="#69b595",
                borderwidth=0, font=("Arial", 12), width=100, command=self.guest_report).pack(padx=10, pady=5)

        # Button to change password
        tk.Button(bottom, text="Change Password", bg="#548A75", activebackground="#69b595",
                borderwidth=0, font=("Arial", 12), width=100, command=self.change_password).pack(padx=10, pady=25)

        # Pack sections and add a separator between them
        top.pack()
        ttk.Separator(left, orient="horizontal").pack(fill="x", pady=5)
        bottom.pack()

        # Add the fully built left pane to the PanedWindow
        self.Pane.add(left)
    
    def change_password(self):
        """
        Set a new password using the old password
        """
        # Create a new popup window for password change
        window = tk.Toplevel(self.Parent)

        # Tkinter string variables to store password input
        oldVar = tk.StringVar()
        newVar = tk.StringVar()
        confirmVar = tk.StringVar()

        # Old password input
        tk.Label(window, text="Old Password: ", font=self.font).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(window, textvariable=oldVar, show="*", font=self.font).grid(row=0, column=1, padx=5, pady=5, sticky="we", columnspan=2)

        # New password input
        tk.Label(window, text="New Password: ", font=self.font).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(window, show="*", textvariable=newVar, font=self.font).grid(row=1, column=1, padx=5, pady=5, sticky="we", columnspan=2)

        # Confirm new password input
        tk.Label(window, text="Confirm New Password:", font=self.font).grid(row=2, column=0, padx=5, pady=5, sticky="e") 
        tk.Entry(window, show="*", textvariable=confirmVar, font=self.font).grid(row=2, column=1, padx=5, pady=5, sticky="we", columnspan=2)

        # Submit button handler
        def submit():
            # Validate that new and confirm passwords match
            if newVar.get() != confirmVar.get():
                messagebox.showerror("Error", "Passwords do not match")
                return

            # Check that new password is not the same as the old one
            if newVar.get() == oldVar.get():
                messagebox.showerror("Same Passwords", "Old and New Passwords cannot be the same")
                return

            old = oldVar.get()
            new = newVar.get()

            # Attempt to change the password in the database
            if not self.con.create_new_password(old, new):
                messagebox.showerror("Error", "Old Password is incorrect!")
                return

            # Close window and show success message
            window.destroy()
            messagebox.showinfo("Success", "Password changed successfully")

        # Submit button
        tk.Button(window, text="Submit", font=self.font, command=submit).grid(row=3, column=1, padx=5, pady=5, columnspan=2)
           
    def right_pane(self):
        right = tk.Frame(self.Pane, bg="#000000", width=900)
        tabs = Tab_pane(right)

        self.Pane.add(right)

    def update_clock(self):
        # Get current date and time formatted as 'dd-mm-yyyy    HH:MM:SS'
        current_time = time.strftime("%d-%m-%Y\t%H:%M:%S")
        
        # Update the clock label with the current time
        self.clock.config(text=current_time)
        
        # Schedule this method to run again after 1000 milliseconds (1 second)
        self.Parent.after(1000, self.update_clock)
   
    def check_out(self):
        """
        Checks out a user who has checked-in but hasn't checked-out yet
        """
        # Create a new pop-up window for check-out
        window = tk.Toplevel(self.Parent)

        # Label for reservation ID
        tk.Label(window, text="Reservation ID:", font=self.font).grid(column=0, row=0, padx=5, pady=5, sticky="e")

        # Variables to hold form data
        idVar = tk.StringVar()
        customerVar = tk.StringVar()
        roomVar = tk.StringVar()
        checkinVar = tk.StringVar()
        checkOutVar = tk.StringVar()
        priceVar = tk.DoubleVar()

        # Called when a reservation ID is selected
        def on_select(event):
            row = self.con.get_reservations(reservationID=idVar.get())[0]
            customerVar.set(row[1])
            roomVar.set(row[2])
            checkinVar.set(row[3])

        # Dropdown to choose from active reservation IDs eligible for check-out
        reservationIDs = ttk.Combobox(window, textvariable=idVar, values=self.con.get_reservation_id_for_checkout())
        reservationIDs.grid(row=0, column=1, pady=5, sticky="we")
        reservationIDs.bind("<<ComboboxSelected>>", on_select)

        # Display customer ID (readonly)
        tk.Label(window, text="Customer ID: ", font=self.font).grid(column=0, row=1, padx=5, pady=5, sticky="e")
        tk.Entry(window, textvariable=customerVar, state="readonly", font=self.font).grid(column=1, row=1, sticky="we")

        # Display room ID (readonly)
        tk.Label(window, font=self.font, text="Room ID: ").grid(column=0, row=2, padx=5, pady=5, sticky="e")
        tk.Entry(window, textvariable=roomVar, state="readonly", font=self.font).grid(row=2, column=1, pady=5, sticky="we")

        # Display check-in date (readonly)
        tk.Label(window, text="Check-In:", font=self.font).grid(column=0, row=3, padx=5, pady=5, sticky="e")
        tk.Entry(window, textvariable=checkinVar, font=self.font, state="readonly").grid(column=1, row=3, pady=5, sticky="we")

        # Input check-out date
        tk.Label(window, text="Check-Out: ", font=self.font).grid(column=0, row=4, padx=5, pady=5, sticky="e")
        DateEntry(window, textvariable=checkOutVar, font=self.font).grid(column=1, row=4, pady=5, sticky="we")

        # Calculate cost of stay
        def calculate_cost():
            # Parse dates from strings to datetime objects
            check_in_time = datetime.strptime(checkinVar.get(), "%d-%m-%Y")
            check_out_time = datetime.strptime(checkOutVar.get(), "%d/%m/%y")
            total_time = check_out_time - check_in_time
            days = total_time.days + 1  # Assume minimum 1 day stay
            price = self.con.get_price(roomVar.get())[0]  # Get room's price per day
            cost = price * days
            priceVar.set(cost)  # Set calculated cost in the field

        # Display total cost (readonly)
        tk.Label(window, text="Total Cost: ", font=self.font).grid(column=0, row=5, padx=5, pady=5, sticky="e")
        tk.Entry(window, textvariable=priceVar, font=self.font, state="readonly").grid(column=1, row=5, pady=5)

        # Button to calculate cost
        tk.Button(window, text="Calculate Total", font=self.font, command=calculate_cost).grid(column=2, row=5, padx=5, pady=5, sticky="we")

        # Finalize check-out
        def finish_checkout():
            self.con.check_out(reservationID=idVar.get(), check_out=checkOutVar.get())
            window.destroy()

        # Button to submit check-out
        tk.Button(window, text="Check-Out", font=self.font, command=finish_checkout).grid(column=0, row=6, sticky="e", padx=5, pady=5)
    
    def check_in(self):
        """
        Opens a check-in window for selecting a reservation and marking a guest as checked in.
        Automatically fills in reservation details when a reservation is selected.
        """
        window = tk.Toplevel(self.Parent)

        # Tkinter variables for form fields
        idVar = tk.StringVar()          # Reservation ID (from dropdown)
        customerVar = tk.StringVar()    # Guest ID (read-only)
        roomVar = tk.StringVar()        # Room ID (read-only)
        checkinVar = tk.StringVar()     # Check-in date

        def on_select(event):
            """Handles selection from reservation dropdown and fills out related fields."""
            reservation_id = idVar.get()
            row = self.con.get_reservations(reservationID=reservation_id)[0]
            idVar.set(row[0])       # Set Reservation ID
            customerVar.set(row[1]) # Set Guest ID
            roomVar.set(row[2])     # Set Room ID

        # Reservation dropdown selector
        tk.Label(window, text="Select Reservation:", font=self.font).grid(column=0, row=0, padx=5, pady=5, sticky="e")
        reservation_selector = ttk.Combobox(
            window,
            textvariable=idVar,
            values=self.con.get_reservation_id_for_checkin(),  # Get only upcoming/unchecked-in reservations
            font=self.font
        )
        reservation_selector.grid(row=0, column=1, sticky="we", pady=5)
        reservation_selector.bind("<<ComboboxSelected>>", on_select)

        # Read-only Customer ID display
        tk.Label(window, text="Customer ID:", font=self.font).grid(column=0, row=2, padx=5, pady=5, sticky="e")
        tk.Entry(window, textvariable=customerVar, state="readonly", font=self.font).grid(column=1, row=2, sticky="we")

        # Read-only Room ID display
        tk.Label(window, text="Room ID:", font=self.font).grid(column=0, row=3, padx=5, pady=5, sticky="e")
        tk.Entry(window, textvariable=roomVar, state="readonly", font=self.font).grid(column=1, row=3, pady=5, sticky="we")

        # Check-in date (defaults to today)
        tk.Label(window, text="Check-In:", font=self.font).grid(column=0, row=4, padx=5, pady=5, sticky="e")
        DateEntry(window, textvariable=checkinVar, font=self.font, state="readonly").grid(column=1, row=4, pady=5, sticky="we")
        checkinVar.set(datetime.now().strftime("%d/%m/%y"))

        def submit_checkin():
            """Submit the check-in details to the database."""
            self.con.check_in(reservationID=idVar.get(), check_in=parse_date(checkinVar.get()))
            window.destroy()

        # Submit button
        tk.Button(window, text="Check-In", font=self.font, command=submit_checkin).grid(column=0, row=5, columnspan=2, pady=10)

    def make_reservation(self):
        """
        Opens a window to create a new reservation.
        The user selects a customer, room type, and room ID.
        Reservation is submitted with status 'Pending'.
        """
        window = tk.Toplevel(self.Parent)

        # Tkinter variables for form fields
        idVar = tk.StringVar(value=self.con.get_next_reservation_id())  # Auto-filled Reservation ID
        customerVar = tk.StringVar()     # Selected customer ID
        roomIDVar = tk.StringVar()       # Selected room ID
        roomTypeVar = tk.StringVar()     # Selected room type

        # Get a list of all guest IDs to populate the customer dropdown
        customers = self.con.get_guests()
        customers = [customer[0] for customer in customers]  # Only keep the ID (assumed to be in index 0)

        # Reservation ID (readonly)
        tk.Label(window, text="Reservation ID:", font=self.font).grid(column=0, row=0, padx=5, pady=5, sticky="e")
        tk.Entry(window, textvariable=idVar, state="readonly", font=self.font).grid(column=1, row=0, sticky="we")

        # Customer selection (dropdown)
        tk.Label(window, text="Customer ID:", font=self.font).grid(column=0, row=1, padx=5, pady=5, sticky="e")
        customerBox = ttk.Combobox(window, textvariable=customerVar, font=self.font, values=customers)
        customerBox.grid(column=1, row=1, sticky="we")

        # Called when a room type is selected – updates available room IDs
        def on_type(event):
            rooms = self.con.get_rooms(status="Available", roomType=roomTypeVar.get())  # Filter by type and availability
            roomIDs = [room[0] for room in rooms]  # Extract room IDs
            roomID["values"] = roomIDs
            if roomIDs:
                roomID.set(roomIDs[0])  # Auto-select first available room

        # Room type selection
        tk.Label(window, text="Room Type:", font=self.font).grid(column=0, row=2, padx=5, pady=5, sticky="e")
        roomType = ttk.Combobox(
            window,
            textvariable=roomTypeVar,
            font=self.font,
            values=("Standard", "Deluxe", "Executive", "Suite", "Presidential Suite")
        )
        roomType.grid(column=1, row=2, sticky="we")
        roomType.bind("<<ComboboxSelected>>", on_type)

        # Room ID dropdown – populated dynamically
        tk.Label(window, text="Room ID:", font=self.font).grid(column=0, row=3, padx=5, pady=5, sticky="e")
        roomID = ttk.Combobox(window, textvariable=roomIDVar, font=self.font)
        roomID.grid(column=1, row=3, sticky="we")

        # Handles reservation submission
        def on_submit():
            if customerVar.get() == "":
                messagebox.showerror("Error", "Please select a customer.")
                return
            success = self.con.make_reservation(
                reservationID=idVar.get(),
                guestID=customerVar.get(),
                roomID=roomIDVar.get(),
                check_in=None,
                check_out=None,
                status="Pending"
            )
            if success:
                window.destroy()
            else:
                messagebox.showerror("Error", "Failed to create reservation. Please try again.")

        # Submit button
        tk.Button(window, text="Submit", font=self.font, command=on_submit).grid(column=0, row=4, columnspan=2, pady=10)

    def occupancy(self):
        """
        Opens a new window where the user can select a date range
        and generate an occupancy report for that period.
        """
        window = tk.Toplevel(self.Parent)

        # Date selection variables
        startVar = tk.StringVar()
        endVar = tk.StringVar()

        # Start date label and date picker
        tk.Label(window, text="Start Date:", font=self.font).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        DateEntry(window, textvariable=startVar, font=self.font).grid(row=0, column=1, padx=5, pady=5, sticky="e")

        # End date label and date picker
        tk.Label(window, text="End Date: ", font=self.font).grid(row=0, column=2, padx=5, pady=5, sticky="e")
        DateEntry(window, textvariable=endVar, font=self.font).grid(row=0, column=3, padx=5, pady=5, sticky="e")

        def generate_report():
            """
            Generates the occupancy report for the selected date range.
            Displays the data in a Tree widget.
            """
            # Parse selected dates
            startDate = parse_date(startVar.get())
            endDate = parse_date(endVar.get())

            # Retrieve occupancy data from the database
            df = self.con.get_occupancy_data(start=startDate, end=endDate)

            # Create a frame to contain the report tree
            tree_frame = tk.Frame(window)
            tree_frame.grid(row=1, column=0, columnspan=5, sticky="nsew", padx=5, pady=5)

            # Allow the frame to expand with the window
            window.grid_rowconfigure(1, weight=1)
            window.grid_columnconfigure(0, weight=1)

            # Display the data using the Tree widget
            tree = Tree(tree_frame, df)

        # Button to trigger the report generation
        tk.Button(window, text="Generate report", font=self.font, command=generate_report).grid(
            row=0, column=4, columnspan=2, padx=5, pady=5, sticky="we"
        )

    def revenue(self):
        """
        Open a window to select start and end dates, then generate and display a revenue report.
        """
        window = tk.Toplevel(self.Parent)
        startVar = tk.StringVar()
        endVar = tk.StringVar()

        # Date selection inputs
        tk.Label(window, text="Start Date:", font=self.font).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        DateEntry(window, textvariable=startVar, font=self.font).grid(row=0, column=1, padx=5, pady=5, sticky="e")
        tk.Label(window, text="End Date: ", font=self.font).grid(row=0, column=2, padx=5, pady=5, sticky="e")
        DateEntry(window, font=self.font, textvariable=endVar).grid(row=0, column=3, padx=5, pady=5, sticky="e")

        def generate_report():
            # Get dates from inputs
            startDate = parse_date(startVar.get())
            endDate = parse_date(endVar.get())

            # Fetch revenue data for date range
            df = self.con.get_revenue_data(start=startDate, end=endDate)

            # Frame to hold the report table
            tree_frame = tk.Frame(window)
            tree_frame.grid(row=1, column=0, columnspan=5, sticky="nsew", padx=5, pady=5)

            # Make frame expandable
            window.grid_rowconfigure(1, weight=1)
            window.grid_columnconfigure(0, weight=1)

            # Display data in a Tree widget
            tree = Tree(tree_frame, df)

        # Button to trigger report generation
        tk.Button(window, text="Generate report", font=self.font, command=generate_report)\
            .grid(row=0, column=4, columnspan=2, padx=5, pady=5, sticky="we")

    def guest_report(self):
        """
            Generates a guest report
        """
        window = tk.Toplevel(self.Parent)
        df = self.con.generate_guest_report()
        tree = Tree(window, df)

class Tree:
    """
    Display a pandas DataFrame in a ttk.Treeview widget with a vertical scrollbar.
    """

    def __init__(self, parent, dataframe):
        self.Parent = parent
        self.df = dataframe
        self.tree = ttk.Treeview(self.Parent)
        self.scrollbar = ttk.Scrollbar(self.Parent, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Place tree and scrollbar side by side
        self.tree.grid(row=1, column=0, sticky="nsew")
        self.scrollbar.grid(row=1, column=1, sticky="ns")

        # Prevent scrollbar from expanding
        self.Parent.grid_rowconfigure(0, weight=0)
        self.Parent.grid_columnconfigure(0, weight=0)
        self.Parent.grid_columnconfigure(1, weight=0)

        self.define_columns()

        # Insert DataFrame rows into the Treeview
        for row in self.df.itertuples(index=False):
            self.tree.insert("", "end", values=row)

    def define_columns(self):
        # Setup columns and headings based on DataFrame
        self.tree["columns"] = list(self.df.columns)
        self.tree["show"] = "headings"

        for heading in self.df.columns:
            self.tree.heading(heading, text=heading)

            # Set column width based on max length of content and header (clamped)
            max_len = max([len(str(val)) for val in self.df[heading].values] + [len(heading)])
            pixel_width = max(80, min(max_len * 8, 300))
            self.tree.column(heading, anchor="center", width=pixel_width)
