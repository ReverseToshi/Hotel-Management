import tkinter as tk
from tkinter import ttk
from sql import SQL
from tkinter import messagebox

class Guest:
    """This class is used to create the guest management frame in the main window."""
    def __init__(self, window):
        """Initialize the guest management frame."""
        self.parent = window
        self.Frame = ttk.Frame(self.parent)
        self.con = SQL()
        self.fillFrame()
        self.Frame.pack(fill="both", expand=True)

    def fillFrame(self):
        """This method creates the guest management layout with a search bar and a list of guests."""
        # Create the main frame for the guest management
        self.Pane = tk.PanedWindow(self.Frame, orient="vertical", border=3, sashwidth=2, bg="#000000")
        self.top_pane = tk.Frame(self.Pane, bg="#ffffff")
        self.bottom_pane = tk.Frame(self.Pane)

        self.create_top()
        self.create_bottom()

        self.Pane.add(self.top_pane)
        self.Pane.add(self.bottom_pane)
        self.Pane.pack(fill="both", expand=True)

    def create_top(self):
        """Create the top pane with a search bar and an 'Add New Guest' button."""
        # Label
        label = tk.Label(self.top_pane, text="Search Guest:", bg="#ffffff")
        label.pack(side="left", padx=(0, 5))

        # Entry with placeholder
        self.search_var = tk.StringVar(value="Name, email, phone...")
        entry = tk.Entry(self.top_pane, textvariable=self.search_var, width=30, bg="#ffffff", fg="#000000")
        entry.pack(side="left", padx=(0, 5))

        # Search button
        search_btn = tk.Button(self.top_pane, text="Search", command=self.search_guest)
        search_btn.pack(side="left", padx=(0, 10))

        # Add New Guest button (styled green)
        add_btn = tk.Button(self.top_pane, text="Add New Guest", bg="#28a745", fg="white", activebackground="#218838", relief="flat", padx=10, pady=2, command=self.add_new_guest)
        add_btn.pack(side="left")

    def create_bottom(self):
        self.Tree = GuestList(self.bottom_pane, self.con)

    def search_guest(self):
        self.Tree.fillTree(self.search_var.get())

    def add_new_guest(self):
        """Open a new window to add a new guest."""
        # Create a new window for the guest entry form
        new_window = tk.Toplevel()
        new_window.title("Customer Entry Form")
        new_window.geometry("400x300")

        # Variables
        id_var = tk.StringVar()
        first_var = tk.StringVar()
        last_var = tk.StringVar()
        age_var = tk.IntVar()
        email_var = tk.StringVar()
        phone_var = tk.IntVar()

        def on_submit():
            """Handle the submission of the new guest form."""
            if self.con.add_guest(id_var.get(), first_var.get(), last_var.get(), age_var.get(), email_var.get(), phone_var.get()):
                new_window.destroy()
                self.Tree.fillTree()
            else:
                messagebox.showerror("Error", "Input valid details")
            
        # Labels and Entries
        labels = ["Customer ID", "First Name", "Last Name", "Age", "Email", "Phone"]
        vars = [id_var, first_var, last_var, age_var, email_var, phone_var]

        # Create and place labels and entry fields in the new window
        for i, (label_text, var) in enumerate(zip(labels, vars)):
            ttk.Label(new_window, text=label_text + ":").grid(row=i, column=0, padx=10, pady=5, sticky="e")
            ttk.Entry(new_window, textvariable=var, width=30).grid(row=i, column=1, padx=10, pady=5)

        # Submit button
        ttk.Button(new_window, text="Submit", command=on_submit).grid(
            row=len(labels), column=0, columnspan=2, pady=10
        )


class GuestList:
    """This class is used to create the guest list frame in the guest management window."""
    def __init__(self, parent, con):
        """Initialize the guest list frame."""
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
        """Define the columns for the guest list Treeview."""
        # Define the columns for the Treeview
        self.tree["columns"]=("ID", "First Name", "Last Name", "Age", "Email", "Phone Number")
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("ID", anchor=tk.CENTER, width=50)
        self.tree.column("First Name", anchor=tk.CENTER, width=100)
        self.tree.column("Last Name", anchor=tk.CENTER, width=100)
        self.tree.column("Age", anchor=tk.CENTER, width=50)
        self.tree.column("Email", anchor=tk.CENTER, width=150)
        self.tree.column("Phone Number", anchor=tk.CENTER, width=100)

        # Set the headings for the columns
        self.tree.heading("#0", text="", anchor=tk.CENTER)
        self.tree.heading("ID", text="ID", anchor=tk.CENTER)
        self.tree.heading("First Name", text="First Name", anchor=tk.CENTER)
        self.tree.heading("Last Name", text="Last Name", anchor=tk.CENTER)
        self.tree.heading("Age", text="Age", anchor=tk.CENTER)
        self.tree.heading("Email", text="Email", anchor=tk.CENTER)
        self.tree.heading("Phone Number", text="Phone Number", anchor=tk.CENTER)

    def fillTree(self, query="Name, email, phone..."):
        """Fill the Treeview with guest data from the database."""
        # Clear the Treeview before filling it with new data
        if query=="Name, email, phone...":
            query=None
        # Clear existing items in the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Fetch data from the database
        results = self.con.get_guests(query)
        # Check if results is None or empty
        for row in results:
            customerID, firstName, age, lastName, email, phone = row
            self.tree.insert("", "end", values=(customerID, firstName, lastName, age, email, phone))