import logging
from datetime import datetime, timedelta
from typing import Optional


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)


# Custom Exceptions
class DuplicateVisitorError(Exception):
    """Raised when the same visitor tries to enter twice in a row."""
    pass


class TooSoonError(Exception):
    """Raised when a new visitor comes in before 5 minutes have passed."""
    pass


class VisitorLog:
    def __init__(self, filename: str = "visitors.txt") -> None:
        self.filename = filename

    def get_last_entry(self) -> Optional[tuple[str, datetime]]:
        """
        Read the last line in the file and return (name, timestamp).
        If file is empty or missing, return None.
        """
        try:
            with open(self.filename, "r") as file:
                last_line = None
                for line in file:  # stream line by line
                    if line.strip():
                        last_line = line.strip()

                if not last_line:
                    return None

                name, time_str = last_line.split(" | ")
                timestamp = datetime.fromisoformat(time_str)
                return name, timestamp

        except FileNotFoundError:
            return None
        except ValueError as e:
            logging.error(f"Error parsing last entry: {e}")
            raise
        except OSError as e:
            logging.error(f"File error: {e}")
            raise

    def add_visitor(self, name: str) -> None:
        """
        Add a visitor with the current timestamp.
        Rules:
        - No duplicate names in a row
        - At least 5 minutes gap between visitors
        """
        last_entry = self.get_last_entry()
        now = datetime.now()

        if last_entry:
            last_name, last_time = last_entry

            # Rule 1: No duplicate names
            if last_name.lower() == name.lower():
                raise DuplicateVisitorError(f"Duplicate visitor: {name}")

            # Rule 2: 5 minutes gap
            if now - last_time < timedelta(minutes=5):
                minutes_left = 5 - (now - last_time).seconds // 60
                raise TooSoonError(
                    f"Please wait {minutes_left} more minute(s) before logging a new visitor."
                )

        # Append visitor to file
        try:
            with open(self.filename, "a") as file:
                file.write(f"{name} | {now.isoformat()}\n")
            logging.info(f"Visitor {name} added at {now.strftime('%Y-%m-%d %H:%M:%S')}")
        except OSError as e:
            logging.error(f"Could not write to file: {e}")
            raise


def main() -> None:
    log = VisitorLog()

    try:
        visitor_name: str = input("Enter visitor name: ").strip()
        log.add_visitor(visitor_name)
    except DuplicateVisitorError as e:
        logging.warning(e)
    except TooSoonError as e:
        logging.warning(e)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise


if __name__ == "__main__":
    main()
