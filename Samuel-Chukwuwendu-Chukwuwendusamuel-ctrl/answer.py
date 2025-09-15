import os
from datetime import datetime, timedelta

# Custom exception for duplicate visitors
class DuplicateVisitorError(Exception):
    """Raised when a visitor tries to check in again within 5 minutes."""
    pass


def read_last_line(filename):
    """Read the last non-empty line of a file. Returns None if file is empty or doesn't exist."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # Return the last non-empty line
            for line in reversed(lines):
                if line.strip():
                    return line.strip()
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"⚠️  Error reading file: {e}")
        return None


def get_timestamp():
    """Return current timestamp as string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def is_duplicate_within_5_minutes(last_entry, new_name):
    """
    Check if the last entry has the same name and was within the last 5 minutes.
    Returns True if duplicate (within 5 min), False otherwise.
    """
    if not last_entry:
        return False

    # Expected format: "Name [YYYY-MM-DD HH:MM:SS]"
    if '[' not in last_entry or ']' not in last_entry:
        return False

    try:
        # Extract name and timestamp
        name_part = last_entry[:last_entry.rfind(' [')]
        timestamp_str = last_entry[last_entry.rfind(' [') + 2:-1]
        last_time = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        current_time = datetime.now()

        # Check if name matches and time difference < 5 minutes
        if name_part == new_name and (current_time - last_time) < timedelta(minutes=5):
            return True
    except ValueError:
        # If timestamp parsing fails, assume it's not a valid duplicate
        return False

    return False


def main():
    store = os.path.join("Princewill-Okereke-CrimsonKarma44", "store")
    filename = os.path.join(store, "visitors.txt")

    if not os.path.exists(store):
        os.makedirs(store)

    if not os.path.exists(filename):
        open(filename, 'w', encoding='utf-8').close()
    
    while True:
        try:
            name = input("Enter visitor's name (or 'quit' to exit): ").strip()

            if name.lower() == 'quit':
                print("👋 Exiting program.")
                break

            if not name:
                print("❌ Name cannot be empty. Try again.")
                continue

            # Read the last entry
            last_entry = read_last_line(filename)

            # Check if this visitor was here within the last 5 minutes
            if is_duplicate_within_5_minutes(last_entry, name):
                raise DuplicateVisitorError(
                    f"🚫 Visitor '{name}' checked in less than 5 minutes ago. Please wait."
                )

            # Write the new entry with timestamp
            with open(filename, 'a', encoding='utf-8') as f:
                f.write(f"{name} [{get_timestamp()}]\n")

            print(f"✅ Visitor '{name}' checked in at {get_timestamp()}.")

        except DuplicateVisitorError as e:
            print(str(e))
        except PermissionError:
            print("❌ Permission denied. Cannot write to file. Please check file permissions.")
        except Exception as e:
            print(f"❌ An unexpected error occurred: {e}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Program interrupted. Exiting.")
