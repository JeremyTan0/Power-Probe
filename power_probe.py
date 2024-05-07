from assets import ascii
import time
import json

import os


def clear():
    print("\n" * 100)

valid_commands = ['login', 'signup', 'guest', 'about', 'quit', 'l', 's', 'g', 'a', 'q', 'Login', "Signup", "Guest", "About", "Quit"]
login_commands = ['back', 'b', 'Back']

user_input = None

def get_data():
    with open('data/users.json', 'r') as file:
        data = json.load(file)["users"]
    return data

def welcome_commands():
    print(ascii.title)
    print(
        "Welcome to PowerProbe!\nThe ultimate text-based quiz game where users can test their knowledge on fun facts!\n")
    print("COMMANDS:")
    print("Type 'login' or 'l' to log in as an existing user.")
    print("Type 'signup' or 's' to sign up as a new user.")
    print("Type 'guest' or 'g' to play as a guest (Your score will not be saved!).")
    print("Type 'about' or 'a' to learn more about the application.")
    print("Type 'quit' or 'q' to leave.\n")
    print("Input a command and hit the Enter key!")

    user_input = input("[login, signup, guest, about, quit]: ").lower()

    while user_input not in valid_commands:
        print("\nInvalid input, please try again.")
        user_input = input("[login, signup, guest, about]: ")

    print('\n')
    if user_input == "login" or user_input == "l":
        clear()
        login()
    elif user_input == "signup" or user_input == "s":
        clear()
        sign_up()
    elif user_input == "guest" or user_input == "g":
        guest_confirm = input("You are about to play as a guest user. Progress and scores will NOT be saved. Are you sure (Y/N)? ").lower()
        while guest_confirm not in ['yes', 'y', 'no', 'n']:
            print("Invalid input. Enter either (Y/N): ")
            guest_confirm = input(
                "You are about to play as a guest user. Progress and scores will NOT be saved. Are you sure (Y/N)?").lower()
        if guest_confirm == 'yes' or guest_confirm == 'y':
            clear()
            game_home_guest(current_user={
                "username": "Guest",
                "password": "NULL",
                "high_score": "NULL"
            })
        else:
            clear()
            welcome_commands()
    elif user_input == "about" or user_input == "a":
        clear()
        about()
    elif user_input == "quit" or user_input == "q":
        confirm = input("You are about to quit the program. Are you sure (Y/N)? ").lower()
        while confirm not in ["n", "no", "yes", "y"]:
            print("Invalid input.")
            confirm = input("You are about to quit the program. Are you sure (Y/N)? ")
        if confirm == "n" or confirm == "no":
            welcome_commands()

def login():
    current_user = None
    print(ascii.login)
    print("Please enter your user credentials.\n")
    print("COMMANDS:")
    print("Type 'back' or 'b' at anytime to return to the welcome page.")

    credential = input("Enter your username: ")

    users = get_data()

    if credential not in login_commands:
        password = input("Enter your password: ")
        if password not in login_commands:
            print("Validating user. Please wait....")
            validated = False
            for user in users:
                if credential == user["username"]:
                    if password == user["password"]:
                        validated = True
                        current_user = user
            print("\n")
            if validated is False:
                print("Invalid username or password. Please try again.\n")
                login()
            else:
                print("User validated!")

                login_confirm = input(f"You are about to log in as {credential}. Proceed (Y/N)? ").lower()
                confirm_commands = ['y', 'n', 'back', 'b', 'yes', 'no']
                while login_confirm not in confirm_commands:
                    print("\nInvalid command entered!")
                    login_confirm = input(f"You are about to log in as {credential}. Proceed (Y/N)? ")
                if login_confirm == 'y' or login_confirm == 'yes':
                    clear()
                    game_home_user(current_user)
                else:
                    clear()
                    welcome_commands()
        else:
            clear()
            welcome_commands()
    elif credential == 'b' or credential == 'back' or credential == 'Back' or credential == 'B':
        clear()
        welcome_commands()
    else:
        print("Username not found")

