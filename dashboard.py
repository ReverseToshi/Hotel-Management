from sql import SQL
import tkinter as tk

class Dashboard:
    def __init__(self):
        self.Parent = tk.Tk()
        # Menu ribbon
        self.menu_bar = tk.Menu(self.Parent)
        self.map_menu()
        self.Parent.config(menu=self.menu_bar)  
        self.Parent.mainloop()


    def map_menu(self):
        info_menu = tk.Menu(self.menu_bar)
        info_menu.add_command(label="Hotel info", command=self.hotel_info)

        self.menu_bar.add_cascade(label="info", menu=info_menu)

    def hotel_info(self):
        info_window = tk.Toplevel(self.Parent)
        info_window.title("Hotel Information")
