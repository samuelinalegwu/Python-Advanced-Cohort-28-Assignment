import os
from datetime import datetime

# Custom Exception
class DuplicateVisitorError(Exception):
    pass


FILENAME = "visitors.txt"


def get_last_visitor():
    """Return the last visitor name from file, or None if empty."""
    if not os.path.exists(FILENAME):
        return None
    
    with open(FILENAME, "r") as file:
        lines = file.readlines()
        if not lines:
            return None
        last_line = lines[-1].strip()
        try:
            name, timestamp_str = last_line.split(" - ")
            return name
        except ValueError:
            return None


def add_visitor():
    visitor_name = input("Enter visitor name: ").strip()
    last_name = get_last_visitor()

    # Check duplicate visitor
    if visitor_name == last_name:
        raise DuplicateVisitorError(f"Visitor '{visitor_name}' already signed in last time!")

    # Append new visitor
    with open(FILENAME, "a") as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{visitor_name} - {timestamp}\n")
    print(f"Visitor {visitor_name} recorded successfully!")


if __name__ == "__main__":
    try:
        add_visitor()
    except DuplicateVisitorError as e:
        print("❌ Error:", e)
    except Exception as e:
        print("⚠️ Unexpected error:", e)
