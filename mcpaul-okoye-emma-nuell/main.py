import os
from typing import Optional, Tuple
from datetime import datetime, timedelta


# Custom exceptions for the visitor management system.
class DuplicateVisitorError(Exception):
    """Raised when the same visitor tries to visit twice in a row"""

    def __init__(self, name: str):
        self.name = name
        super().__init__(f"Duplicate visitor: {name} already visited last!")


class VisitTooSoonError(Exception):
    """Raised when a visitor tries to visit within 5 minutes of the last visit"""

    def __init__(self, time_left: float):
        self.time_left = time_left
        super().__init__(
            f"Please wait {time_left:.1f} more minutes before the next visit"
        )


# File handling operations for visitor management.
class VisitorFileHandler:
    """Handles file operations for visitor records"""

    def __init__(self, filename: str = "visitors.txt"):
        self.filename = filename

    def ensure_file_exists(self) -> None:
        """Create the visitors file if it doesn't exist"""
        try:
            if not os.path.exists(self.filename):
                with open(self.filename, "w", encoding="utf-8") as f:
                    f.write("")  # Create empty file
                print(f"Created new file: {self.filename}")
            else:
                print(f"File {self.filename} already exists.")
        except IOError as e:
            print(f"Error creating file: {e}")
            raise

    def get_last_visitor_info(self) -> Optional[Tuple[str, datetime]]:
        """
        Get the last visitor's name and timestamp from the file.

        Returns:
            Tuple of (name, timestamp) if file has content, None otherwise
        """
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                lines = f.readlines()

            if not lines:
                return None

            last_line = lines[-1].strip()
            if not last_line:
                return None

            # Parse the last line
            parts = last_line.split(" - ")
            if len(parts) >= 2:
                name = parts[0]
                timestamp_str = " - ".join(parts[1:])
                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                return (name, timestamp)

            return None

        except (IOError, ValueError) as e:
            print(f"Error reading last visitor info: {e}")
            return None

    def add_visitor(self, name: str) -> None:
        """Add a new visitor to the file with timestamp"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(self.filename, "a", encoding="utf-8") as f:
                f.write(f"{name} - {timestamp}\n")
            print(f"Visitor '{name}' added successfully at {timestamp}")
        except IOError as e:
            print(f"Error adding visitor: {e}")
            raise


# Validation logic for visitor management.
class VisitorValidator:
    """Validates visitor entries based on rules"""

    @staticmethod
    def validate_visitor(
        name: str, last_visitor_info: Optional[Tuple[str, datetime]]
    ) -> None:
        """
        Validate if a visitor can be added based on set rules

        Args:
            name: The visitor's name
            last_visitor_info: Tuple of (last_name, last_timestamp) or None

        Raises:
            DuplicateVisitorError: If the same visitor visited last
            VisitTooSoonError: If less than 5 minutes have passed since last visit
        """
        if last_visitor_info is None:
            return  # First visitor, no validation needed

        last_name, last_timestamp = last_visitor_info

        # Check for duplicate visitor
        if name.strip().lower() == last_name.strip().lower():
            raise DuplicateVisitorError(name)

        # Check if 5 minutes have passed
        current_time: datetime = datetime.now()
        time_diff: timedelta = current_time - last_timestamp
        min_wait_time: timedelta = timedelta(minutes=5)

        if time_diff < min_wait_time:
            remaining_time: timedelta = min_wait_time - time_diff
            remaining_minutes: float = remaining_time.total_seconds() / 60.0
            raise VisitTooSoonError(remaining_minutes)



# Main visitor management logic
class VisitorManager:
    """Main class for managing visitor operations"""

    def __init__(self, filename: str = "visitors.txt"):
        self.file_handler = VisitorFileHandler(filename)
        self.validator = VisitorValidator()

    def initialize(self) -> None:
        """Initialize the visitor system by ensuring file exists"""
        self.file_handler.ensure_file_exists()

    def get_visitor_name(self) -> str:
        """Get visitor name from user input"""
        while True:
            name = input("Please enter your name: ").strip()
            if name:
                return name
            print("Name cannot be empty. Please try again.")

    def process_visitor(self) -> bool:
        """
        Process a new visitor entry

        Returns:
            True if visitor was successfully processed, False otherwise
        """
        try:
            name = self.get_visitor_name()
            last_visitor_info = self.file_handler.get_last_visitor_info()

            # Validate the visitor
            self.validator.validate_visitor(name, last_visitor_info)

            # Add the visitor
            self.file_handler.add_visitor(name)
            return True

        except DuplicateVisitorError as e:
            print(f"Error: {e}")
            return False

        except VisitTooSoonError as e:
            print(f"Error: {e}")
            return False

    def run(self) -> None:
        """Main program loop"""
        print("=== Visitor Adding System ===")

        try:
            self.initialize()

            while True:
                print("\nOptions:")
                print("1. Add new visitor")
                print("2. Exit")

                choice = input("Choose an option (1-2): ").strip()

                if choice == "1":
                    success = self.process_visitor()
                    if success:
                        print("Visitor processed successfully!")

                elif choice == "2":
                    print("Thank you for using the Visitor Management System!")
                    break

                else:
                    print("Invalid choice. Please enter 1 or 2.")

        except KeyboardInterrupt:
            print("\n\nProgram interrupted by user. Goodbye!")



# Entry point for the visitor management system.
def main():
    """Main function to run the visitor management system."""
    manager = VisitorManager()
    manager.run()


if __name__ == "__main__":
    main()
