import os
from datetime import datetime, timedelta
import time

class DuplicateVisitorError(Exception):
    pass


class LibraryManagementSystem:
    file_path: str = "C:/jomi_pyth/Advanced/Ajani-Jomiloju/Ajani-Jomiloju/visitor.txt"

    def __init__(self):
        self.name = input("Hello there, what is your name?: ")

    # The function creates and reads the visitor file
    def readFile(self):
        try:
            # Creates file if it doesn't exist
            if not os.path.exists(self.file_path):
                print("Creating file")
                time.sleep(1.2)
                self.writeFile()
                return
            #Reads last line
            with open(self.file_path, "r", encoding="utf-8") as rpath:
                lines = rpath.read().splitlines()
                last_line = lines[-1] if lines else None

                if last_line:
                    last_name, last_time_str = last_line.split(" | ")
                    last_time = datetime.strptime(last_time_str, "%Y-%m-%d %H:%M:%S")

                    # Checks name
                    if self.name == last_name and datetime.now() - last_time < timedelta(minutes=5):
                        time.sleep(0.95)
                        raise DuplicateVisitorError("Duplicate visitor! You cannot sign in twice in a row, within 5 minutes.")

            # Writes new visitor
            self.writeFile()

        except FileNotFoundError:
            print("Visitor file not found! Creating a new one...")
            self.writeFile()

        except DuplicateVisitorError as e:
            print(e)

        except Exception as e:
            print("An unexpected error occurred:", e)

    #Writes into file
    def writeFile(self):
        try:
            #Writes in name and time stamp
            with open(self.file_path, "a", encoding="utf-8") as wpath:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                wpath.write(f"{self.name} | {timestamp}\n")
                time.sleep(0.95)
            print(f"Welcome, {self.name}! Your visit has been recorded at {timestamp}.")
        except Exception as e:
            time.sleep(0.5)
            print("Error while writing to file:", e)


def main():
    print("Library Management System Started")
    lbs = LibraryManagementSystem()
    lbs.readFile()


if __name__ == '__main__':
    main()
