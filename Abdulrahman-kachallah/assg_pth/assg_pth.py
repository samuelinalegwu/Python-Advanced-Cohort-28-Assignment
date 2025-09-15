import os
from datetime import datetime, timedelta
class DuplicateVisitorError(Exception):
    pass
class TooSoonError(Exception):
    pass
def add_visitor(filename="visitors.txt"):
    name = input("Please enter a username : ")
    now = datetime.now()
    try:
        with open(filename, "r", encoding="UTF-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = []
    if lines:
        last_line = lines[-1].strip()
        
        last_name, last_time_str = last_line.split("-", 1)
        last_time = datetime.fromisoformat(last_time_str)
        if name == last_name:
            raise DuplicateVisitorError(f"Duplicate visitor : {name}")
        if now < last_time + timedelta(minutes=5):
            raise TooSoonError(f"Its too soon, Next visitor allowed after {last_time + timedelta(minutes=5)}")
    with open(filename, "a", encoding="UTF-8") as f:
        f.write(f"{name}-{now.isoformat()}\n")
    print(f"Visitor {name} added at {now.strftime('%H:%M:%S')}")
try:
    add_visitor()
except DuplicateVisitorError as e:
    print("error: ", e)
except TooSoonError as e:
    print("error: ", e)
except Exception as e:
    print("error: ", e)

