import os
import datetime

# Custom Exceptions
class DuplicateVisitorError(Exception):
    pass

class VisitorWaitError(Exception):
    pass

def add_visitor():
    file_name = "visitors.txt"
    visitor_name = input("Enter visitor's name: ").strip()

    if not os.path.exists(file_name):
        with open(file_name, "w") as f:
            pass

    try:
        with open(file_name, "r") as f:
            lines = f.readlines()

        if lines:
            last_line = lines[-1].strip()
            last_visitor, last_time_str = last_line.split(" - ")
            last_time = datetime.datetime.strptime(last_time_str, "%Y-%m-%d %H:%M:%S")

            # Duplicate check
            if visitor_name == last_visitor:
                raise DuplicateVisitorError(f"Visitor '{visitor_name}' already logged last time!")

            # Time difference check (5 mins = 300 seconds)
            now = datetime.datetime.now()
            diff = (now - last_time).total_seconds()
            if diff < 300:  # less than 5 minutes
                raise VisitorWaitError("Another visitor must wait at least 5 minutes!")

        # Add visitor
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(file_name, "a") as f:
            f.write(f"{visitor_name} - {timestamp}\n")

        print(f"Visitor '{visitor_name}' added successfully.")

    except (DuplicateVisitorError, VisitorWaitError) as e:
        print("Error:", e)

    except Exception as e:
        print("An unexpected error occurred:", e)

if __name__ == "__main__":
    add_visitor()