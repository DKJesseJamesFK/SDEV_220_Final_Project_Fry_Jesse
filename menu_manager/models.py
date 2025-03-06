import sqlite3

class MenuItem:
    def __init__(self, name, description, price, calories):
        """
        Initialize a MenuItem object.

        :param name: the name of the menu item
        :param description: the description of the menu item
        :param price: the price of the menu item
        :param calories: the number of calories in the menu item
        """
        self.name = name
        self.description = description
        self.price = price
        self.calories = calories

    def __str__(self):
        return f"{self.name}: {self.description} ${self.price} ({self.calories} calories)"
    
class Menu:
    def __init__(self):
        self.items = []

    def __str__(self):
        menu_str = "Menu:\n"
        for i, item in enumerate(self.items, start=1):
            menu_str += f"{i}. {item}\n"
        return menu_str
    
class Order:
    TAX_RATE = 0.07
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def total_cost(self):
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
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS menu_items (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                calories INTEGER
            );
        """)
        self.conn.commit()

    def create_menu_item(self, item):
        self.cursor.execute("""
            INSERT INTO menu_items (name, description, price, calories)
            VALUES (?, ?, ?, ?);
        """, (item.name, item.description, item.price, item.calories))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_menu(self, item_id):
        self.cursor.execute("SELECT * FROM menu_items WHERE id = ?;", (item_id,))
        row = self.cursor.fetchone()
        if row:
            return MenuItem(row[1], row[2], row[3], row[4])
        return None

    def update_menu_item(self, item_id, updated_item):
        self.cursor.execute("""
            UPDATE menu_items
            SET name = ?, description = ?, price = ?, calories = ?
            WHERE id = ?;
        """, (updated_item.name, updated_item.description, updated_item.price, updated_item.calories, item_id))
        self.conn.commit()

    def delete_menu_item(self, item_id):
        self.cursor.execute("DELETE FROM menu_items WHERE id = ?;", (item_id,))
        self.conn.commit()

    def get_all_menu_items(self):
        self.cursor.execute("SELECT * FROM menu_items;")
        rows = self.cursor.fetchall()
        menu_items = []
        for row in rows:
            menu_item = MenuItem(row[1], row[2], row[3], row[4])
            menu_items.append(menu_item)
        return menu_items