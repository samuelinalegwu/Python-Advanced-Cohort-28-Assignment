# Import the datetime class from the datetime module
from datetime import datetime, timedelta

today = datetime.today()
print(today)
print(today.year)

# Define a custom exception for duplicate visitors
class DuplicateVisitorError(Exception):
    def __init__(self, name):
        self.message = (f"Visitor {name} already signed in last! No back-to-back visits allowed.")
        super().__init__(self.message)

# Define a custom exception for time restriction
class TimeRestrictionError(Exception):
    def __init__(self, minutes):
        self.message = (f"New entry not allowed until {minutes} minutes have passed since last entry.")
        super().__init__(self.message)

# Define the main function
def main():
    filename = "visitor-date.txt"

    # Ensure the file exists before usage
    try:
        with open(filename, "r", encoding="utf-8") as f:
            pass
    except FileNotFoundError:
        with open(filename, "w", encoding="utf-8") as f:
            pass

    # Ask for user input
    visitor = input("Enter your name: ")

    try:
        # Open the file to read the existing visitor records
        with open("visitor-date.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            last_visitor = None
            last_time = None

            if lines:
                last_entry = lines[-1].strip().split(" | ")
                last_visitor = last_entry[0]
                last_time = datetime.strptime(last_entry[1], "%Y-%m-%d %H:%M:%S.%f")

        # Check if same visitor is signing in again
        if visitor == last_visitor:
            raise DuplicateVisitorError(visitor)

        # Check if 5 minutes have passed
        if last_time and datetime.now() < last_time + timedelta(minutes=5):
            raise TimeRestrictionError(5)

        # If all checks passed, write new entry
        with open("visitor-date.txt", "a", encoding="utf-8") as f:
            f.write(f"{visitor} | {datetime.now()}\n")

        print("User added successfully!")

    except DuplicateVisitorError as e:
        print("Error:", e)

    except TimeRestrictionError as e:
        print("Error:", e)


# Run the program
if __name__ == "__main__":
    main()
