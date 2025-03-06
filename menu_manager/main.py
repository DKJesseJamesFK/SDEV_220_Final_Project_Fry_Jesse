import tkinter as tk
import tkinter.ttk as ttk
from models import *

class MenuManagerApp:
    """The main application class. It is a Tkinter window with tabs for menu, menu items, orders, and inventory."""
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
        self.menu_text.config(state="disabled")
        self.update_menu_text()

        # Create menu items tab
        self.menu_items_tab = tk.Frame(self.notebook)
        self.notebook.add(self.menu_items_tab, text="Menu Items")

        # Create orders tab
        self.orders_tab = tk.Frame(self.notebook)
        self.notebook.add(self.orders_tab, text="Orders")

        # Create inventory tab
        self.inventory_tab = tk.Frame(self.notebook)
        self.notebook.add(self.inventory_tab, text="Inventory")

    """DELETE THIS LATER"""
    # def generate_menu_text(self):
    #     """Generates the menu text and returns it as a string."""
    #     menu = Menu()
    #     return str(menu)
    
    def update_menu_text(self):
        """Updates the menu text in the text widget."""
        self.menu_text.config(state="normal")
        self.menu_text.delete(1.0, tk.END)
        menu_repo = MenuRepository("menu.db")
        menu_items = menu_repo.get_all_menu_items()
        for category, items in menu_items.items():
            self.menu_text.insert(tk.END, f"{category}:\n")
            for item in items:
                self.menu_text.insert(tk.END, f"  {item}\n")
            self.menu_text.insert(tk.END, "\n")
        self.menu_text.config(state="disabled")

    """DELETE THIS LATER"""
    # def on_tab_change(self, event):
    #     current_tab = self.notebook.index(self.notebook.select())
    #     if current_tab == 0: # Menu tab
    #         self.update_menu_text()

if __name__ == "__main__":
    root = tk.Tk()
    app = MenuManagerApp(root)
    root.mainloop()