def sign_up():
    print(ascii.sign_up)
    print("Create a new user! By signing up, your score will be tracked and placed on a leaderboard!\n")
    print("COMMANDS:")
    print("Type 'back' or 'b' at anytime to return to the welcome page.")

    valid_credential = False
    credential = input("Enter your chosen username (Minimum of 3 characters): ")
    users = get_data()
    existing_usernames = []
    for user in users:
        existing_usernames.append(user["username"])

    while not valid_credential:
        if credential in login_commands:
            clear()
            welcome_commands()

        if credential not in existing_usernames and credential not in valid_commands:
            valid_credential = True
        elif credential in existing_usernames:
            print("\nUsername invalid. It already exists.")
            credential = input("Enter your chosen username (Minimum of 3 characters): ")
        elif len(credential) < 3:
            print("\nUsername invalid. It is less than 3 characters.")
            credential = input("Enter your chosen username (Minimum of 3 characters): ")

    if valid_credential:
        password = input("Enter a password (Minimum of 3 characters): ")
        confirm_password = input("Confirm password (Minimum of 3 characters): ")
        while password != confirm_password or len(password) < 3:
            if password != confirm_password:
                print("Passwords do not match\n")
            else:
                print("Password is less than 3 characters\n")
            password = input("Enter a password (Minimum of 3 characters): ")
            confirm_password = input("Confirm password (Minimum of 3 characters): ")

        user_confirmation = input(f"Confirm that these details are correct?\nUsername: {credential}\nPassword: {password}\n\nType (Y/N) to confirm or not: ").lower()
        confirm_commands = ['y', 'n', 'back', 'b', 'yes', 'no']
        while user_confirmation not in confirm_commands:
            print("\nInvalid command entered!")
            user_confirmation = input("Type (Y/N) to confirm or not: ")

        if user_confirmation == "y" or user_input == 'yes':
            new_user = {
                "username": credential,
                "password": password
            }
            users.append(new_user)
            with open("data/users.json", "w") as file:
                json.dump({'users': users}, file)
            clear()
            game_home_user(new_user)
        elif user_confirmation == "n" or user_confirmation == 'no':
            clear()
            sign_up()
        else:
            clear()
            welcome_commands()

def about():
    print(ascii.about)
    print("Hello there!\n PowerProbe is a text-based, multiple-choice quiz game. Questions come from a wide range of categories, specifically:\n"
          "1. Music\n2. Sports and Leisure\n3. Film and TV\n4. Arts and Literature\n5. History\n6. Society and Culture\n7. Science\n8. Geography\n9. Food and Drink\n10. General Knowledge\n\n"
          "Each question will have 4 options, and users will be prompted to choose one out of the four.\nUsers will be asked questions until they get an incorrect answer, and correct answers will get added to their score for each attempt.\n"
          "Essentially, high scores mean more questions answered consecutively!\nFor players who have registered or have logged in to an account, their highest score will be kept and potentially displayed on the leaderboard if the score is in the top 10 among all player scores.\n"
          "Users may also opt to play as 'Guest' users, however, scores are not tracked and remembered.\n")
    u_input = input("To return to home, enter any key: ")
    if u_input:
        clear()
        welcome_commands()

def game_home_user(current_user):
    print(ascii.home)
    if current_user['username'] != 'Guest':
        print(f"Logged in as {current_user['username']}")
    else:
        print("Logged in as guest user. Scores and progress will not be saved!")

    home_commands = ['start', 's', 'lb', 'l', 'help', 'h', 'settings', 'st', 'quit', 'q']
    print("COMMANDS:")
    # print("Type 'start' or 's' to get a new question to answer.")
    # print("Type 'lb' or 'l' to get the leaderboard.")
    # print("Type 'help' or 'h' to get the game instructions.")
    # print("Type 'settings' or 'st' to access the settings page.")
    print("Type 'quit' or 'q' to log out and return to home.")

    user_input = input("[start, lb, help, settings, quit]: ").lower()
    while user_input not in valid_commands:
        print("\nInvalid input, please try again.")
        user_input = input("[quit]: ")
    if user_input == 'quit' or user_input == 'q':
        clear()
        welcome_commands()


def game_home_guest(current_user):
    print(ascii.home)
    if current_user['username'] != 'Guest':
        print(f"Logged in as {current_user['username']}")
    else:
        print("Logged in as guest user. Scores and progress will not be saved!")

    home_commands = ['start', 's', 'lb', 'l', 'help', 'h', 'quit', 'q']
    print("COMMANDS:")
    # print("Type 'start' or 's' to get a new question to answer.")
    # print("Type 'lb' or 'l' to get the leaderboard.")
    # print("Type 'help' or 'h' to get the game instructions.")
    print("Type 'quit' or 'q' to log out and return to home.")

    user_input = input("[start, lb, help, quit]: ").lower()
    while user_input not in valid_commands:
        print("\nInvalid input, please try again.")
        user_input = input("[quit]: ")
    if user_input == 'quit' or user_input == 'q':
        clear()
        welcome_commands()

welcome_commands()



