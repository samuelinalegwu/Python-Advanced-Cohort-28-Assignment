from datetime import datetime

class DuplicateVisitorError(Exception):
    pass

file = "visitors.txt"
name = input("Enter visitor name: ")

try:
    try:
        with open(file, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = []

    if lines:
        last = lines[-1].strip()
        last_name, last_time = last.split(" - ")
        last_time = datetime.strptime(last_time, "%Y-%m-%d %H:%M:%S")

        if last_name == name:
            raise DuplicateVisitorError("Same name as last visitor!")

        minutes = (datetime.now() - last_time).total_seconds() / 60
        if minutes < 5:
            print("Wait at least 5 minutes before another visitor!")
            exit()

    with open(file, "a") as f:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(name + " - " + now + "\n")

    print("Visitor saved.")

except DuplicateVisitorError as e:
    print(e)
except Exception as e:
    print("Error:", e)