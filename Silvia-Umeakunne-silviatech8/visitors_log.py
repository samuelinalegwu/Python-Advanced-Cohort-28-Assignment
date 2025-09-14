import os
from datetime import datetime, timedelta

#  Custom exception classes 
class DuplicateVisitorError(Exception):
    """Raised when the last visitor name matches the new one."""
    pass

class TooSoonVisitorError(Exception):
    """Raised when less than WAIT_MINUTES (i.e 5mins) passed since last visitor."""
    pass

# Config / constants
FILENAME = "visitors.txt"     # file where we store visitor entries
WAIT_MINUTES = 5              # required minutes between visitors

# Helper: read last entry from the file 
def get_last_entry(filename: str):
    """ Return (name, timestamp) of the last non-empty line in the file.
    If file missing, empty, or parse fails, return (None, None). """
    # If file doesn't exist, nothing to read
    if not os.path.exists(filename):
        return None, None

    # Open file for reading (with ensures it will be closed automatically)
    with open(filename, "r", encoding="utf-8") as f:
        # read and strip blank lines
        lines = [line.strip() for line in f if line.strip()]

    # If file had no non-empty lines
    if not lines:
        return None, None

    last_line = lines[-1]  # last recorded visitor line, e.g. "Alice | 2025-09-14T18:05:12.345678"

    try:
        # Expect format: "Name | ISO_TIMESTAMP"
        name, timestamp_str = last_line.split(" | ")
        # Convert ISO timestamp back to datetime
        timestamp = datetime.fromisoformat(timestamp_str)
        return name, timestamp
    except Exception:
        # If parsing fails (unexpected format), return None so program continues safely
        return None, None

# Main logging logic
def log_visitor(filename: str, visitor_name: str):
    """Check rules, then append visitor and timestamp to file.
    Raises DuplicateVisitorError or TooSoonVisitorError when rules are violated."""
    last_name, last_time = get_last_entry(filename)  # get last entry (or None, None)

    # Rule 1: same name as last visitor (consecutive duplicate) -> error
    if last_name is not None and last_name == visitor_name:
        raise DuplicateVisitorError(f"Visitor '{visitor_name}' is already the last visitor.")

    # Rule 2: require at least WAIT_MINUTES between visitors
    if last_time is not None and (datetime.now() - last_time) < timedelta(minutes=WAIT_MINUTES):
        raise TooSoonVisitorError(f"Please wait at least {WAIT_MINUTES} minutes before the next visitor.")

    # If checks pass, append the visitor with current ISO timestamp
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"{visitor_name} | {datetime.now().isoformat()}\n")

    print(f"✅ Visitor '{visitor_name}' logged successfully.")

# Program entry point 
def main():
    try:
        visitor_name = input("Enter visitor's name: ").strip()  # ask user for there name
        if not visitor_name:
            # handle empty input without crashing
            print("No name entered — nothing recorded.")
            return

        log_visitor(FILENAME, visitor_name)  # try to log the visitor

    except DuplicateVisitorError as e:
        # Controlled message when same consecutive name is entered
        print("Duplicate visitor:", e)

    except TooSoonVisitorError as e:
        # Controlled message when next visitor is too soon
        print("Too soon:", e)

    except Exception as e:
        # Catch-all for anything unexpected (keeps program from crashing)
        print("Unexpected error:", e)

    finally:
        # Always runs: nice place for final messages / cleanup tasks
        print("Program finished. File closed safely.")

if __name__ == "__main__":
    main()
