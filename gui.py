import classes
import tkinter as tk


# def create_account():

window = tk.Tk()
window.geometry('300x1080')
window.resizable(False, False)
window.title('RunApp - Create an account')

intVar = tk.IntVar(window, 0)
stringVar = tk.StringVar(window, '')
parameter_dict = {
    'username': tk.StringVar(),
    'password': tk.StringVar(),
    'phone_number': tk.StringVar(),
    'first_name': tk.StringVar(),
    'last_name': tk.StringVar(),
    'isMale': tk.IntVar(),
    'weight_kg': tk.IntVar(),
    'height_cm': tk.IntVar(),
    'age': tk.IntVar()
}
confirm_password_value = tk.StringVar()


username_label = tk.Label(window, text='Create a username:')
username_label.pack(pady=(20, 0))
username = tk.Entry(window, textvariable=parameter_dict['username'])
username.pack()

password_label = tk.Label(window, text='Create a password:')
password_label.pack(pady=(20, 0))
password = tk.Entry(window, textvariable=parameter_dict['password'], show='*')
password.pack()

confirm_password_label = tk.Label(window, text='Confirm password:')
confirm_password_label.pack(pady=(20, 0))
confirm_password = tk.Entry(window, textvariable=confirm_password_value, show='*')
confirm_password.pack()
password_mismatch_error = tk.Label(window, text='Passwords must match', fg='red')
if confirm_password_value.get() != parameter_dict['password'].get():
    password_mismatch_error.pack()


phone_number_label = tk.Label(window, text='Phone number:')
phone_number_label.pack(pady=(20, 0))
phone_number = tk.Entry(window, textvariable=parameter_dict['phone_number'])
phone_number.pack()

first_name_label = tk.Label(window, text='First name:')
first_name_label.pack(pady=(20, 0))
first_name = tk.Entry(window, textvariable=parameter_dict['first_name'])
first_name.pack()

last_name_label = tk.Label(window, text='Last name:')
last_name_label.pack(pady=(20, 0))
last_name = tk.Entry(window, textvariable=parameter_dict['last_name'])
last_name.pack()

isMale_label = tk.Label(window, text='Select your gender:')
isMale_label.pack(pady=(20,0))
values = {"Male": 0,
          "Female": 1,
          "Prefer not to say": 2
          }
for (text, value) in values.items():
    tk.Radiobutton(window, text=text, value=value, variable=parameter_dict['isMale']).pack(pady=(0, 0))

weight_label = tk.Label(window, text='Weight (kg):')
weight_label.pack(pady=(20, 0))
weight = tk.Scale(window, from_=0, to=300, orient='horizontal', length=150, sliderlength=50, variable=parameter_dict['weight_kg'])
weight.pack()


if __name__ == '__main__':
    window.mainloop()
    for key in parameter_dict:
        parameter_dict[key] = parameter_dict[key].get()    # Convert tkinter Vars into basic strings and ints
    print(parameter_dict)
