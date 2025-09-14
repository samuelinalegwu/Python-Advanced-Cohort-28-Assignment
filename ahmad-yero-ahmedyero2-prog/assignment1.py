from datetime import datetime, timedelta

# Define a Custom Exception for duplicate visitors
class DuplicateVisitorError(Exception):
    def __init__(self, name):
        self.message = f'Visitor {name} already exists! No back-to-back visits allowed.'
        super().__init__(self.message)

# Define a Custom Exception for visit intervals
class VisitTooSoonError(Exception):
    def __init__(self, wait_time):
        self.message = f"Too soon to log another visitor. Please wait {wait_time} more minutes."
        super().__init__(self.message)

def main():
    filename = "visitors.txt"

    # Ensure the file exists
    try:
        with open(filename, "r", encoding="utf-8"):
            pass
    except FileNotFoundError:
        print("Visitors file not found, creating...")
        with open(filename, "w", encoding="utf-8"):
            pass

    visitor = input("Enter a visitor name: ").strip()

    try:
        with open(filename, "r", encoding="utf-8") as visitors:
            lines = visitors.readlines()
            if lines:
                last_line = lines[-1].strip()
                last_visitor, last_time_str = last_line.split(" | ")
                last_time = datetime.fromisoformat(last_time_str.strip())

                # Check for duplicate visitor
                if visitor == last_visitor:
                    raise DuplicateVisitorError(visitor)

                # Check if 5 minutes have passed
                time_diff = datetime.now() - last_time
                if time_diff < timedelta(minutes=5):
                    remaining = 5 - int(time_diff.total_seconds() // 60)
                    raise VisitTooSoonError(remaining)

        # Append the new visitor entry
        with open(filename, "a", encoding="utf-8") as visitors:
            visitors.write(f"{visitor} | {datetime.now().isoformat()}\n")

        print("Visitor added successfully.")

    except DuplicateVisitorError as e:
        print(e)
    except VisitTooSoonError as e:
        print(e)

if __name__ == "__main__":
    main()