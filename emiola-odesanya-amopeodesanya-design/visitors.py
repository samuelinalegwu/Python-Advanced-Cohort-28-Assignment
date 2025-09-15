import os
from datetime import datetime, timedelta

# Custom exceptions
class DuplicateVisitorError(Exception):
    pass

class TooSoonError(Exception):
    pass

# Constants
FILENAME = "visitors.txt"
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
WAIT_MINUTES = 5

def read_last_entry():
    """Read the last visitor entry and return name and timestamp."""
    if not os.path.exists(FILENAME):
        return None, None
    
    with open(FILENAME, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    
    if not lines:
        return None, None

    last_line = lines[-1]
    try:
        name, time_str = last_line.rsplit(" - ", 1)
        last_time = datetime.strptime(time_str, TIME_FORMAT)
        return name, last_time
    except Exception:
        return None, None

def append_entry(name):
    """Append a new visitor with timestamp to the file."""
    timestamp = datetime.now().strftime(TIME_FORMAT)
    with open(FILENAME, "a", encoding="utf-8") as f:
        f.write(f"{name} - {timestamp}\n")
    return timestamp

def main():
    try:
        name = input("Enter visitor name: ").strip()
        if not name:
            print("No name entered. Exiting.")
            return

        last_name, last_time = read_last_entry()

        # 1. Check for duplicate visitor
        if last_name and name.lower() == last_name.lower():
            raise DuplicateVisitorError(f"{name} was the last visitor — duplicate not allowed.")

        # 2. Check if 5 minutes have passed since last visitor
        if last_time:
            now = datetime.now()
            earliest_allowed = last_time + timedelta(minutes=WAIT_MINUTES)
            if now < earliest_allowed:
                remaining = earliest_allowed - now
                mins = int(remaining.total_seconds() // 60)
                secs = int(remaining.total_seconds() % 60)
                raise TooSoonError(f"Please wait {mins} minute(s) and {secs} second(s) before next visitor.")

        # 3. If all checks passed, log the visitor
        timestamp = append_entry(name)
        print(f"Visitor '{name}' logged at {timestamp}.")

    except DuplicateVisitorError as e:
        print("DuplicateVisitorError:", e)
    except TooSoonError as e:
        print("TooSoonError:", e)
    except Exception as e:
        print("An unexpected error occurred:", e)

if __name__ == "__main__":
    main()
