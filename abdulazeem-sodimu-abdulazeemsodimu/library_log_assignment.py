from datetime import datetime, timedelta

# Create the custom exceptions
class DuplicateVisitorError(Exception):
    pass

class InsufficientTimeError(Exception):
    pass


def main():
    # Check if visitors.txt exists
    try:
        with open('visitors.txt') as file:
            pass
    except FileNotFoundError:
        print('File does not exist. Creating File....')
        with open('visitors.txt', 'w') as file:
            pass

    # Load data from file
    with open('visitors.txt') as file:
        data: list[str] = file.readlines()

    # Get current time
    now = datetime.now()

    try:
        # Get user input
        name: str = input('Enter your name>>> ')

        # If data is empty
        if data == []:
            data.append(f'{name} | {now}')

        # If data is not empty
        else:
            # Get the last-entry
            last_name, last_time = data[-1].split('|')

            # Check last entry
            if name == last_name.strip():
                raise DuplicateVisitorError('Duplicate Visitor Detected')
            
            # Check time
            if now - datetime.strptime(last_time.strip(), '%Y-%m-%d %H:%M:%S.%f') < timedelta(minutes=5):
                raise InsufficientTimeError('Wait until after 5 minutes')

            data.append(f'\n{name} | {now}')

        # Store in visitors.txt
        with open('visitors.txt', 'w') as file:
            file.writelines(data)

        # Give the user a response when successful
        print('Done!')
        
    except DuplicateVisitorError as e:
        print(f'Error: {e}')
    except InsufficientTimeError as e:
        print(f'Error: {e}')

main()
