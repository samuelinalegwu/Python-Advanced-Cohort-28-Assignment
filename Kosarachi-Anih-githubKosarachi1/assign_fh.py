# Import the datetime class from the datetime module
from datetime import datetime, timedelta

# Define a custom exception for duplicate visitors
class DuplicateVisitorError(Exception):
    def __init__(self, name):
        self.message = f"Visitor '{name}' already signed in last! No back-to-back visits allowed."
        super().__init__(self.message)

# Define a custom exception for 5-minute wait rule
class TooSoonError(Exception):
    def __init__(self, minutes_left):
        self.message = f"Another visitor cannot sign in yet. Please wait {minutes_left} more minute(s)."
        super().__init__(self.message)

def main():
    filename = "visitors.txt"

    # Ensure file exists
    try:
        with open(filename, "r", encoding="utf-8") as f:
            pass
    except FileNotFoundError:
        print("File not found, creating a new one...")
        with open(filename, "w", encoding="utf-8") as f:
            pass

    # Ask user for visitor's name
    visitor = input("Enter visitor's name: ").strip()

    try:
        last_visitor, last_time = None, None
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
            if lines:
                last_line = lines[-1].strip().split(" | ")
                last_visitor = last_line[0]
                last_time = datetime.fromisoformat(last_line[1])

        # Rule 1: No duplicate back-to-back visitor
        if visitor == last_visitor:
            raise DuplicateVisitorError(visitor)

        # Rule 2: Enforce 5-minute gap between visitors
        if last_time:
            time_diff = datetime.now() - last_time
            if time_diff < timedelta(minutes=5):
                minutes_left = 5 - int(time_diff.total_seconds() // 60)
                raise TooSoonError(minutes_left)

        # If all checks pass → add visitor
        with open(filename, "a", encoding="utf-8") as f:
            f.write(f"{visitor} | {datetime.now().isoformat()}\n")

        print("Visitor added successfully!")

    except (DuplicateVisitorError, TooSoonError) as e:
        print("Error:", e)
    except Exception as e:
        print("Unexpected error:", e)

# Run the program
if __name__ == "__main__":
    main()
