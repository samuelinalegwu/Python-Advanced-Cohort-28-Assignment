from datetime import datetime, timedelta

#Custom Exceptions
class DuplicateVisitorError(Exception):
    def __init__(self, name):
        self.message = f"Visitor '{name}' already signed in last! No back-to-back visits allowed."
        super().__init__(self.message)

class TooSoonError(Exception):
    def __init__(self, minutes_left):
        self.message = f"Too soon! Please wait {minutes_left} more minute(s) before the next visitor."
        super().__init__(self.message)

#Constants
FILENAME = "visitors.txt"
TIME_LIMIT = 5  # minutes

#Helper Function
def get_last_record():
    """Return the last visitor's (name, time) from the file, or (None, None) if empty/missing."""
    try:
        with open(FILENAME, "r") as f:
            lines = f.readlines()
            if lines:
                last_line = lines[-1].strip()
                # Format: "Name - Timestamp"
                name, time_str = last_line.split(" - ")
                last_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
                return name, last_time
    except FileNotFoundError:
        return None, None
    return None, None

def add_visitor(name):
    """Add a visitor with timestamp, enforcing duplicate & 5-minute rule."""
    last_name, last_time = get_last_record()
    now = datetime.now()

    if last_name == name:
        raise DuplicateVisitorError(name)

    if last_time:
        time_diff = now - last_time
        if time_diff < timedelta(minutes=TIME_LIMIT):
            minutes_left = TIME_LIMIT - int(time_diff.total_seconds() // 60)
            raise TooSoonError(minutes_left)

    with open(FILENAME, "a") as f:
        f.write(f"{name} - {now.strftime('%Y-%m-%d %H:%M:%S')}\n")

    print(f"Visitor '{name}' added successfully at {now.strftime('%Y-%m-%d %H:%M:%S')}.")

#Main Program
def main():
    try:
        visitor_name = input("Enter visitor's name: ").strip()

        if not visitor_name:
            print("Visitor name cannot be empty.")
            return

        add_visitor(visitor_name)

    except (DuplicateVisitorError, TooSoonError) as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
