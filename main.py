from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    """Generates a random password"""
    # Clean up any previous passwords if Generate button is pressed again
    password_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    # password_list = []

    # for char in range(nr_letters):
    #   password_list.append(random.choice(letters))
    password_list = [choice(letters) for _ in range(randint(8, 10))]

    # for char in range(nr_symbols):
    #   password_list += random.choice(symbols)
    password_list.extend([choice(symbols) for _ in range(randint(2, 4))])

    # for char in range(nr_numbers):
    #   password_list += random.choice(numbers)
    password_list.extend([choice(numbers) for _ in range(randint(2, 4))])

    # Alternatively, create 3 lists:
    # password_letters = [choice(letters) for _ in range(randint(8, 10))]
    # password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    # password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    #
    # password_list = password_letters + password_symbols + password_numbers

    shuffle(password_list)

    passwd = "".join(password_list)

    # password = ""
    # for char in password_list:
    #   password += char

    # print(f"Your password is: {password}")
    password_entry.insert(0, passwd)

    # Copy the password to clipboard
    pyperclip.copy(passwd)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    """Saves the provided details to a .json file"""
    web_input = website_entry.get()
    web_input = web_input.lower()
    email_input = email_entry.get()
    pass_input = password_entry.get()

    # creating a new dictionary
    new_data = {
        web_input: {
            "email": email_input,
            "password": pass_input,
        }
    }

    # checking for empty inputs
    if len(web_input) == 0 or len(pass_input) == 0:
        messagebox.showinfo(title="Oops!", message="Please don't leave any fields empty!")
    else:
        is_ok = messagebox.askokcancel(title=web_input, message=f"These are the details entered: \nEmail: {email_input}"
                                       f"\nPassword: {pass_input} \nIs it ok to save?")
        if is_ok:
            # write data to a data.json file when Add is pressed
            # Check if file exists
            try:
                with open("data.json", "r") as data_file:
                    # load the old json data to a 'data' variable as a dictionary
                    data = json.load(data_file)

            # if check above fails, create new file with new_data
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)

            # if check above succeeds,
            else:
                # update the old 'data' variable with new data
                data.update(new_data)
                with open("data.json", "w") as data_file:
                    # save back the updated data to the data_file
                    json.dump(data, data_file, indent=4)

            finally:
                # Clear fields after Save button is pressed
                website_entry.delete(0, END)
                password_entry.delete(0, END)

# ------------------------- FIND PASSWORD ----------------------------- #


def find_password():
    """Searches the generated .json file for saved details"""
    # get the entry to a variable, convert to lowercase
    web_input = website_entry.get()
    web_input = web_input.lower()

    # check if there is a 'data.json' file
    try:
        with open("data.json", "r") as data_file:
            # load the old json data to a 'data' variable as a dictionary
            data = json.load(data_file)

    # if not,
    except FileNotFoundError:
        # message the user that the datafile does not exist
        messagebox.showinfo(title="Error", message="No saved data found.")

    # if file exists,
    else:
        # search through its keys for a match with web_input
        if web_input not in data:
            messagebox.showinfo(title="Error", message=f"No details for  {web_input} exist.")

        else:
            # return result to a window
            mail = data[web_input]["email"]
            passwd = data[web_input]["password"]
            messagebox.showinfo(title=web_input, message=f"These are the details entered: \n"
                                f"Email: {mail}\n"
                                f"Password: {passwd}")

    # only use exception handling when no other alternative exists

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

bgimg = PhotoImage(file="logo.png")
canvas = Canvas(window, width=202, height=202)
canvas.create_image(100, 100, image=bgimg)
canvas.grid(column=1, row=0)

# The 'website' label
website = Label(text="Website:")
website.grid(column=0, row=1)
# The 'email/username' label
email = Label(text="Email/Username: ")
email.grid(column=0, row=2)
# The 'password' label
password = Label(text="Password: ")
password.grid(column=0, row=3)

# The 'website' entry, width 35
website_entry = Entry(width=25)
website_entry.grid(column=1, row=1)
website_entry.focus()
# The 'email/username' entry, width 35
email_entry = Entry(width=35)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(0, "username@email.com")
# The 'password' entry, width 21
password_entry = Entry(width=25)
password_entry.grid(column=1, row=3)


# The 'Generate' button
generate = Button(text="Generate", width=5, command=generate_password)
generate.grid(column=2, row=3)
# The 'save' button, width 36
save_button = Button(text="Save", width=31, command=save)
save_button.grid(column=1, row=4, columnspan=2)
# The 'search' button
search = Button(text="Search", command=find_password)
search.grid(column=2, row=1)

window.mainloop()
