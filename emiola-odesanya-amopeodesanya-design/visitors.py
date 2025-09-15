import os
from datetime import datetime, timedelta

# Custom exception for duplicate visitor
class DuplicateVisitorError(Exception):
    pass

# File to store visitor logs
FILENAME = "visitors.txt"

def get_last_visitor():
    """Return the last visitor's name and timestamp from the file."""
    if not os.path.exists(FILENAME):
        return None, None

    with open(FILENAME, "r") as file:
        lines = file.readlines()
        if not lines:
            return None, None
        last_line = lines[-1].strip()
        try:
            name, timestamp_str = last_line.rsplit(" - ", 1)
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            return name, timestamp
        except ValueError:
            return None, None

def add_visitor(name):
    """Add a new visitor to the file if valid."""
    last_name, last_time = get_last_visitor()

    # Check for duplicate name
    if last_name == name:
        raise DuplicateVisitorError(f"{name} is already the last visitor!")

    # Check 5-minute gap
    if last_time and datetime.now() - last_time < timedelta(minutes=5):
        remaining = timedelta(minutes=5) - (datetime.now() - last_time)
        print(f"Please wait {remaining.seconds // 60} minutes and {remaining.seconds % 60} seconds before adding a new visitor.")
        return

    # Add visitor with timestamp
    with open(FILENAME, "a") as file:
        file.write(f"{name} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    print(f"Visitor {name} added successfully!")

def main():
    try:
        visitor_name = input("Enter visitor's name: ").strip()
        if not visitor_name:
            print("Name cannot be empty!")
            return

        add_visitor(visitor_name)

    except DuplicateVisitorError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
