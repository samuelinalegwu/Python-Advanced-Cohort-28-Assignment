import datetime
import os


# Step 1: Create a custom exception
class DuplicateVisitorError(Exception):
    """Custom exception raised when the same visitor tries to enter consecutively"""

    def __init__(self, name):
        self.name = name
        super().__init__(f"Duplicate visitor: {name} is already the last visitor!")


def get_last_visitor_info(filename):
    """
    Get the last visitor's name and timestamp from the file
    Returns: (name, timestamp) or (None, None) if file is empty
    """
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            if lines:
                # Get the last line and strip whitespace
                last_line = lines[-1].strip()
                if last_line:
                    # Split the line to get name and timestamp
                    # Format: "Name - YYYY-MM-DD HH:MM:SS"
                    parts = last_line.split(' - ')
                    if len(parts) >= 2:
                        name = parts[0]
                        timestamp_str = parts[1]
                        # Convert timestamp string back to datetime object
                        timestamp = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                        return name, timestamp
            return None, None
    except FileNotFoundError:
        # File doesn't exist yet
        return None, None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None, None


def add_visitor(filename, visitor_name):
    """
    Add a visitor to the file with timestamp
    """
    current_time = datetime.datetime.now()

    # Check if the same visitor is trying to enter again
    last_name, last_timestamp = get_last_visitor_info(filename)

    if last_name and last_name.lower() == visitor_name.lower():
        raise DuplicateVisitorError(visitor_name)

    # ASSIGNMENT PART: Check if enough time has passed since last visitor
    if last_timestamp:
        time_difference = current_time - last_timestamp
        if time_difference.total_seconds() < 300:  # 300 seconds = 5 minutes
            minutes_left = 5 - (time_difference.total_seconds() / 60)
            raise Exception(f"Please wait {minutes_left:.1f} more minutes before next visitor can enter.")

    # Add the visitor with timestamp
    try:
        with open(filename, 'a') as file:  # 'a' for append mode
            file.write(f"{visitor_name} - {current_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        print(f"✓ {visitor_name} has been added to the visitor log at {current_time.strftime('%H:%M:%S')}")
    except Exception as e:
        print(f"Error writing to file: {e}")


def main():
    """Main function to run the visitor management system"""
    filename = "visitors.txt"

    print("=== Visitor Management System ===")
    print("Note: Only one visitor allowed every 5 minutes")

    while True:
        try:
            # Ask for visitor's name
            visitor_name = input("\nEnter visitor's name (or 'quit' to exit): ").strip()

            if visitor_name.lower() == 'quit':
                print("Goodbye!")
                break

            if not visitor_name:
                print("Please enter a valid name.")
                continue

            # Try to add the visitor
            add_visitor(filename, visitor_name)

        except DuplicateVisitorError as e:
            print(f"❌ Error: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")
        except KeyboardInterrupt:
            print("\n\nProgram interrupted. Goodbye!")
            break


def show_visitor_log(filename="visitors.txt"):
    """Helper function to display all visitors (for testing)"""
    print("\n=== Current Visitor Log ===")
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                lines = file.readlines()
                if lines:
                    for i, line in enumerate(lines, 1):
                        print(f"{i}. {line.strip()}")
                else:
                    print("No visitors yet.")
        else:
            print("Visitor file doesn't exist yet.")
    except Exception as e:
        print(f"Error reading visitor log: {e}")


if __name__ == "__main__":
    # Uncomment the line below to see current visitor log before starting
    # show_visitor_log()
    main()