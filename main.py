from order import Create, Read, Update, Delete
from utility import display_title
from zerodha_api import ZerodhaLogin, ZerodhaOrders

if __name__ == "__main__":

    display_title()
    
    while True:
        print("\n1️⃣ Create Order")
        print("2️⃣ View All Orders")
        print("3️⃣ Update Order")
        print("4️⃣ Delete Order")
        print("5️⃣ Execute Orders")
        print("6️⃣ Exit")

        choice = input("\nSelect an option (1/2/3/4/5/6): ").strip()
        print("\n")

        if choice == "1":
            Create.create_order()
        elif choice == "2":
            Read.print_orders()
        elif choice == "3":
            Update.update_order()
        elif choice == "4":
            Delete.delete_order()
        elif choice == "5":
            login = ZerodhaLogin()
            enctoken = login.login()
            if enctoken:
                print("✅ Login successful! Enctoken retrieved.")
                orders = ZerodhaOrders()
                orders.execute_orders()
            else:
                print("❌ Login failed.")
        elif choice == "6":
            print("🚀 Exiting... Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, 4, 5 or 6.")
