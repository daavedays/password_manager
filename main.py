from tkinter import *
from tkinter import messagebox
from random import randint, shuffle, choice
import json

FONT = ("Ariel", 15)
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def password_generator():
    """Function to generate passwords. Uses the alphabet, symbols and numbers and picks random characheters."""
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
               'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F',
               'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    letters_list = [choice(letters) for _ in range(randint(8, 10))]
    numbers_list = [choice(numbers) for _ in range(randint(2, 4))]
    symbols_list = [choice(symbols) for _ in range(randint(2, 4))]

    password_list = letters_list + numbers_list + symbols_list
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(END, string=f"{password}")
    return password


# ---------------------------- SAVE PASSWORD ------------------------------- #

def saved_passwords():
    try:
        with open("usernames_and_passwords.json") as file:
            data_file = json.load(file)
    except FileNotFoundError:
        messagebox.showerror("Error", "Nothing Saved Yet")
    else:
        saved = 0
        for key, value in data_file.items():
            saved += 1
            username = value["username"]
            password = value["password"]
            messagebox.showinfo("Saved", f"{saved}\n{key}\n{username}\n{password}")


def add():
    """Adds the txt file to the same file path that is being worked on."""

    website = website_entry.get().lower()
    username = email_username_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "username": username,
            "password": password
        }
    }

    # is_ok = messagebox.askokcancel("Conformation", f"Do you want to save the following information.\n\n"
    #                                                f" website: {website_entry.get()}\n"
    #                                                f"email:{email_username_entry.get()}\n"
    #                                                f"password:{password_entry.get()}")  # Messagebox returns a boolean

    if len(website_entry.get()) == 0 or len(password_entry.get()) == 0:
        messagebox.showerror("Missing Information", "Please fill out all the fields.")
    else:
        try:  # Protects against file not being found.
            with open("usernames_and_passwords.json", "r") as data_file:
                data = json.load(data_file)  # Opens the files content and converts into a python readable code.

        except FileNotFoundError:  # Generate a new file and save it.
            with open("usernames_and_passwords.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)

        else:  # If file found and no error, we save the new information.
            data.update(new_data)
            with open("usernames_and_passwords.json", "w") as data_file:
                json.dump(data, data_file, indent=4)

        finally:  # No matter what we clear the users inputs from the entries.
            password_entry.delete(0, END)  # Deletes the text inside the entry
            website_entry.delete(0, END)  # ''       ''         ''         ''

# --------------------------- SEARCH BUTTON ------------------------- #


def search():
    website = website_entry.get().lower()  # Get the entry to be used as the key to get specific website.
    try:
        with open("usernames_and_passwords.json") as file:
            data = json.load(file)  # Convert the file into a python friendly dictionary.
    except FileNotFoundError:
        messagebox.showerror("No Website Found", "No website found.")
    else:
        if website in data:  # using the searched website as main key to iterate over the keys in data file.
            username = data[website]["username"]  # nested dictionary, using the website as main key.
            password = data[website]["password"]
            messagebox.showinfo(f"{website}", f"Website: {website}\n\nUsername: {username}\n\nPassword: {password}")
        else:
            messagebox.showerror(f"{website}", "Not Found")

# --------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=30)

# TODO create the logo using the canvas.
canvas = Canvas(width=200, height=200)
logo_png = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_png)
canvas.grid(column=1, row=0)

# ---------TODO create the website, email, password texts.
website_label = Label(text="Website:", font=FONT)
website_label.grid(column=0, row=1)
email_username_label = Label(text="Email/Username:", font=FONT)
email_username_label.grid(column=0, row=2)
password_label = Label(text="Password:", fg="red", font=FONT)
password_label.grid(column=0, row=3)

# ---------TODO create the buttons: 1) Generate Password 2)Add.
generate_password_btn = Button(text="Generate Password", command=password_generator, fg="red")
generate_password_btn.grid(column=2, row=3)
add_btn = Button(text="            add            ", command=add, fg="blue")
add_btn.grid(column=1, row=4)
search_btn = Button(text="          Search          ", command=search, fg="green")
search_btn.grid(column=2, row=1)
all_passwords_btn = Button(text=" Saved Passwords ", command=saved_passwords, fg="purple")
all_passwords_btn.grid(column=2, row=2)

# ---------TODO create entries for the website, for the email, and password.
website_entry = Entry(width=23)
website_entry.focus()  # Makes the curser automatically be located in the website entry.
website_entry.grid(column=1, row=1)

email_username_entry = Entry(width=23)
email_username_entry.insert(0, string="davemirzoyan@gmail.com")
email_username_entry.grid(column=1, row=2, columnspan=1)

password_entry = Entry(width=23)
password_entry.grid(column=1, row=3)


window.mainloop()
