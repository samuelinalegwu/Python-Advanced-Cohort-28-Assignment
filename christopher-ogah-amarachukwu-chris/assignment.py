from datetime import datetime, timedelta


class DuplicateVisitorError(Exception):
    """Raised when a visitor with the same name already exists."""
    def __init__(self, name):
        self.message = f"Visitor with name '{name}' already signed in last."
        super().__init__(self.message)


def main():
    file_name = "visitors.txt"

    # Ensure the file exists
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            pass
    except FileNotFoundError:
        with open(file_name, "w", encoding="utf-8") as f:
            pass

    visitor = input("Enter your name: ").strip()

    try:
        last_visitor, last_time = None, None

        with open(file_name, "r", encoding="utf-8") as f:
            lines = f.readlines()
            if lines:  # if file not empty
                last_line = lines[-1].strip()
                parts = last_line.split("|")
                if len(parts) == 2:
                    last_visitor = parts[0].strip()
                    last_time = datetime.strptime(parts[1].strip(), "%Y-%m-%d %H:%M:%S")

        # Duplicate check
        if last_visitor and visitor.lower() == last_visitor.lower():
            raise DuplicateVisitorError(visitor)

        # Time check (5 minutes wait)
        if last_time and datetime.now() - last_time < timedelta(minutes=5):
            wait_seconds = (timedelta(minutes=5) - (datetime.now() - last_time)).seconds
            print(f"Another visitor cannot sign in yet. Please wait {wait_seconds // 60} min {wait_seconds % 60} sec.")
            return

        # Append visitor
        with open(file_name, "a", encoding="utf-8") as f:
            f.write(f"{visitor} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            print("Visitor signed in successfully.")

    except DuplicateVisitorError as e:
        print(e)
    except Exception as e:
        print("Unexpected error:", e)


if __name__ == "__main__":
    main()
