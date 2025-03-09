import sqlite3
import tkinter as tk

class MenuItem:
    """A class representing a menu item."""
    def __init__(self, name, description, price, calories, category):
        """
        Initialize a MenuItem object.

        :param name: the name of the menu item
        :param description: the description of the menu item
        :param price: the price of the menu item
        :param calories: the number of calories in the menu item
        :param category: the category of the menu item
        """
        self.name = name
        self.description = description
        self.price = price
        self.calories = calories
        self.category = category

    def __str__(self):
        return f"{self.name}: {self.description} ${self.price} ({self.calories} calories)"
    
class Menu:
    """A class representing a menu of menu items."""
    def __init__(self):
        self.items = []

    def __str__(self):
        menu_str = "Menu:\n"
        for i, item in enumerate(self.items, start=1):
            menu_str += f"{i}. {item}\n"
        return menu_str
    
class Order:
    """A class representing an order of menu items."""
    TAX_RATE = 0.07
    def __init__(self):
        self.items = []

    def add_item(self, item):
        """Add a menu item to the order."""
        self.items.append(item)

    def total_cost(self):
        """Calculate the total cost of the order, including subtotal, tax, and total."""
        print()
        subtotal = sum(item.price for item in self.items)
        total_tax = subtotal * Order.TAX_RATE
        total_cost = subtotal + total_tax
        return subtotal, total_tax, total_cost
    
    def __str__(self):
        order_str = "Order:\n"
        for i, item in enumerate(self.items, start=1):
            order_str += f"{i}. {item}\n"
        subtotal, total_tax, total_cost = self.total_cost()
        order_str += f"Subtotal: ${subtotal:.2f}\n"
        order_str += f"Tax ({Order.TAX_RATE*100}%): ${total_tax:.2f}\n"
        order_str += f"Total: ${total_cost:.2f}"
        return order_str

class MenuRepository:
    """A class for interacting with the menu database."""
    def __init__(self, db_name):
        """
        Initialize the MenuRepository object.

        :param db_name: the name of the sqlite database file
        """
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()
    #    self.add_test_data() # Add test data

    def create_table(self):
        """Create the menu_items table if it doesn't exist."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS menu_items (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                calories INTEGER,
                category TEXT NOT NULL
            );
        """)
        self.conn.commit()

    def create_menu_item(self, item):
        """Add a menu item to the database."""
        self.cursor.execute("""
            INSERT INTO menu_items (name, description, price, calories, category)
            VALUES (?, ?, ?, ?, ?);
        """, (item.name, item.description, item.price, item.calories, item.category))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_menu(self, item_id):
        """Return a single menu item from the database."""
        self.cursor.execute("SELECT * FROM menu_items WHERE id = ?;", (item_id,))
        row = self.cursor.fetchone()
        if row:
            return MenuItem(row[1], row[2], row[3], row[4], row[5])
        return None

    def update_menu_item(self, item_id, updated_item):
        """Update a single menu item in the database."""
        self.cursor.execute("""
            UPDATE menu_items
            SET name = ?, description = ?, price = ?, calories = ?, category = ?
            WHERE id = ?;
        """, (updated_item.name, updated_item.description, updated_item.price, updated_item.calories, updated_item.category, item_id))
        self.conn.commit()

    def delete_menu_item(self, item_id):
        """Delete a single menu item from the database."""
        self.cursor.execute("DELETE FROM menu_items WHERE id = ?;", (item_id,))
        self.conn.commit()

    def get_menu_item_by_name(self, name):
        """Return a menu item and its ID from the database based on its name."""
        # print(f"Searching for menu item: {name}") # TESTING PURPOSES ONLY
        self.cursor.execute("SELECT * FROM menu_items WHERE name = ?;", (name,))
        row = self.cursor.fetchone()
        if row:
            # print(f"Database row found {row}") # TESTING PURPOSES ONLY
            menu_item = MenuItem(row[1], row[2], row[3], row[4], row[5])  # Create MenuItem object
            return menu_item, row[0]  # Return both MenuItem object and its ID
        # print("Menu item not found in database.") # TESTING PURPOSES ONLY
        return None, None  # Return None if not found

    def get_all_menu_items(self):
        """Return all menu items from the database. Separated by category."""
        self.cursor.execute("SELECT * FROM menu_items;")
        rows = self.cursor.fetchall()
        menu_items = []
        entrees = []
        sides = []
        beverages = []
        desserts = []

        for row in rows:
            menu_item = MenuItem(row[1], row[2], row[3], row[4], row[5])
            menu_items.append(menu_item)
            if menu_item.category == "Entrees":
                entrees.append(menu_item)
            elif menu_item.category == "Sides":
                sides.append(menu_item)
            elif menu_item.category == "Beverages":
                beverages.append(menu_item)
            elif menu_item.category == "Desserts":
                desserts.append(menu_item)
        return {
            "Entrees": entrees,
            "Sides": sides,
            "Beverages": beverages,
            "Desserts": desserts
        }
    
    # def add_test_data(self):
    #     """TESTING PURPOSES ONLY"""
    #     self.cursor.execute("""
    #         INSERT INTO menu_items (name, description, price, calories, category)
    #         VALUES
    #             ('Burger', 'A juicy beef burger', 10.99, 500, 'Entrees'),
    #             ('Grilled Chicken', 'A grilled chicken breast', 9.99, 400, 'Entrees'),
    #             ('Fries', 'Crispy french fries', 4.99, 200, 'Sides'),
    #             ('Salad', 'A fresh green salad', 3.99, 100, 'Sides'),
    #             ('Soda', 'A cold soda', 2.99, 150, 'Beverages'),
    #             ('Iced Tea', 'A refreshing iced tea', 1.99, 0, 'Beverages'),
    #             ('Ice Cream', 'A scoop of creamy ice cream', 5.99, 300, 'Desserts'),
    #             ('Brownie', 'A rich, fudgy brownie', 4.99, 250, 'Desserts');
    #     """)
    #     self.conn.commit()

