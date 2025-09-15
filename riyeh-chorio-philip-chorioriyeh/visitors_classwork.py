#Import the datetime class from the datetime module
from datetime import datetime
today = datetime.today()
print(today)
print(today.year)

#Define a custom exception for duplicate visitors
class DuplicateVisitorError(Exception):
    def __init__(self, name):
        #Set a custom message if the visitor signs in twice
        self.message = (f"Visitor {name} already signed in last! No back to back visits allowed")
        super().__init__(self.message)

#Define the main function
def main():
    #Name of file where visitor records are stored
    filename = "visitors.txt"

    #Ensure the file exists before usage
    try:
        with open("visitors.txt", "r", encoding="utf-8") as f:
            pass #Do nothing Just check if file exists
    except FileNotFoundError:
        print("File not found")
        #If file doesn't exist
        with open("visitors.txt", "w", encoding="utf-8") as f:
            pass #Just create the file

#Ask for user input
visitor = input("Enter your name: ")

try:
    #Open the file to read the existing visitor records
    with open("visitors.txt", "r", encoding="utf-8") as f:
        #Read all entries into a list
        lines = f.readlines()
        #Get the name of the last visitor
        last_visitor = lines[-1].split(" | ")[0] if lines else None

    #Check if new visitor is same as last
    if visitor == last_visitor:
        #if yes, raise the Duplicate error
        raise DuplicateVisitorError(visitor)

    #if not a duplicate
    with open("visitors.txt", "a", encoding="utf-8") as f:
        #Write the visitor's name with the current date and time
        f.write(f"{visitor} | {datetime.now()}\n")

    #Tell the user that it worked fine
    print("User added successfully")

#Catch the custom error if a duplicate is detected
except DuplicateVisitorError as e:
    print("Error ", e)



# while True:
#     try:
#         with open("visitors.txt", "a", encoding="utf-8") as f:
#             f.write(input("Enter your Fullname here: \n"))
#     except DuplicateVisitorError:
#         print("Visitor has already been added")
