# MenuManager

Author: Jesse Fry
version beta
03/08/2025

This is a simple menu management system to be used by a small-scale mon-and-pop style restaurant. It allows the user to view the current menu, edit the menu, calculate the price of an order (including tax). and keep track of inventory items.

## Introduction

This project is a menu management system designed as the final project for my Software Development with Python college course. My roommate has a dream of opening up a small restaurant, so I decided to base my project around his idea. It solves the problem of keeping track of menu items and changes, and inventory availability. There are future updates planned that have not been implemented yet, including the ability to save the menu as a formated text document, saving an order receipt as the same, and adding discount abilities to Orders tab. I sadly got a late start on the project, and the deadline is in less than two hours. I'm excited to keep working on it moving forward, though!

## Features and Functionality

* Create and update menu items.
* Keep track of menu item:
    Name
    Description
    Price
    Calories
    Category
* Mock order displays:
    Items on order
    Subtotal
    Tax
    Total
* Keep track or restaurant inventory items:
    Name
    Quantity
    Category
* Saves Menu Items and Inventory in databases.

## Usage

There are four tabs at the top, each giving access to a different part of the program.

1. Menu
    This displays the full current menu, along with all information about each item.
    The menu is sorted by category: Entrees, Sides, Beverages, and Desserts.

2. Menu Items
    A list box at the top contains every menu item.
    You can create, edit, or delete menu items from this tab.
    * Create:
        Don't click on an item. Just fill in the desired information, and click the save button.
        A confirmation box will pop up if successful.
        Name and description are text strings.
        Price is a floating point number.
        Calories is an integer.
        Category is a selection from the dropdown box (Entrees, Sides, Beverages, Desserts).
    * Edit:
        Click on the item you want to edit in the list box at the top.
        Click the Edit button.
        The fields will automatically populate.
        Change any data you would like.
        Click the save button.
        A confirmation box will pop up if successful.
    * Delete:
        Click on the item you want to delete in the list box at the top.
        Click the Edit button.
        The fields will automatically populate.
        Click the Delete button.
        Click the Save button.
        A confirmation box will pop up if successful.
        CAUTION!!! Make sure you follow this procedure exactly. It can be a little finicky, but I did not have the time to make the process more robust yet.
    The Menu tab will be automatically updated.

3. Orders
    A list box at the top contains every menu item.
    Click the item you would like to add to the order.
    Click the Add Item button.
    This will add the item to the order, and display it on the list box on the bottom.
    Subtotal, Tax, and Total are automatically calculated and updated beneath the second list box every time an item is added.
    The Clear Order button clears all items from the order and resets the Subtotal, Tax, and Total values.

4. Inventory
    A list box at the top contains every inventory item.
    You can create, edit, or delete inventory items from this tab.
    * Create:
        Don't click on an item. Just fill in the desired information, and click the save button.
        The item will be added to inventory.
        If the item already existe, a yes or no box will pop up asking if you wish to procees.
        CAUTION!!! This will not add to the inventory, it will replace it.
        Name is a text string.
        Quantity is an integer.
        Category is a selection from the dropdown box (Food, Cleaning Supplies, Misc).
    * Edit:
        Click the item you want to edit.
        Click the Edit Item button.
        The fields will automatically populate.
        Change any data you would like.
        Click the save button.
        A confirmation box does not pop up currently. It will be implemented in the near future.
    * Delete:
        Click on the item you want to delete in the list box at the top.
        Click the Edit Item button.
        The fields will automatically populate.
        Click the Delete Item button.
        A yes or no box will ask if you are sure.
        Click the Save button.

## Dependencies and Requirements

Just standard Python library. This program uses Tkinter and sqlite3.

# Known Issues

* Menu Items tab, it is possible to delete an item without clicking Edit or Save button, however this does not correctly remove it from the database.

## Contact

If you have any questions or want to get in touch, please email me at jfry59@ivytech.edu or visit my GitHub profile at https://github.com/DKJesseJamesFK
