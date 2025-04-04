import requests
import pyotp
import json
from config import KITE_USERNAME, KITE_PASSWORD, KITE_TOTP_KEY

class ZerodhaLogin:
    def __init__(self):
        """Initialize session and login variables"""
        self.session = requests.Session()
        self.enctoken = None

    def login(self):
        """Performs login and two-factor authentication"""
        try:
            # Step 1: Login Request
            res1 = self.session.post(
                'https://kite.zerodha.com/api/login', 
                data={"user_id": KITE_USERNAME, "password": KITE_PASSWORD, "type": "user_id"}
            )
            login_res = res1.json()
            
            if 'data' not in login_res or 'request_id' not in login_res['data']:
                raise Exception(f"Login failed: {login_res.get('message', 'Unknown error')}")

            # Step 2: Two-Factor Authentication
            return self._twofa_auth(login_res['data']['request_id'], login_res['data']['user_id'])

        except Exception as e:
            print(f"Error during login: {e}")
            return None

    def _twofa_auth(self, request_id, user_id):
        """Handles two-factor authentication"""
        try:
            final_res = self.session.post(
                'https://kite.zerodha.com/api/twofa',
                data={
                    "request_id": request_id,
                    "twofa_value": pyotp.TOTP(KITE_TOTP_KEY).now(),
                    "user_id": user_id,
                    "twofa_type": "totp"
                }
            )
            final_res_json = final_res.json()

            if 'status' not in final_res_json or final_res_json['status'] != 'success':
                raise Exception(f"2FA failed: {final_res_json.get('message', 'Unknown error')}")

            # Step 3: Extract enctoken
            self.enctoken = self.session.cookies.get_dict().get('enctoken')

            if not self.enctoken:
                raise Exception("Failed to retrieve enctoken.")

            return self.enctoken

        except Exception as e:
            print(f"Error during two-factor authentication: {e}")
            return None

    def get_enctoken(self):
        """Returns the stored enctoken after successful login"""
        return self.enctoken

class ZerodhaOrders:
    def __init__(self, orders_file="orders.json"):
        """Initialize with order file path and authentication"""
        self.orders_file = orders_file
        self.enctoken = None
        self.session = requests.Session()

    def authenticate(self):
        """Logs in and retrieves the enctoken"""
        login = ZerodhaLogin()
        self.enctoken = login.login()

        if not self.enctoken:
            raise Exception("Authentication failed! Cannot place orders.")

    def load_orders(self):
        """Loads orders from JSON file"""
        try:
            with open(self.orders_file, "r") as file:
                data = json.load(file)
                return data.get("orders", [])  # Extract orders list
        except Exception as e:
            print(f"Error loading orders: {e}")
            return []

    def place_order(self, order):
        """Places a single order"""
        url = "https://kite.zerodha.com/oms/orders/regular"

        # Remove order_id and add 'variety': 'regular'
        order_data = {"variety": "regular", **{k: v for k, v in order.items() if k != "order_id"}}

        # Add user_id from config
        order_data["user_id"] = KITE_USERNAME

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            "Referer": "https://kite.zerodha.com/dashboard",
            "Accept-Language": "en-US,en;q=0.6",
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": "application/json, text/plain, */*",
            "Authorization": f"enctoken {self.enctoken}",
        }

        response = self.session.post(url, headers=headers, data=order_data)
        return response.json()

    def execute_orders(self):
        """Executes all orders in the JSON file"""
        self.authenticate()  # Login first
        orders = self.load_orders()

        if not orders:
            print("No orders found.")
            return

        
        for order in orders:
            result = self.place_order(order)
            print(f"Order for {order['tradingsymbol']}: {result}")
        
        print("✅ All the orders executed sucessfully.")
