import os
from datetime import datetime, timedelta


class DuplicateVisitorError(Exception):
    """Custom exception raised when the same visitor tries to register consecutively."""
    pass


class TooSoonError(Exception):
    """Custom exception raised when a visitor tries to register within 5 minutes of last entry."""
    pass


def read_last_entry(filename):
    """Read the last entry from the visitors file."""
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            if lines:
                return lines[-1].strip()
            return None
    except FileNotFoundError:
        return None


def parse_entry(entry_line):
    """Parse an entry line to extract name and timestamp."""
    if not entry_line:
        return None, None
    
    try:
        # Split by the last occurrence of " - " to separate name and timestamp
        parts = entry_line.rsplit(" - ", 1)
        if len(parts) == 2:
            name = parts[0]
            timestamp_str = parts[1]
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            return name, timestamp
        return None, None
    except ValueError:
        return None, None


def add_visitor(filename, visitor_name):
    """Add a visitor to the file with timestamp."""
    current_time = datetime.now()
    
    # Check if file exists and read last entry
    last_entry = read_last_entry(filename)
    
    if last_entry:
        last_name, last_timestamp = parse_entry(last_entry)
        
        # Check for duplicate visitor (same name as last entry)
        if last_name and last_name.lower() == visitor_name.lower():
            raise DuplicateVisitorError(f"Visitor '{visitor_name}' is already the last registered visitor.")
        
        # Check if 5 minutes have passed since last visitor
        if last_timestamp:
            time_diff = current_time - last_timestamp
            if time_diff < timedelta(minutes=5):
                remaining_time = timedelta(minutes=5) - time_diff
                minutes = int(remaining_time.total_seconds() // 60)
                seconds = int(remaining_time.total_seconds() % 60)
                raise TooSoonError(f"Please wait {minutes} minutes and {seconds} seconds before allowing another visitor.")
    
    # Add the new visitor
    try:
        with open(filename, 'a') as file:
            timestamp_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"{visitor_name} - {timestamp_str}\n")
        print(f"✓ Visitor '{visitor_name}' has been registered successfully at {timestamp_str}")
    except IOError as e:
        print(f"Error writing to file: {e}")
        raise


def display_all_visitors(filename):
    """Display all visitors from the file."""
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            if lines:
                print("\n--- All Visitors ---")
                for i, line in enumerate(lines, 1):
                    print(f"{i}. {line.strip()}")
            else:
                print("No visitors registered yet.")
    except FileNotFoundError:
        print("No visitors file found. No visitors registered yet.")


def main():
    filename = "visitors.txt"
    
    print("=== Visitor Management System ===")
    print("Enter 'quit' to exit or 'show' to display all visitors\n")
    
    while True:
        try:
            visitor_name = input("Enter visitor's name: ").strip()
            
            if visitor_name.lower() == 'quit':
                print("Goodbye!")
                break
            elif visitor_name.lower() == 'show':
                display_all_visitors(filename)
                continue
            elif not visitor_name:
                print("Please enter a valid name.")
                continue
            
            # Try to add the visitor
            add_visitor(filename, visitor_name)
            
        except DuplicateVisitorError as e:
            print(f"❌ Duplicate Visitor Error: {e}")
        except TooSoonError as e:
            print(f"⏰ Too Soon Error: {e}")
        except KeyboardInterrupt:
            print("\n\nProgram interrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"❌ An unexpected error occurred: {e}")
        
        print()  # Add blank line for readability


if __name__ == "__main__":
    main()