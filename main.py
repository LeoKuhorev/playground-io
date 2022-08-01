import random
from exceptions import QuitException
from io_utils import IO


io = IO()

WELCOME_MESSAGE = "Welcome to our super cool application!!"
GOODBYE_MESSAGE = "Thank you for using our super cool application. Goodbye!"
CARRIERS = ["AT&T", "Verizon", "T-Mobile", "Sprint"]
OPTIONS = ['Add item', 'Edit item', 'Delete item']
WEBSITES = ["Amazon", "Ebay", "Bestbuy", "Walmart"]

items = []


try:
    io.print(WELCOME_MESSAGE)

    user_email = io.input('Please enter your email:', io.VALID_EMAIL)
    io.print("User not found!", style=IO.COLOR_WARNING)
    phone_number = io.input(
        'Please enter your phone number in format xxx-xxx-xxxx:', io.VALID_PHONE)
    user_carrier = io.print_options(CARRIERS, "Please select your carrier:")

    io.print(
        f"New user created!\nEmail: {user_email}\nPhone: {phone_number}\nCarrier: {user_carrier}", style=IO.COLOR_SUCCESS)

    while True:
        user_selection = io.print_options(OPTIONS if len(
            items) > 0 else OPTIONS[:1], "Please select an option:")

        if user_selection == OPTIONS[0]:
            new_item = {"links": []}
            new_item['name'] = io.input('Please enter item name: ')

            user_selection = io.print_options(
                ["Yes", "No"], "Do you want to add a link?")
            while user_selection == "Yes":
                website = io.print_options(
                    WEBSITES, "Please select a website:")
                link = io.input('Please enter a link:', io.VALID_URL)
                new_item["links"].append(
                    {"website": website, "link": link, "price": random.randrange(1, 999)})

                user_selection = io.print_options(
                    ["Yes", "No"], "Do you want to add a link?")

            new_item["target_price"] = io.input(
                'Please enter target price:', io.VALID_PRICE)
            io.print(
                f"New item created!\n{str(new_item)}", style=IO.COLOR_SUCCESS)
            items.append(new_item)

        elif user_selection == OPTIONS[1]:
            selected_item = io.print_options(
                [str(item) for item in items], "Select an item you want to edit:")
        elif user_selection == OPTIONS[2]:
            selected_item = io.print_options(
                [str(item) for item in items], "Select an item you want to delete:")

except QuitException:
    # This is made to gracefully handle quit at any moment
    io.print(GOODBYE_MESSAGE)
