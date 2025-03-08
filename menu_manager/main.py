import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as msgbox
from models import *

# MENU

class MenuManagerApp:
    """The main application class. It is a Tkinter window with tabs for menu, menu items, orders, and inventory."""
    def __init__(self, root):
        self.root = root
        self.root.title("Menu Manager")
        self.root.geometry("800x600")
        self.menu_repo = MenuRepository("menu.db")

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
        self.create_menu_items_tab()

        # Create orders tab
        self.orders_tab = tk.Frame(self.notebook)
        self.notebook.add(self.orders_tab, text="Orders")
        self.create_orders_tab()

        # Create inventory tab
        self.inventory_tab = tk.Frame(self.notebook)
        self.notebook.add(self.inventory_tab, text="Inventory")
        self.create_inventory_tab()
    
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

        # MENU ITEMS

    
    def create_menu_items_tab(self):
        """Creates GUI elements for menu items tab."""

        # Create listbox to display menu items
        self.menu_items_listbox = tk.Listbox(self.menu_items_tab)
        self.menu_items_listbox.pack()

        # Create Edit button
        self.edit_button = tk.Button(self.menu_items_tab, text="Edit", command=self.edit_menu_item)
        self.edit_button.pack()

        # Create Delete button
        self.delete_button = tk.Button(self.menu_items_tab, text="Delete", command=self.delete_menu_item)
        self.delete_button.pack()

        # Create Name form field
        self.name_label = tk.Label(self.menu_items_tab, text="Name:")
        self.name_label.pack()
        self.name_entry = tk.Entry(self.menu_items_tab)
        self.name_entry.pack()

        # Create Description form field
        self.description_label = tk.Label(self.menu_items_tab, text="Description:")
        self.description_label.pack()
        self.description_entry = tk.Entry(self.menu_items_tab)
        self.description_entry.pack()

        # Create Price form field
        self.price_label = tk.Label(self.menu_items_tab, text="Price:")
        self.price_label.pack()
        self.price_entry = tk.Entry(self.menu_items_tab)
        self.price_entry.pack()

        # Create Calories form field
        self.calories_label = tk.Label(self.menu_items_tab, text="Calories:")
        self.calories_label.pack()
        self.calories_entry = tk.Entry(self.menu_items_tab)
        self.calories_entry.pack()

        # Create Category dropdown
        self.category_label = tk.Label(self.menu_items_tab, text="Category:")
        self.category_label.pack()
        categories = list(self.menu_repo.get_all_menu_items().keys())
        self.category_entry = ttk.Combobox(self.menu_items_tab, values=categories)
        self.category_entry.pack()

        # Create Save button
        self.save_button = tk.Button(self.menu_items_tab, text="Save", command=self.save_menu_item)
        self.save_button.pack()

        # Populate menu items list
        self.update_menu_items_list()

    def update_menu_items_list(self):
        """Updates the menu items list in the listbox."""
        self.menu_items_listbox.delete(0, tk.END)
        menu_items = self.menu_repo.get_all_menu_items()
        for category, items in menu_items.items():
            for item in items:
                self.menu_items_listbox.insert(tk.END, item.name)

    def edit_menu_item(self):
        """Populates the form fields with the selected menu item's details for editing."""
        # print("Edit menu item") # TESTING PURPOSES ONLY
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
                self.category_entry.set(menu_item.category)
                self.category_entry.update_idletasks()

                self.current_menu_item_id = menu_item_id  # Store ID for future use.

    def delete_menu_item(self):
        """Deletes the selected menu item from the database."""
        # print("Delete menu item") # TESTING PURPOSES ONLY
        index = self.menu_items_listbox.curselection()
        if index:
            menu_item_name = self.menu_items_listbox.get(index[0])
            menu_item, menu_item_id = self.menu_repo.get_menu_item_by_name(menu_item_name)
            if menu_item and menu_item_id:
                self.menu_repo.delete_menu_item(menu_item_id)
                self.update_menu_items_list()

    def save_menu_item(self):
        """Saves the updated or new menu item to the database."""
        print("Save menu item") # TESTING PURPOSES ONLY
        menu_item_name = self.name_entry.get().strip()
        menu_item_description = self.description_entry.get().strip()
        menu_item_price = self.price_entry.get().strip()
        menu_item_calories = self.calories_entry.get().strip()
        menu_item_category = self.category_entry.get().strip()

        if not menu_item_name or not menu_item_category:
            msgbox.showerror("Error", "Please enter a name and category for the menu item.")
            return
        
        try: # Input validation
            menu_item_price = float(menu_item_price)
            menu_item_calories = int(menu_item_calories)
        except ValueError:
            msgbox.showerror("Error", "Please enter a valid price and calories for the menu item.")
            return
        
        # Create MenuItem object
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
        """Clears the form fields."""
        self.name_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.calories_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)

    # ORDERS

    def create_orders_tab(self):
        """Creates the orders tab."""

        # Initialize self.order
        self.order = Order()

        # Create label to display "Order"
        self.order_label = tk.Label(self.orders_tab, text="Order")
        self.order_label.pack()

        # Create listbox to display available menu items
        self.available_menu_items_listbox = tk.Listbox(self.orders_tab)
        self.available_menu_items_listbox.pack()

        # Populate listbox with available menu items
        menu_items = self.menu_repo.get_all_menu_items()
        for category, items in menu_items.items():
            for item in items:
                self.available_menu_items_listbox.insert(tk.END, item.name)

        # Create button to add item to order
        self.add_item_button = tk.Button(self.orders_tab, text="Add Item", command=self.add_item_to_order)
        self.add_item_button.pack()

        # Create listbox to display items in order
        self.order_listbox = tk.Listbox(self.orders_tab)
        self.order_listbox.pack()

        # Create labels to display subtotal, tax, and total
        self.subtotal_label = tk.Label(self.orders_tab, text="Subtotal: $0.00")
        self.subtotal_label.pack()
        self.tax_label = tk.Label(self.orders_tab, text="Tax: $0.00")
        self.tax_label.pack()
        self.total_label = tk.Label(self.orders_tab, text="Total: $0.00")
        self.total_label.pack()

        # Create button to clear order
        self.clear_order_button = tk.Button(self.orders_tab, text="Clear Order", command=self.clear_order)
        self.clear_order_button.pack()

    def add_item_to_order(self):
        """Adds the selected menu item to the order and updates the order display."""
        index = self.available_menu_items_listbox.curselection()
        if index and index[0] >= 0:
            menu_item_name = self.available_menu_items_listbox.get(index[0])
            selected_item = self.menu_repo.get_menu_item_by_name(menu_item_name)
            if selected_item:
                # print(f"Selected item: {selected_item[0].name}, Price: {selected_item[0].price}") # TESTING PURPOSES ONLY
                menu_item, _ = selected_item # Extract the MenuItem object from the tuple. THIS WAS DIFFICULT TO FIGURE OUT FOR ME
                self.order.add_item(menu_item)
                self.order_listbox.insert(tk.END, menu_item_name)
                subtotal, tax, total = self.order.total_cost()
                self.subtotal_label.config(text=f"Subtotal: ${subtotal:.2f}")
                self.tax_label.config(text=f"Tax: ${tax:.2f}")
                self.total_label.config(text=f"Total: ${total:.2f}")
            else:
                msgbox.showerror("Error", "Item not found in menu.")
        else:
            msgbox.showerror("Error", "Please select an item from the menu.")

    def clear_order(self):
        """Clears the order."""
        self.order.items = []
        self.order_listbox.delete(0, tk.END)
        self.subtotal_label.config(text="Subtotal: $0.00")
        self.tax_label.config(text="Tax: $0.00")
        self.total_label.config(text="Total: $0.00")

    # INVENTORY

    def create_inventory_tab(self):
        """Creates the inventory tab."""

        # Create listbox to display inventory items
        self.inventory_listbox = tk.Listbox(self.inventory_tab)
        self.inventory_listbox.pack()

        # Create form to add new items
        self.add_item_label = tk.Label(self.inventory_tab, text="Add Item:")
        self.add_item_label.pack()
        self.add_item_name_entry = tk.Entry(self.inventory_tab)
        self.add_item_name_entry.pack()
        self.add_item_quantity_entry = tk.Entry(self.inventory_tab)
        self.add_item_quantity_entry.pack()
        self.add_item_category_entry = tk.Entry(self.inventory_tab)
        self.add_item_category_entry.pack()
        self.add_item_button = tk.Button(self.inventory_tab, text="Add Item", command=self.add_item_to_inventory)
        self.add_item_button.pack()

        # Create buttons to edit and delete existing items
        self.edit_item_button = tk.Button(self.inventory_tab, text="Edit Item", command=self.edit_item_in_inventory)
        self.edit_item_button.pack()
        self.delete_item_button = tk.Button(self.inventory_tab, text="Delete Item", command=self.delete_item_from_inventory)
        self.delete_item_button.pack()

        # Populate listbox with inventory items
        self.update_inventory_listbox()

    def add_item_to_inventory(self):
        """Adds a new item to the inventory."""
        item_name = self.add_item_name_entry.get().strip()
        item_quantity = self.add_item_quantity_entry.get().strip()
        item_category = self.add_item_category_entry.get().strip()

        if not item_name or not item_quantity or not item_category:
            msgbox.showerror("Error", "Please enter all fields.")
            return

        try:
            item_quantity = int(item_quantity)
        except ValueError:
            msgbox.showerror("Error", "Please enter a valid quantity.")
            return

        inventory_repo = InventoryRepository("inventory.db")
        inventory_repo.create_inventory_item(item_name, item_quantity, item_category)
        self.update_inventory_listbox()

    def update_inventory_listbox(self):
        """Updates the listbox with the inventory items."""
        self.inventory_listbox.delete(0, tk.END)
        inventory_repo = InventoryRepository("inventory.db")
        inventory_items = inventory_repo.get_all_inventory_items()
        for item in inventory_items:
            self.inventory_listbox.insert(tk.END, f"{item['item_name']} - {item['quantity']} - {item['category']}")

    def edit_item_in_inventory(self):
        pass

    def delete_item_from_inventory(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = MenuManagerApp(root)
    root.mainloop()