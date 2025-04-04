# Zerodha Order Automation

This project allows users to place, update, read, and delete orders programmatically using the terminal. The automation is achieved by making HTTP requests on the Zerodha Kite platform.

## 📥 Installation

### 1️⃣ Clone the Repository

```sh
git clone https://github.com/niranjan-bhol/zerodha-order-automation.git
cd zerodha-order-automation
```

### 2️⃣ Install Dependencies
Make sure you have Python installed, then run:

```sh
pip install -r requirements.txt
```

### 3️⃣ Set Up Environment Variables
Create a .env file and add your Zerodha credentials:

```sh
KITE_USERNAME=your_username
KITE_PASSWORD=your_password
KITE_TOTP_KEY=your_totp_secret
```

### 4️⃣ Run the Application
To place orders:

```sh
python main.py
```

Follow the on-screen options to execute various actions.

## 📚 Resources

- Zerodha Kite API Docs: [link](https://kite.trade/docs/connect/v3/)
- YouTube Tutorial: [link](https://youtu.be/HIpT1in7pCM?si=cnPrd9LJGfE-ln44)

## 🛑 Disclaimer
This project is for educational purposes only. Use at your own risk.
