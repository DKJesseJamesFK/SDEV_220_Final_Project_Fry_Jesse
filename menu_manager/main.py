import tkinter as tk
import tkinter.ttk as ttk
from models import *

class MenuManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Menu Manager")
        self.root.geometry("800x600")

        # Create a notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)

        # Create menu tab
        self.menu_tab = tk.Frame(self.notebook)
        self.notebook.add(self.menu_tab, text="Menu")

        # Create text widget to display menu
        self.menu_text = tk.Text(self.menu_tab, width=80, height=20)
        self.menu_text.pack(pady=10)

        # Create menu items tab
        self.menu_items_tab = tk.Frame(self.notebook)
        self.notebook.add(self.menu_items_tab, text="Menu Items")

        # Create orders tab
        self.orders_tab = tk.Frame(self.notebook)
        self.notebook.add(self.orders_tab, text="Orders")

        # Create inventory tab
        self.inventory_tab = tk.Frame(self.notebook)
        self.notebook.add(self.inventory_tab, text="Inventory")

if __name__ == "__main__":
    root = tk.Tk()
    app = MenuManagerApp(root)
    root.mainloop()