class InventoryRepository:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_inventory_table()

    def create_inventory_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY,
                item_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                category TEXT
            );
        """)
        self.conn.commit()

    def create_inventory_item(self, item_name, quantity, category):
        self.cursor.execute("""
            INSERT INTO inventory (item_name, quantity, category)
            VALUES (?, ?, ?);
        """, (item_name, quantity, category))
        self.conn.commit()

    def get_inventory_item(self, item_id):
        self.cursor.execute("SELECT * FROM inventory WHERE id = ?;", (item_id,))
        row = self.cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "item_name": row[1],
                "quantity": row[2],
                "category": row[3]
            }
        return None

    def update_inventory_item(self, item_id, item_name, quantity, category):
        self.cursor.execute("""
            UPDATE inventory
            SET item_name = ?, quantity = ?, category = ?
            WHERE id = ?;
        """, (item_name, quantity, category, item_id))
        self.conn.commit()

    def delete_inventory_item(self, item_id):
        self.cursor.execute("DELETE FROM inventory WHERE id = ?;", (item_id,))
        self.conn.commit()

    def get_all_inventory_items(self):
        """Gets all inventory items from the database."""
        self.cursor.execute("SELECT * FROM inventory;")
        rows = self.cursor.fetchall()
        inventory_items = []
        for row in rows:
            inventory_item = {
                "id": row[0],
                "item_name": row[1],
                "quantity": row[2],
                "category": row[3]
            }
            inventory_items.append(inventory_item)
        return inventory_items
    
    def get_inventory_item_by_name(self, name):
        """Gets an inventory item by name."""
        self.cursor.execute("SELECT * FROM inventory WHERE item_name = ?", (name,))
        row = self.cursor.fetchone()
        if row:
            inventory_item = {
                "id": row[0],
                "name": row[1],
                "quantity": row[2],
                "category": row[3]
            }
            return inventory_item
        else:
            return None