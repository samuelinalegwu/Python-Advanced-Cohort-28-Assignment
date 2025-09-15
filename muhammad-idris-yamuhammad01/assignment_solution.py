import os
import time
from datetime import datetime, timedelta


class DuplicateVisitorError(Exception):
    """Raised when the visitor is the same as the last one in the file"""
    pass


class TooEarlyError(Exception):
    """Raised when a visitor tries to check in within 5 minutes of the last visitor"""
    pass


def get_last_visitor(filename="visitors.txt"): # Reads the last visitor record from the file
    
    if not os.path.exists(filename):
        return None, None
    
    with open(filename, "r") as f:
        lines = f.readlines()
        if not lines:
            return None, None
        last_line = lines[-1].strip() #checks the last line in the file
        try:
            name, timestamp = last_line.split(" | ")
            last_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            return name, last_time
        except ValueError:
            return None, None


def log_visitor(visitor_name, filename="visitors.txt"):
    """Logs visitor with timestamp, enforcing rules"""
    last_name, last_time = get_last_visitor(filename)
    
    # Check duplicate visitor
    if visitor_name == last_name:
        raise DuplicateVisitorError(f"Visitor '{visitor_name}' is already the last recorded visitor.")

    # Check if the user retries before 5-minute 
    if last_time is not None:
        if datetime.now() < last_time + timedelta(minutes=5):
            raise TooEarlyError("A new visitor can only be added 5 minutes after the last visitor.")

    # Append visitor with timestamp
    with open(filename, "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{visitor_name} | {timestamp}\n")


def main():
    try:
        visitor_name = input("Enter visitor name: ").strip() #remove white spaces when collecting the visitors input
        log_visitor(visitor_name)
        print(f"Hey, Visitor {visitor_name}, you are logged in successfully.")
    except DuplicateVisitorError as e:
        print("Error:", e)
    except TooEarlyError as e:
        print("Error:", e)
    except Exception as e:
        print("Unexpected error:", e)


if __name__ == "__main__":
    main()
