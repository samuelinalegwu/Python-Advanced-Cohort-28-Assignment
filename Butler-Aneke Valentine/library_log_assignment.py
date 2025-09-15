from datetime import datetime
import os
import time

# 🎯 Custom exceptions
class DuplicateVisitorError(Exception):
    def __init__(self, name):
        super().__init__(f"⚠️ Visitor '{name}' already signed in last! No back-to-back visits allowed.")

class TooSoonVisitorError(Exception):
    def __init__(self, minutes_left):
        super().__init__(
            f"⏳ Please wait {minutes_left:.1f} more minute(s) before the next visitor can sign in."
        )

def pretty_line(char="=", length=45):
    """Print a decorative line for separation."""
    print(char * length)

def show_error(message):
    """💥 Centralized error display with decorative lines."""
    pretty_line("!")
    print(f"❌ Error: {message}")
    pretty_line("!")

def log_visitor(filename, visitor):
    """Check rules and log visitor if allowed."""
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    last_visitor = None
    last_time = None

    if lines:
        last_line = lines[-1].strip()
        parts = last_line.split(" | ")
        if len(parts) == 2:
            last_visitor = parts[0]
            last_time = datetime.fromisoformat(parts[1])

    # 🚫 Duplicate check
    if visitor == last_visitor:
        raise DuplicateVisitorError(visitor)

    # ⏳ 5-minute rule
    if last_time:
        elapsed_minutes = (datetime.now() - last_time).total_seconds() / 60
        if elapsed_minutes < 5:
            raise TooSoonVisitorError(5 - elapsed_minutes)

    # ✅ Append visitor record
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"{visitor} | {datetime.now().isoformat()}\n")

def main():
    filename = "visitors.txt"
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as f:
            pass

    pretty_line()
    print("🎉 Welcome to the Visitor Log System 🎉")
    pretty_line()

    while True:
        visitor = input("👤 Enter visitor's name or type 'X' to exit: ").strip()

        if visitor.lower() == "x":
            pretty_line()
            print("👋 Goodbye! Thanks for using the Visitor Log System.")
            pretty_line()
            break

        if not visitor:
            show_error("Name cannot be empty. Try again.")
            continue

        try:
            log_visitor(filename, visitor)
            pretty_line("-")
            print(f"✨ Visitor '{visitor}' added successfully at "
                  f"{datetime.now().strftime('%H:%M:%S')}! ✨")
            pretty_line("-")

        except (DuplicateVisitorError, TooSoonVisitorError) as e:
            show_error(e)
        except Exception as e:
            show_error(e)

        time.sleep(0.5)

if __name__ == "__main__":
    main()
