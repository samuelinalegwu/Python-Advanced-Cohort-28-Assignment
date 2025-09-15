import os
# Exercise 1: Reading Safely
def read_stud():
    try:
        with open("students.txt", "r") as file:
            print(file.read())
    except FileNotFoundError:
        print("Sorry, the file 'students.txt' does not exist!")

# Exercise 2: Writing and Reading
def fave_movies():
    movies = [] #creating a variable for the series
    print("Enter your favorite movies (type 'done' to close):")
    while True:
        movie = input("Movie name: ")
        if movie.lower() == "done":
            break
        movies.append(movie)

    with open("movies.txt", "w") as file:
        for movie in movies:
            file.write(movie + "\n")

    print("\nYour favorite movies are:")
    with open("movies.txt", "r") as file:
        print(file.read())

# Exercise 3: Append Mode (Diary Program)
def diary():
    entry = input("Write your diary entry: ")
    with open("diary.txt", "a") as page:
        page.write(entry + "\n")
    print("Diary entry saved!")

# Exercise 4: Exception Handling/Error handling
def error_handling():
    filename = input("Enter the filename: ")
    try:
        with open(filename, "r") as file:
            print(file.read())
    except FileNotFoundError:
        print("Oops, no such file!")

# Exercise 5: Custom Exception
class EmptyFileError(Exception):
    """Raised when the file is empty"""
    pass

def empty_file():
    filename = input("Enter the filename: ")
    try:
        with open(filename, "r") as file:
            content = file.read()
            if not content.strip():
                raise EmptyFileError("The file is empty!")
            print(content)
    except FileNotFoundError:
        print("File not found!")
    except EmptyFileError as e:
        print(e)

# Exercise 6: Witty Challenge (forgive_me.py)
def witty():
    if not os.path.exists("apology.txt"):
        apology = input("File not found. Write an apology message: ")
        with open("apology.txt", "w") as file:
            file.write(apology)
        print("Apology saved in apology.txt")
    else:
        print("The file apology.txt already exists.")



# Example function calls

# Exercise 1
read_stud()  
# ➝ Tries to read "students.txt" and prints its contents (or shows an error if missing).

# Exercise 2
fave_movies()  
# ➝ Prompts you to type movies one by one. End with "done". It then saves and prints them.

# Exercise 3
diary()  
# ➝ Prompts you for a diary entry and appends it to "diary.txt".

# Exercise 4
error_handling()  
# ➝ Asks for a filename, tries to open it, prints contents or shows "Oops, no such file!".

# Exercise 5
empty_file()  
# ➝ Asks for a filename, checks if it’s empty, raises `EmptyFileError` if so.

# Exercise 6
witty()  
# ➝ Checks if "apology.txt" exists. If not, it asks you for an apology message and saves it.
