# visitors.py
import datetime
import os

class TooSoonError(Exception):
    """Exception raised when a visitor tries to log in too soon after the last visitor."""
    pass

def read_last_visitor_time():
    """Read the timestamp of the last visitor from the file."""
    if not os.path.exists('visitors.txt'):
        return None
    
    try:
        with open('visitors.txt', 'r') as file:
            lines = file.readlines()
            if not lines:
                return None
            
            # Get the last line and extract timestamp
            last_line = lines[-1].strip()
            if last_line:
                # Assuming format: "timestamp - name"
                parts = last_line.split(' - ', 1)
                if len(parts) == 2:
                    timestamp_str = parts[0]
                    return datetime.datetime.fromisoformat(timestamp_str)
    except (FileNotFoundError, ValueError, IndexError):
        pass
    
    return None

def write_visitor(name):
    """Write the visitor's name and current timestamp to the file."""
    current_time = datetime.datetime.now()
    timestamp = current_time.isoformat()
    
    with open('visitors.txt', 'a') as file:
        file.write(f"{timestamp} - {name}\n")
    
    return current_time

def main():
    print("=== Visitor Log Program ===")
    
    try:
        # Get visitor's name
        name = input("Enter visitor's name: ").strip()
        if not name:
            print("Name cannot be empty!")
            return
        
        # Check last visitor time
        last_visit_time = read_last_visitor_time()
        
        if last_visit_time:
            current_time = datetime.datetime.now()
            time_diff = (current_time - last_visit_time).total_seconds()
            
            if time_diff < 300:  # 5 minutes = 300 seconds
                remaining_time = 300 - time_diff
                raise TooSoonError(
                    f"Too soon! Please wait {remaining_time:.0f} more seconds "
                    f"({remaining_time/60:.1f} minutes) before adding a new visitor."
                )
        
        # Add new visitor
        visit_time = write_visitor(name)
        print(f"Visitor '{name}' logged successfully at {visit_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
    except TooSoonError as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()