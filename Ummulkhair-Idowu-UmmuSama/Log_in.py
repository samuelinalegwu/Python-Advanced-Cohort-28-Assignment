#import os
# Import the datetime class from the datetime module
from datetime import datetime, timedelta


# Define a custom exception for duplicate visitors
class DuplicateVisitorError(Exception):
    def __init__(self, name):
        # Set a custom message if a visitor tries to sign in twice in a row
        self.message = f"Visitor '{name}' already signed in last! No back to back visits allowed."
        # Call the base Exception class with this message
        super().__init__(self.message)

# Define a custom exception for time restriction
class TooSoonError(Exception):
  def __init__(self, next_allowed_time):
    # Set a custom message if a visitor tries to sign in before time condition
    self.message = f"Next visitor must wait until {next_allowed_time.strftime('%H:%M:%S')}."
    # Call the base Exception class with this message
    super().__init__(self.message)

# Define the main function that runs the program
def main():
    # The name of the file where the visitor records are stored
    filename = "visitors.txt"

    # Ensure the file exists before we start using it
    try:
        # Try opening the file in read mode
        with open(filename, "r", encoding="utf-8") as f:
            pass  # Do nothing, just check if file exists
    except FileNotFoundError:
        # If file does not exist, create the file by opening in write mode
        print("file not found, creating a new file")
        with open(filename, "w", encoding="utf-8") as f:
            pass  # create a new line

    # Ask the user to type the visitor's name
    visitor = input("Enter visitor's name")

    try:
        # Open the file to read the existing visitors' records
        with open(filename, "r", encoding="utf-8") as f:
            # Read all lines into a list
            lines = f.readlines()
            # Get the name of the last visitor
            last_visitor = lines[-1].split(" | ")[0] if lines else None
            # Get the time of last visitor's login
            last_time = None
            if lines:
                # Extract the timestamp string and convert back to datetime
                time_str = lines[-1].split(" | ")[1].strip()
                last_time = datetime.fromisoformat(time_str)

        # Check if the new visitor is the same as last
        if visitor == last_visitor:
            # If yes, raise our custom DuplicateVisitorError
            raise DuplicateVisitorError(visitor)

        # Check for 5-minute wait condition
        if last_time and datetime.now() < last_time + timedelta(minutes=5):
            #calculate the earliest valid entry time - 5 minutes after the last visitor's timestamp
            next_allowed = last_time + timedelta(minutes=5)
            #stop and raise custom exception
            raise TooSoonError(next_allowed)

        # If not a duplicate, open the file in append mode
        with open(filename, "a", encoding="utf-8") as f:
            # write the visitor's name and the current date and time
            f.write(f"{visitor} | {datetime.now()}\n")

        # Tell the user everything worked fine
        print("Visitor added successfully!")

    # Catch the custom error if a duplicate user was detected
    except DuplicateVisitorError as e:
        # Print out the error message
        print("Error:", e)
    # Catch the custom error if another visitor tries to enter before wait condition
    except TooSoonError as e:
        # Print out the error message
        print("Error:", e)


# Run the program
main()