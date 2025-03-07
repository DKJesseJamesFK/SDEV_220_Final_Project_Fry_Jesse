import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as msgbox
from models import *

class MenuManagerApp:
    """The main application class. It is a Tkinter window with tabs for menu, menu items, orders, and inventory."""
    def __init__(self, root):
        self.root = root
        self.root.title("Menu Manager")
        self.root.geometry("800x600")
        self.menu_repo = MenuRepository("menu.db") #NEW

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
        self.create_menu_items_tab() #NEW

        # Create orders tab
        self.orders_tab = tk.Frame(self.notebook)
        self.notebook.add(self.orders_tab, text="Orders")

        # Create inventory tab
        self.inventory_tab = tk.Frame(self.notebook)
        self.notebook.add(self.inventory_tab, text="Inventory")
    
    def update_menu_text(self):
        """Updates the menu text in the text widget."""
        self.menu_text.config(state="normal")
        self.menu_text.delete(1.0, tk.END)
        menu_items = self.menu_repo.get_all_menu_items()
        for category, items in menu_items.items():
            self.menu_text.insert(tk.END, f"{category}:\n")
            for item in items:
                self.menu_text.insert(tk.END, f"  {item}\n")
            self.menu_text.insert(tk.END, "\n")
        self.menu_text.config(state="disabled")

    # NEWv
    def create_menu_items_tab(self):
        self.menu_items_listbox = tk.Listbox(self.menu_items_tab)
        self.menu_items_listbox.pack()

        self.edit_button = tk.Button(self.menu_items_tab, text="Edit", command=self.edit_menu_item)
        self.edit_button.pack()

        self.delete_button = tk.Button(self.menu_items_tab, text="Delete", command=self.delete_menu_item)
        self.delete_button.pack()

        self.name_label = tk.Label(self.menu_items_tab, text="Name:")
        self.name_label.pack()
        self.name_entry = tk.Entry(self.menu_items_tab)
        self.name_entry.pack()

        self.description_label = tk.Label(self.menu_items_tab, text="Description:")
        self.description_label.pack()
        self.description_entry = tk.Entry(self.menu_items_tab)
        self.description_entry.pack()

        self.price_label = tk.Label(self.menu_items_tab, text="Price:")
        self.price_label.pack()
        self.price_entry = tk.Entry(self.menu_items_tab)
        self.price_entry.pack()

        self.calories_label = tk.Label(self.menu_items_tab, text="Calories:")
        self.calories_label.pack()
        self.calories_entry = tk.Entry(self.menu_items_tab)
        self.calories_entry.pack()

        self.category_label = tk.Label(self.menu_items_tab, text="Category:")
        self.category_label.pack()
        self.category_entry = tk.Entry(self.menu_items_tab)
        self.category_entry.pack()

        self.save_button = tk.Button(self.menu_items_tab, text="Save", command=self.save_menu_item)
        self.save_button.pack()

        self.update_menu_items_list()

    def update_menu_items_list(self):
        self.menu_items_listbox.delete(0, tk.END)
        menu_items = self.menu_repo.get_all_menu_items()
        for category, items in menu_items.items():
            for item in items:
                self.menu_items_listbox.insert(tk.END, item.name)

    def edit_menu_item(self):
        print("Edit menu item") # TESTING PURPOSES ONLY
        index = self.menu_items_listbox.curselection()
        if index:
            menu_item_name = self.menu_items_listbox.get(index[0])
            menu_item, menu_item_id = self.menu_repo.get_menu_item_by_name(menu_item_name)
            if menu_item and menu_item_id:
                self.name_entry.delete(0, tk.END)
                self.name_entry.insert(0, menu_item.name)
                self.description_entry.delete(0, tk.END)
                self.description_entry.insert(0, menu_item.description)
                self.price_entry.delete(0, tk.END)
                self.price_entry.insert(tk.END, str(menu_item.price))
                self.calories_entry.delete(0, tk.END)
                self.calories_entry.insert(tk.END, str(menu_item.calories))
                self.category_entry.delete(0, tk.END)
                self.category_entry.insert(0, menu_item.category)

                self.current_menu_item_id = menu_item_id  # Store ID for future use.

    def delete_menu_item(self):
        print("Delete menu item") # TESTING PURPOSES ONLY
        index = self.menu_items_listbox.curselection()
        if index:
            menu_item_name = self.menu_items_listbox.get(index[0])
            menu_item, menu_item_id = self.menu_repo.get_menu_item_by_name(menu_item_name)
            if menu_item and menu_item_id:
                self.menu_repo.delete_menu_item(menu_item_id)
                self.update_menu_items_list()

    def save_menu_item(self):
        print("Save menu item") # TESTING PURPOSES ONLY
        menu_item_name = self.name_entry.get().strip()
        menu_item_description = self.description_entry.get().strip()
        menu_item_price = self.price_entry.get().strip()
        menu_item_calories = self.calories_entry.get().strip()
        menu_item_category = self.category_entry.get().strip()

        if not menu_item_name or not menu_item_category:
            msgbox.showerror("Error", "Please enter a name and category for the menu item.")
            return
        
        try:
            menu_item_price = float(menu_item_price)
            menu_item_calories = int(menu_item_calories)
        except ValueError:
            msgbox.showerror("Error", "Please enter a valid price and calories for the menu item.")
            return
        
        menu_item = MenuItem(menu_item_name, menu_item_description, menu_item_price, menu_item_calories, menu_item_category)

        if hasattr(self, "current_menu_item_id") and self.current_menu_item_id:
            # Update existing menu item
            self.menu_repo.update_menu_item(self.current_menu_item_id, menu_item)
            msgbox.showinfo("Success", "Menu item updated successfully.")
            del self.current_menu_item_id
        else:
            # Create new menu item
            self.menu_repo.create_menu_item(menu_item)
            msgbox.showinfo("Success", "Menu item created successfully.")

        self.update_menu_items_list()
        self.clear_form_fields() # Clear input fields after saving
        self.update_menu_text()

    def clear_form_fields(self):
        self.name_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.calories_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)

        # NEW^

if __name__ == "__main__":
    root = tk.Tk()
    app = MenuManagerApp(root)
    root.mainloop()