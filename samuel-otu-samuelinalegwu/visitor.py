from datetime import datetime, timedelta


class DuplicateVisitorError(Exception):
    def __init__(self, name, minutes=5):
        self.message = (
            f"Visitor '{name}' must wait at least {minutes} minutes before signing in again!"
        )
        super().__init__(self.message)


def main():
    filename = "visitors.txt"

    # Ensure the file exists
    try:
        with open(filename, "r", encoding="utf-8") as f:
            pass
    except FileNotFoundError:
        print("File not found, creating a new file...")
        with open(filename, "w", encoding="utf-8") as f:
            pass

    visitor = input("Enter visitor's name:  ").strip()

    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()

        last_visit_time = None
        # Find the last visit of this visitor in the log
        for line in reversed(lines):
            name, time_str = line.strip().split(" | ")
            if name == visitor:
                last_visit_time = datetime.fromisoformat(time_str)
                break

        # If visitor was found, check the time difference
        if last_visit_time:
            if datetime.now() - last_visit_time < timedelta(minutes=5):
                raise DuplicateVisitorError(visitor, minutes=5)

        # Append new visit
        with open(filename, "a", encoding="utf-8") as f:
            f.write(f"{visitor} | {datetime.now().isoformat()}\n")

        print("Visitor added successfully!")

    except DuplicateVisitorError as e:
        print("Error:", e)


if __name__ == "__main__":
    main()

    main()
