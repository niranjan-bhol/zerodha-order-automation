import json
import os
from tabulate import tabulate

class Create:
    """
    Class to handle order creation and storage in a JSON file.
    """
    order_id_counter = 1  
    orders_list = []  
    json_file = "orders.json"  

    exchange_map = {"1": "NSE", "2": "BSE", "nse": "NSE", "bse": "BSE"}
    transaction_map = {"1": "BUY", "2": "SELL", "buy": "BUY", "sell": "SELL"}
    order_type_map = {"1": "MARKET", "2": "LIMIT", "market": "MARKET", "limit": "LIMIT"}
    product_map = {"1": "MIS", "2": "CNC", "mis": "MIS", "cnc": "CNC"}

    @classmethod
    def load_orders(cls):
        if os.path.exists(cls.json_file):
            with open(cls.json_file, "r") as file:
                try:
                    data = json.load(file)
                    cls.orders_list = data.get("orders", [])
                    cls.order_id_counter = max(order["order_id"] for order in cls.orders_list) + 1 if cls.orders_list else 1
                except json.JSONDecodeError:
                    cls.orders_list = []
                    cls.order_id_counter = 1
        else:
            cls.orders_list = []
            cls.order_id_counter = 1

    @classmethod
    def save_orders(cls):
        with open(cls.json_file, "w") as file:
            json.dump({"orders": cls.orders_list}, file, indent=4)
    
    @staticmethod
    def get_valid_input(prompt, valid_options):
        while True:
            user_input = input(prompt).strip().lower()
            if user_input in valid_options:
                return valid_options[user_input]
            print("❌ Invalid input. Please enter a valid option.")

    @classmethod
    def create_order(cls):
        exchange = cls.get_valid_input("Enter Exchange (NSE/BSE or 1/2): ", cls.exchange_map)
        tradingsymbol = input("Enter Trading Symbol: ").strip().upper()
        transaction_type = cls.get_valid_input("Enter Transaction Type (BUY/SELL or 1/2): ", cls.transaction_map)
        order_type = cls.get_valid_input("Enter Order Type (MARKET/LIMIT or 1/2): ", cls.order_type_map)
        quantity = int(input("Enter Quantity: ").strip())

        price = None
        if order_type == "LIMIT":  
            price = float(input("Enter Price: ").strip())

        product = cls.get_valid_input("Enter Product (MIS/CNC or 1/2): ", cls.product_map)

        order = {
            "order_id": cls.order_id_counter,
            "exchange": exchange,
            "tradingsymbol": tradingsymbol,
            "transaction_type": transaction_type,
            "order_type": order_type,
            "quantity": quantity,
            "product": product
        }

        if price is not None:
            order["price"] = price

        cls.orders_list.append(order)
        cls.order_id_counter += 1  

        cls.save_orders()

        print(f"\n✅ Order Created Successfully! Order ID: {order['order_id']}\n")
        return order


class Read:
    """
    Class to read and display all stored orders in a table format.
    """
    json_file = "orders.json"

    @classmethod
    def load_orders(cls):
        if os.path.exists(cls.json_file):
            with open(cls.json_file, "r") as file:
                try:
                    data = json.load(file)
                    return data.get("orders", [])
                except json.JSONDecodeError:
                    return []
        return []

    @classmethod
    def print_orders(cls):
        orders = cls.load_orders()
        
        if not orders:
            print("\n📌 No orders found.")
            return

        table_data = []
        headers = ["Order ID", "Exchange", "Trading Symbol", "Transaction Type", "Order Type", "Quantity", "Product", "Price"]
        
        for order in orders:
            row = [
                order["order_id"],
                order["exchange"],
                order["tradingsymbol"],
                order["transaction_type"],
                order["order_type"],
                order["quantity"],
                order["product"],
                order.get("price", "-")
            ]
            table_data.append(row)

        print("📜 All Orders:")
        print(tabulate(table_data, headers=headers, tablefmt="grid"))


class Update:
    """
    Class to update existing orders.
    Allows updating only the price and quantity fields.
    """
    json_file = "orders.json"

    @classmethod
    def load_orders(cls):
        if os.path.exists(cls.json_file):
            with open(cls.json_file, "r") as file:
                try:
                    data = json.load(file)
                    return data.get("orders", [])
                except json.JSONDecodeError:
                    return []
        return []

    @classmethod
    def save_orders(cls, orders):
        with open(cls.json_file, "w") as file:
            json.dump({"orders": orders}, file, indent=4)

    @classmethod
    def update_order(cls):
        orders = cls.load_orders()

        if not orders:
            print("\n📌 No orders found.")
            return

        Read.print_orders()
        try:
            order_id = int(input("\nEnter the Order ID to update: ").strip())
        except ValueError:
            print("❌ Invalid input. Order ID must be a number.")
            return

        for order in orders:
            if order["order_id"] == order_id:
                print(f"\n🔄 Updating Order ID: {order_id}")

                try:
                    new_quantity = int(input("Enter new Quantity (leave blank to keep unchanged): ").strip() or order["quantity"])
                except ValueError:
                    print("❌ Invalid quantity. Must be an integer.")
                    return

                new_price = order.get("price", None)
                if order["order_type"] == "LIMIT":
                    try:
                        new_price = float(input("Enter new Price (leave blank to keep unchanged): ").strip() or order.get("price", 0))
                    except ValueError:
                        print("❌ Invalid price. Must be a number.")
                        return

                order["quantity"] = new_quantity
                if new_price is not None:
                    order["price"] = new_price

                cls.save_orders(orders)

                print(f"\n✅ Order ID {order_id} Updated Successfully!\n")
                return

        print(f"❌ Order ID {order_id} not found.")


class Delete:
    """
    Class to delete existing orders.
    """
    json_file = "orders.json"

    @classmethod
    def load_orders(cls):
        if os.path.exists(cls.json_file):
            with open(cls.json_file, "r") as file:
                try:
                    data = json.load(file)
                    return data.get("orders", [])
                except json.JSONDecodeError:
                    return []
        return []

    @classmethod
    def save_orders(cls, orders):
        with open(cls.json_file, "w") as file:
            json.dump({"orders": orders}, file, indent=4)

    @classmethod
    def delete_order(cls):
        orders = cls.load_orders()

        if not orders:
            print("\n📌 No orders found.")
            return

        Read.print_orders()
        try:
            order_id = int(input("\nEnter the Order ID to delete: ").strip())
        except ValueError:
            print("❌ Invalid input. Order ID must be a number.")
            return

        filtered_orders = [order for order in orders if order["order_id"] != order_id]

        if len(filtered_orders) == len(orders):
            print(f"❌ Order ID {order_id} not found.")
            return

        cls.save_orders(filtered_orders)

        print(f"\n✅ Order ID {order_id} Deleted Successfully!\n")


# Load existing orders when the script starts
Create.load_orders()
