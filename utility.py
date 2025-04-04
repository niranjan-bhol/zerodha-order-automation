import json
import os

# Function to display the project title
def display_title():
    print("\nZerodha Order Management System")

def load_json_data(filename):
    """Load data from a JSON file."""
    if os.path.exists(filename):
        with open(filename, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}

def save_json_data(filename, data):
    """Save data to a JSON file."""
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

def get_valid_input(prompt, valid_options):
    """Validate user input against predefined options."""
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in valid_options:
            return valid_options[user_input]
        print("❌ Invalid input. Please enter a valid option.")
