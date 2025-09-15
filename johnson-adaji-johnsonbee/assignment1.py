from datetime import datetime, timedelta

# define a custom exception for duplicate visitors
class DuplicateVisitorError(Exception):
    def __init__(self, name):
        # set custom message if a visitor appears as a duplicate
        self.message = f"visitor '{name}' already signed in, no back visits allowed!"
        # call the base exception class with this message
        super().__init__(self.message)

# define a custom exception for visitors coming too soon
class TooSoonError(Exception):
    def __init__(self, time_remaining):
        # set custom message for visitors coming too soon
        self.message = f"Another visitor was here recently. Please wait {time_remaining} more minutes."
        # call the base exception class with this message
        super().__init__(self.message)

# define the main function that runs the program
def main():
    # the name of the file where the visitors records are stored
    filename = "visitors.txt"
    
    # ensure the file exists before we start using it
    try:
        # try opening the file in read mode
        with open(filename, "r", encoding="utf-8") as f:
            pass  # do nothing just check if file exists
    except FileNotFoundError:
        # if file does not exist, create file by writing in write mode
        with open(filename, "w", encoding="utf-8") as f:
            pass  # just create an empty file
    
    # ask user input
    visitor = input("enter visitors name: ")
    
    try:
        # open the file to read the existing visitors record
        with open(filename, "r", encoding="utf-8") as f:
            # read the lines into a list
            lines = f.readlines()
            
            if lines:
                # get the last visitor's info
                last_line = lines[-1].strip()
                last_visitor_name = last_line.split(" | ")[0]
                last_visitor_time_str = last_line.split(" | ")[1]
                
                # convert the timestamp string back to datetime object
                last_visitor_time = datetime.strptime(last_visitor_time_str, "%Y-%m-%d %H:%M:%S.%f")
                
                # check if new visitor is same as last visitor
                if visitor == last_visitor_name:
                    raise DuplicateVisitorError(visitor)
                
                # check if 5 minutes have passed since last visitor
                current_time = datetime.now()
                time_difference = current_time - last_visitor_time
                five_minutes = timedelta(minutes=5)
                
                if time_difference < five_minutes:
                    # calculate remaining time
                    remaining_time = five_minutes - time_difference
                    remaining_minutes = int(remaining_time.total_seconds() / 60) + 1
                    raise TooSoonError(remaining_minutes)
        
        # if not duplicate and enough time has passed, open file in append mode
        with open(filename, "a", encoding="utf-8") as f:
            # write visitors name and current date and time
            f.write(f"{visitor} | {datetime.now()}\n")
        
        # tell user everything worked fine
        print("added successfully")
    
    # catch the custom error if a duplicate user was detected
    except DuplicateVisitorError as e:
        print("Error:", e)
    
    # catch the custom error if visitor came too soon
    except TooSoonError as e:
        print("Error:", e)

if __name__ == "__main__":
    main()