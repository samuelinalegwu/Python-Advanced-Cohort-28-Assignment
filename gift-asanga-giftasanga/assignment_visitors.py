import os
from datetime import datetime, timedelta

# Custom Exceptions
class DuplicateVisitorError(Exception):
    pass

class TooSoonError(Exception):
    pass


FILENAME = "visitors.txt"


def get_last_visitor():
    """Return the last visitor name and timestamp from file, or (None, None) if empty."""
    if not os.path.exists(FILENAME):
        return None, None
    
    with open(FILENAME, "r") as file:
        lines = file.readlines()
        if not lines:
            return None, None

        last_line = lines[-1].strip()
        try:
            name, timestamp_str = last_line.split(" - ")
            last_time = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            return name, last_time
        except ValueError:
            return None, None


def add_visitor():
    visitor_name = input("Enter visitor name: ").strip()
    last_name, last_time = get_last_visitor()

    # Check duplicate visitor
    if visitor_name == last_name:
        raise DuplicateVisitorError(f"Visitor '{visitor_name}' already signed in last time!")

    # Check 5-minute restriction
    if last_time is not None and datetime.now() - last_time < timedelta(minutes=5):
        raise TooSoonError("Another visitor cannot be allowed until 5 minutes have passed.")

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
    except TooSoonError as e:
        print("⏳ Wait:", e)
    except Exception as e:
        print("⚠️ Unexpected error:", e)
