import os
import time
from datetime import datetime, timedelta

# Custom exceptions


class DuplicateVisitorError(Exception):
    pass


class TooSoonError(Exception):
    pass


FILENAME = "visitors.txt"


def log_visitor(name):
    # If file doesn't exist, create it
    if not os.path.exists(FILENAME):
        with open(FILENAME, "w") as f:
            pass  # Just create the file

    # Read last line (if any)
    last_name = None
    last_time = None
    with open(FILENAME, "r") as f:
        lines = f.readlines()
        if lines:
            last_line = lines[-1].strip()
            if last_line:
                try:
                    last_name, timestamp = last_line.split(" | ")
                    last_time = datetime.strptime(
                        timestamp, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    pass  # Handle if line format is broken

    # Check for duplicate name
    if name == last_name:
        raise DuplicateVisitorError(f"Duplicate visitor detected: {name}")

    # Check for 5-minute rule
    if last_time and datetime.now() - last_time < timedelta(minutes=5):
        raise TooSoonError(
            f"Another visitor cannot be logged until 5 minutes have passed.")

    # Append new visitor with timestamp
    with open(FILENAME, "a") as f:
        f.write(f"{name} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")


def main():
    try:
        visitor_name = input("Enter visitor's name: ").strip()
        log_visitor(visitor_name)
        print(f"Visitor '{visitor_name}' logged successfully.")
    except DuplicateVisitorError as e:
        print("Error:", e)
    except TooSoonError as e:
        print("Error:", e)
    except Exception as e:
        print("Unexpected error:", e)


if __name__ == "__main__":
    main()
