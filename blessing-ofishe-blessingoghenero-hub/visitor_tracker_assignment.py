import os
from datetime import datetime

class DuplicateVisitorError(Exception):
    """Custom exception raised when the same visitor tries to sign in consecutively."""
    pass

def get_last_visitor_name(filename):
    """
    Get the name of the last visitor from the file.
    Returns None if file doesn't exist or is empty.
    """
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            if lines:
                # Get the last line and extract the name (everything before the first ' - ')
                last_line = lines[-1].strip()
                if ' - ' in last_line:
                    return last_line.split(' - ')[0]
                return last_line
            return None
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def add_visitor(filename, visitor_name):
    """
    Add a visitor to the file with timestamp.
    Raises DuplicateVisitorError if the same name was the last entry.
    """
    # Check for duplicate visitor
    last_visitor = get_last_visitor_name(filename)
    if last_visitor and last_visitor.lower() == visitor_name.lower():
        raise DuplicateVisitorError(f"Visitor '{visitor_name}' is already the most recent entry!")
    
    # Add visitor with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"{visitor_name} - {timestamp}\n"
    
    try:
        with open(filename, 'a') as file:
            file.write(entry)
        print(f"✓ Successfully added '{visitor_name}' to the visitor log.")
    except Exception as e:
        print(f"Error writing to file: {e}")
        raise

def display_recent_visitors(filename, count=5):
    """Display the most recent visitors."""
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            if lines:
                print(f"\n--- Last {min(count, len(lines))} visitors ---")
                for line in lines[-count:]:
                    print(f"  {line.strip()}")
            else:
                print("\nNo visitors yet.")
    except FileNotFoundError:
        print("\nNo visitor log found yet.")
    except Exception as e:
        print(f"Error reading visitor log: {e}")

def main():
    """Main program loop."""
    filename = "visitors.txt"
    
    print("=== Visitor Tracking System ===")
    print("Type 'quit' to exit the program\n")
    
    while True:
        try:
            # Get visitor name
            visitor_name = input("Enter visitor's name: ").strip()
            
            # Check for exit condition
            if visitor_name.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            # Validate input
            if not visitor_name:
                print("⚠️  Name cannot be empty. Please try again.\n")
                continue
            
            # Add visitor to log
            add_visitor(filename, visitor_name)
            
            # Show recent visitors
            display_recent_visitors(filename)
            print()
            
        except DuplicateVisitorError as e:
            print(f"⚠️  Duplicate visitor detected: {e}")
            print("The same person cannot sign in twice in a row.\n")
            
        except KeyboardInterrupt:
            print("\n\nProgram interrupted by user. Goodbye!")
            break
            
        except Exception as e:
            print(f"❌ An unexpected error occurred: {e}")
            print("The program will continue running.\n")

if __name__ == "__main__":
    main()
