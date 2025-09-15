from datetime import datetime

# Define a Custom Exception for duplicate visitors
class DuplicateVisitorError(Exception):
    def __init__(self, name):
        # set a custom message if a visitor tries to sign in twice in a row
        self.message = f'Visitor {name} already exists! No back to back visits allowed'
        # Call the base Exception class with this message
        super().__init__(self.message)

# Define the main function that runs the program
def main():
    # The name of the file where the names are stored
    filename = "visitors.txt"

    # Ensure the file exists before we start using it
    try:
        # Try opening the file in read mode
        with open(filename, "r", encoding="utf-8") as visitors:
            pass
    except FileNotFoundError: # if file does not exist create the file by opening in read mode
        print("Visitors file not found, creating...")
        with open(filename, "w", encoding="utf-8") as visitors:
            pass # Just create a new line

    # Ask user for visitor's name
    visitor = input("Enter a visitor name: ")
        # Open the file to read the existing visitors list
    try:
        with open(filename, "r", encoding="utf-8") as visitors:
            # Read all limes into a list
            lines = visitors.readlines()
            # Get the name of the last visitor
            last_visitor = lines[-1].split(" | ")[0] if lines else None

            if visitor == last_visitor:
                # if yes, raise our custom error
                raise DuplicateVisitorError(visitor)

        # if not a duplicate, open the file in append mode
        with (open("visitors.txt","a", encoding="utf-8")) as visitors:
            # write the visitors name and the current date and time
            visitors.write(f"{visitor} | {datetime.now()}\n")

        # Tell the user everything worked
        print("Visitor added successfully")

    except DuplicateVisitorError as e:
        print("Duplicate Visitor")

if __name__ == "__main__":
    main()

