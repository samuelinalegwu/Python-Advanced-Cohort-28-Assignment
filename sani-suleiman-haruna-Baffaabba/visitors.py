from datetime import datetime, timedelta

class DuplicateVisitorError(Exception):
  pass

class TimeLimitError(Exception):
  pass


filename = "visitors.txt"
wait_period = timedelta(minutes=5)

try:
  with open(filename, "r", encoding="utf-8") as f:
    pass
except FileNotFoundError:
  print("File not found, creating a new file.")
  with open(filename, "w", encoding="utf-8") as f:
    pass 
  
visitor = input("Enter visitor's name: ")

try:
  with open(filename, "r", encoding="utf-8") as f:
    lines = f.readlines()
    
  if lines:
    last_entry = lines[-1].strip()
    last_visitor, last_timestamp_str = last_entry.split(" | ")
    
    if visitor == last_visitor:
      raise DuplicateVisitorError(f"Visitor '{visitor}' already signed in last. No back-to-back visits allowed.")
      
    last_timestamp = datetime.fromisoformat(last_timestamp_str)
    current_time = datetime.now()
    
    if (current_time - last_timestamp) < wait_period:
      time_remaining = wait_period - (current_time - last_timestamp)
      minutes = int(time_remaining.total_seconds() // 60)
      seconds = int(time_remaining.total_seconds() % 60)
      message = f"Cannot sign in yet. Please wait another {minutes}m {seconds}s."
      raise TimeLimitError(message)
  
  with open(filename, "a", encoding="utf-8") as f:
    f.write(f"{visitor} | {datetime.now().isoformat()}\n")
    
  print("Visitor added successfully!")

except DuplicateVisitorError as e:
  print(f"Error: {e}")
except TimeLimitError as e:
  print(f"Error: {e}")
except ValueError:
  print("Error: Could not parse a timestamp from the file. The file may be corrupted.")
