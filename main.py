from exceptions import QuitException
from io_utils import IO

io = IO()

WELCOME_MESSAGE = "Welcome to our super cool application!!"
GOODBYE_MESSAGE = "Thank you for using our super cool application. Goodbye!"

try:
    io.print(WELCOME_MESSAGE)

    # How to capture user input
    email = io.input('Enter your email:', io.VALID_EMAIL)
    io.print(f"Your email is: {email}")

    phone_number = io.input('Enter your phone number in format xxx-xxx-xxxx:', io.VALID_PHONE)
    io.print(f"Your phone number is: {phone_number}")

    # How to render multiple options.
    # Note that the method returns the option that user selected
    options = ['Add item', 'Edit item', 'Delete item']
    user_selection = io.print_options(options)

    # So you can build your own logic to handle the user selection
    if user_selection == options[0]:
        # do some actual logic here
        user_input = io.input('Enter item you want to add: ')
        io.print(f"You have entered {user_input}")
    elif user_selection == options[1]:
        # do some actual logic here
        user_input = io.input('Enter item you want to edit: ')
        io.print(f"You have entered {user_input}")
    elif user_selection == options[2]:
        # do some actual logic here
        user_input = io.input('Enter item you want to delete: ')
        io.print(f"You have entered {user_input}")

except QuitException:
    # This is made to gracefully handle quite at any moment
    io.print(GOODBYE_MESSAGE)
