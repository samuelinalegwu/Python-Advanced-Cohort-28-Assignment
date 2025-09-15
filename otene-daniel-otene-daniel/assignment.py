import os
from datetime import datetime, timedelta

class DuplicateVisitorError(Exception):
    pass

class TooSoonVisitorError(Exception):
    pass

def get_last_visitor(filename):
    """Return (name, timestamp) of the last visitor, or (None, None) if file missing/empty."""
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
            if lines:
                last_line = lines[-1].strip()
                if last_line:
                    try:
                        name, ts = last_line.split(',')
                        return name, datetime.strptime(ts.strip(), "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        # If line is malformed, ignore it
                        return None, None
        return None, None
    except FileNotFoundError:
        return None, None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None, None

def add_visitor(filename, name):
    """Append a visitor entry with timestamp."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        with open(filename, 'a') as f:
            f.write(f"{name},{timestamp}\n")
    except Exception as e:
        print(f"Error writing to file: {e}")

def main():
    filename = "visitors.txt"
    try:
        name = input("Enter visitor's name: ").strip()

        last_visitor, last_time = get_last_visitor(filename)

        if last_visitor and last_visitor.lower() == name.lower():
            raise DuplicateVisitorError(f"❌ Duplicate visitor: {name}")

        if last_time and datetime.now() < last_time + timedelta(minutes=5):
            raise TooSoonVisitorError(
                f"❌ Last visitor was at {last_time}. Please wait 5 minutes before logging another visitor."
            )

        add_visitor(filename, name)
        print(f"✅ Welcome, {name}! Your visit has been recorded.")

    except DuplicateVisitorError as e:
        print(e)
    except TooSoonVisitorError as e:
        print(e)
    except Exception as e:
        print(f"⚠️ An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
