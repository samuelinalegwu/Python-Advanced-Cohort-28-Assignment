import os
import datetime
import time

class DuplicateVisitorError(Exception):
    pass

def get_last_visitor(file_name):
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()
            if lines:
                last_line = lines[-1].strip()
                return last_line.split(' - ')[0]
    except FileNotFoundError:
        return None

def add_visitor(file_name, name):
    with open(file_name, 'a') as file:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        file.write(f'{name} - {timestamp}\n')

def check_time_gap(file_name):
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()
            if lines:
                last_line = lines[-1].strip()
                last_timestamp = datetime.datetime.strptime(last_line.split(' - ')[1], '%Y-%m-%d %H:%M:%S')
                time_gap = (datetime.datetime.now() - last_timestamp).total_seconds() / 60
                if time_gap < 5:
                    wait_time = 5 - int(time_gap)
                    print(f"Please wait {wait_time} minutes before another visitor can be added.")
                    return False
    except FileNotFoundError:
        pass
    return True

def get_visitor_name():
    while True:
        name = input("Enter visitor's name: ").strip()
        if name:
            return name
        else:
            print("Name cannot be empty. Please enter a valid name.")

def main():
    file_name = 'visitors.txt'
    
    print("Welcome to the Visitor Registration System!")
    print("Please follow the instructions to register a new visitor.")
    
    while True:
        if check_time_gap(file_name):
            name = get_visitor_name()
            last_visitor = get_last_visitor(file_name)
            if name == last_visitor:
                try:
                    raise DuplicateVisitorError("Duplicate visitor not allowed.")
                except DuplicateVisitorError as e:
                    print(e)
                    print("Please enter a different name.")
            else:
                add_visitor(file_name, name)
                print(f"Visitor {name} added successfully.")
                break
        else:
            print("Waiting for the time restriction to pass...")
            time.sleep(60)  # wait for 1 minute before checking again

if __name__== "_main_":
    main()

