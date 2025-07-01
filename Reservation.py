from sql import SQL
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
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
        self.searchBtn = tk.Button(self.guest_frame, text="Search", font=("Arial", 10), bg="#ffffff", fg="#000000", height=1, command=self.search_guest)
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
        self.Treeview = ResList(self.bottom_Pane, self.con, self.on_select)

        self.Add_NewBtn = tk.Button(self.bottom_Pane, text="Add New", font=("Arial", 8), bg="#03A503", fg="#000000", height=1, command=self.add_new)
        self.Add_NewBtn.pack(padx=5, pady=2, side="right")
        
        self.cancelBtn = tk.Button(self.bottom_Pane, text="Cancel", font=("Arial", 8), bg="#ffffff", fg="#000000", height=1, state="disabled", command=self.cancel_select)
        self.cancelBtn.pack(padx=5, pady=2, side="right")

        self.editBtn = tk.Button(self.bottom_Pane, text="Edit", font=("Arial", 8), bg="#ffffff", fg="#000000", height=1, state="disabled", command=self.edit_row)
        self.editBtn.pack(padx=5, pady=2, side="right")

        self.deleteBtn = tk.Button(self.bottom_Pane, text="Delete", font=("Arial", 8), bg="#ffffff", fg="#000000", height=1, state="disabled", command=self.delete_row)
        self.deleteBtn.pack(padx=5, pady=2, side="right")

    def search_guest(self):
        guestID = self.guest_bar.get()
        self.Treeview.fillTree(guestID=guestID)
        
    def on_select(self, selected_row = None):
        if selected_row:
            self.editBtn.config(state="active")
            self.cancelBtn.config(state="active")
            self.deleteBtn.config(state="active")
            self.selected_row = selected_row
        else:
            self.editBtn.config(state="disabled")
            self.cancelBtn.config(state="disabled")
            self.deleteBtn.config(state="disabled")
            self.selected_row = None

    def edit_row(self):
        new_window = tk.Toplevel(self.parent)
        new_window.title("Edit Reservation")

        guest_var = tk.StringVar(value=self.selected_row[1])
        room_var = tk.StringVar(value=self.selected_row[2])
        date_var = tk.StringVar(value=self.selected_row[4])
        status_var = tk.StringVar(value=self.selected_row[5])

        def on_submit():
            guest = guest_var.get()
            room = room_var.get()
            date = date_var.get()
            status = status_var.get()
            if self.con.change_reservation(
                reservationID=self.selected_row[0],
                guestID=guest,
                roomID=room,
                check_out=date,
                status=status,
            ):
                self.Treeview.fillTree()
                new_window.destroy()
            else:
                messagebox.showerror("Error", "Operation failed. Please enter correct details")

        font_style = ("Arial", 10, "bold")

        # Reservation ID (readonly label)
        tk.Label(new_window, text="Reservation ID:", font=font_style).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        tk.Label(new_window, text=self.selected_row[0], font=font_style).grid(row=0, column=1, sticky="w", padx=5, pady=5)

        # Guest ID
        tk.Label(new_window, text="Guest ID:", font=font_style).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(new_window, textvariable=guest_var, font=font_style).grid(row=1, column=1, sticky="w", padx=5, pady=5)

        # Room No
        tk.Label(new_window, text="Room No:", font=font_style).grid(row=2, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(new_window, textvariable=room_var, font=font_style).grid(row=2, column=1, sticky="w", padx=5, pady=5)

        # Check-In (readonly label)
        tk.Label(new_window, text="Check-In:", font=font_style).grid(row=3, column=0, sticky="e", padx=5, pady=5)
        tk.Label(new_window, text=self.selected_row[3], font=font_style).grid(row=3, column=1, sticky="w", padx=5, pady=5)

        # Check-Out (DateEntry)
        tk.Label(new_window, text="Check-Out:", font=font_style).grid(row=4, column=0, sticky="e", padx=5, pady=5)
        tkcal.DateEntry(new_window, textvariable=date_var, font=font_style).grid(row=4, column=1, sticky="w", padx=5, pady=5)

        # Status (Combobox)
        tk.Label(new_window, text="Status (Pending/Booked):", font=font_style).grid(row=5, column=0, sticky="e", padx=5, pady=5)
        dropdown = ttk.Combobox(new_window, textvariable=status_var, values=["Pending", "Booked"], state="readonly", font=font_style)
        dropdown.grid(row=5, column=1, sticky="w", padx=5, pady=5)
        dropdown.set(status_var.get())  # set current value properly

        # Submit button spanning both columns, centered
        tk.Button(new_window, text="Submit", font=font_style, command=on_submit).grid(row=6, column=0, columnspan=2, pady=10)


    def cancel_select(self):
        self.selected_row = None
        self.Treeview._unselect()

    def add_new(self):
        new_window = tk.Toplevel(self.parent)

        reserve_var = tk.StringVar()
        guest_var = tk.StringVar()
        room_var = tk.StringVar()
        check_in_var = tk.StringVar()
        check_out_var = tk.StringVar()
        status_var = tk.StringVar()

        def on_submit():
            reserve = reserve_var.get()
            guest = guest_var.get()
            room = room_var.get()
            check_in = check_in_var.get()
            check_out = check_out_var.get()
            status = status_var.get()
            if check_in == "":
                check_in = None
            if check_out == "":
                check_out = None
            if self.con.make_reservation(
                reservationID=reserve,
                guestID=guest,
                roomID=room,
                check_in=check_in,
                check_out=check_out,
                status=status,
            ):
                self.Treeview.fillTree()
                new_window.destroy()
            else:
                messagebox.showerror("Error", "Operation failed. Please enter correct details")

        # Use a consistent font for all widgets
        font_style = ("Arial", 10, "bold")

        # Labels and their corresponding widgets
        labels = [
            "Reservation ID:",
            "Guest ID:",
            "Room No.:",
            "Check-in date:",
            "Check-out date:",
            "Status (Pending/Booked):",
        ]
        widgets = [
            tk.Entry(new_window, textvariable=reserve_var, font=font_style),
            tk.Entry(new_window, textvariable=guest_var, font=font_style),
            tk.Entry(new_window, textvariable=room_var, font=font_style),
            tkcal.DateEntry(new_window, textvariable=check_in_var, font=font_style),
            tkcal.DateEntry(new_window, textvariable=check_out_var, font=font_style),
            ttk.Combobox(new_window, textvariable=status_var, values=["Pending", "Booked"], state="readonly", font=font_style),
        ]
        
        widgets[4].delete(0, 'end')
        
        status_var.set("Pending")  # Set default for dropdown

        for i, (text, widget) in enumerate(zip(labels, widgets)):
            tk.Label(new_window, text=text, font=font_style).grid(row=i, column=0, sticky="e", padx=5, pady=5)
            widget.grid(row=i, column=1, sticky="w", padx=5, pady=5)

        # Submit button spans two columns and centered
        submit_btn = tk.Button(new_window, text="Submit", font=font_style, command=on_submit)
        submit_btn.grid(row=len(labels), column=0, columnspan=2, pady=10)


    def delete_row(self):
        reservationID = self.selected_row[0]
        self.con.delete_reservation(reservationID)
        self.Treeview.fillTree()


class ResList:
    def __init__(self, parent, con, callback):
        self.parent = parent
        self.callback = callback
        self.tree = ttk.Treeview(self.parent)
        self.scrollbar = ttk.Scrollbar(self.parent, orient="vertical", command=self.tree.yview)
        self.define_columns()
        self.con = con
        self.scrollbar.pack(side="right",fill="y")
        self.tree.pack(fill="both", expand=True)
        self.tree.config(yscrollcommand=self.scrollbar.set)
        self.fillTree()
        self.tree.bind("<<TreeviewSelect>>", self._handle_selection)

    def define_columns(self):
        self.tree["columns"]= ("ID", "Guest ID", "Room No.", "Check-in", "Check-Out", "Status")
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("ID", anchor=tk.CENTER, width=80)
        self.tree.column("Guest ID", anchor=tk.CENTER, width=100)
        self.tree.column("Room No.", anchor=tk.CENTER, width=100)
        self.tree.column("Check-in", anchor=tk.CENTER, width=120)
        self.tree.column("Check-Out", anchor=tk.CENTER, width=120)
        self.tree.column("Status", anchor=tk.CENTER, width=100)

        self.tree.heading("#0", text="", anchor=tk.CENTER)
        self.tree.heading("ID", text="ID", anchor=tk.CENTER)
        self.tree.heading("Guest ID", text="Guest ID", anchor=tk.CENTER)
        self.tree.heading("Room No.", text="Room No.", anchor=tk.CENTER)
        self.tree.heading("Check-in", text="Check-in", anchor=tk.CENTER)
        self.tree.heading("Check-Out", text="Check-Out", anchor=tk.CENTER)
        self.tree.heading("Status", text="Status", anchor=tk.CENTER)

    def fillTree(self, guestID = None, date = None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        results = self.con.get_reservations(guestID, date)
        for row in results:
            reservID, guestID, roomNo, check_in, check_out, status = row
            self.tree.insert("", "end", values=(reservID, guestID, roomNo, check_in, check_out, status))

    def _handle_selection(self, event):
        selected_rows = self.tree.selection()
        if selected_rows:
            values = self.tree.item(selected_rows[0], "values")
            self.callback(values)
        else:
            self.callback(None)
    
    def _unselect(self):
        self.tree.selection_set()