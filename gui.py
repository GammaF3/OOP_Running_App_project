import classes as ra
import tkinter as tk
from tkinter import ttk


def destroy_popup_and_master(popup_window: tk.Tk, master_window: tk.Tk):    # destroys both the initial window user is trying to X out (master) and the popup
    popup_window.destroy()
    master_window.destroy()


def confirm_close_win_manager(title, text, window: tk.Tk):    # confirms closing windows after user tries to 'X out', then continues code
    root = tk.Tk()
    root.geometry('300x200')
    root.eval('tk::PlaceWindow . center')
    root.resizable(False, False)
    root.title(title)

    warning = tk.Label(root, text=text, justify='center')
    warning.pack(side='top', pady=(30, 10))

    choices = tk.Canvas(root)
    choices.pack(side='bottom', pady=(20, 10))
    yes = tk.Button(choices, text='Yes', justify='center', width=8, command=lambda: destroy_popup_and_master(root, window))
    yes.grid(row=0, column=0)
    cancel = tk.Button(choices, text='Cancel', justify='center', width=8, command=root.destroy)
    cancel.grid(row=0, column=1)

    root.protocol('WM_DELETE_WINDOW', root.destroy)
    root.mainloop()


def error_window(title, text):
    root = tk.Tk()
    root.geometry('300x200')
    root.eval('tk::PlaceWindow . center')
    root.resizable(False, False)
    root.title(title)

    error = tk.Label(root, text=text, justify='center')
    error.pack(side='top', pady=(30, 10))

    cancel = tk.Button(root, text='OK', justify='center', width=4, command=root.destroy)
    cancel.pack()

    root.protocol('WM_DELETE_WINDOW', root.destroy)
    root.mainloop()


def expected_close_for_forms(window: tk.Tk, params: dict, flag: list):    # closes windows that have fields that must be filled
    None_values_found = False
    for key in params:
        if params[key].get() == '':
            None_values_found = True
            break
    if None_values_found:
        root = tk.Tk()
        root.geometry('300x200')
        root.eval('tk::PlaceWindow . center')
        root.resizable(False, False)
        root.title('Empty fields found')
        warning = tk.Label(root,
                           text='Please fill out every field.',
                           justify='center', )
        warning.pack(side='top', pady=(30, 10))

        choices = tk.Canvas(root)
        choices.pack(side='bottom', pady=(20, 10))

        cancel = tk.Button(choices, text='Ok', justify='center', width=8, command=root.destroy)
        cancel.grid(row=0, column=1)

        root.protocol('WM_DELETE_WINDOW', root.destroy)

        root.mainloop()
    else:
        window.destroy()
        flag[0] = True


def create_account():
    window = tk.Tk()
    window.geometry('400x500')
    window.eval('tk::PlaceWindow . center')
    window.resizable(False, False)
    window.title('RunApp - Create an account')

    window_frame = tk.Frame(window)
    window_frame.pack(fill='both', expand=1)

    window_canvas = tk.Canvas(window_frame)
    window_canvas.pack(side='left', fill='both', expand=1)

    scrollbar = ttk.Scrollbar(window_frame, orient='vertical', command=window_canvas.yview)
    scrollbar.pack(expand=False, side='right', fill='y')

    window_canvas.configure(yscrollcommand=scrollbar.set)
    window_canvas.bind('<Configure>', lambda e: window_canvas.configure(scrollregion=window_canvas.bbox('all')))

    frame_within_scrollbar = tk.Frame(window_canvas)

    window_canvas.create_window((0, 0), window=frame_within_scrollbar, anchor='nw')

    canvas_for_entries = tk.Canvas(frame_within_scrollbar)
    canvas_for_entries.pack(side='top')

    parameter_dict = {
        'username': tk.StringVar(),
        'password': tk.StringVar(),
        'phone_number': tk.StringVar(),
        'first_name': tk.StringVar(),
        'last_name': tk.StringVar(),
        'isMale': tk.IntVar(),
        'weight_kg': tk.IntVar(),
        'height_cm': tk.IntVar(),
        'age': tk.IntVar(),
        'confirm_password': tk.StringVar()
    }
    save_data = [False]    # if False, don't return anything. If True, return Account object. List for mutability.

    username_label = tk.Label(canvas_for_entries, text='Create a username:')
    username_label.grid(row=0, column=0, sticky='w', padx=(5, 10), pady=(20, 0))
    username = tk.Entry(canvas_for_entries, textvariable=parameter_dict['username'])
    username.grid(row=0, column=1, sticky='w', pady=(20, 0))

    password_label = tk.Label(canvas_for_entries, text='Create a password:')
    password_label.grid(row=1, column=0, sticky='w', padx=(5, 10), pady=(20, 0))
    password = tk.Entry(canvas_for_entries, textvariable=parameter_dict['password'], show='*')
    password.grid(row=1, column=1, sticky='w', pady=(20, 0))

    confirm_password_label = tk.Label(canvas_for_entries, text='Confirm password:')
    confirm_password_label.grid(row=2, column=0, sticky='w', padx=(5, 10), pady=(20, 0))
    confirm_password = tk.Entry(canvas_for_entries, textvariable=parameter_dict['confirm_password'], show='*')
    confirm_password.grid(row=2, column=1, sticky='w', pady=(20, 0))

    phone_number_label = tk.Label(canvas_for_entries, text='Phone number:')
    phone_number_label.grid(row=4, column=0, sticky='w', padx=(5, 10), pady=(20, 0))
    phone_number = tk.Entry(canvas_for_entries, textvariable=parameter_dict['phone_number'])
    phone_number.grid(row=4, column=1, sticky='w', pady=(20, 0))

    first_name_label = tk.Label(canvas_for_entries, text='First name:')
    first_name_label.grid(row=5, column=0, sticky='w', padx=(5, 10), pady=(20, 0))
    first_name = tk.Entry(canvas_for_entries, textvariable=parameter_dict['first_name'])
    first_name.grid(row=5, column=1, sticky='w', pady=(20, 0))

    last_name_label = tk.Label(canvas_for_entries, text='Last name:')
    last_name_label.grid(row=6, column=0, sticky='w', padx=(5, 10), pady=(20, 0))
    last_name = tk.Entry(canvas_for_entries, textvariable=parameter_dict['last_name'])
    last_name.grid(row=6, column=1, sticky='w', pady=(20, 0))

    isMale_label = tk.Label(frame_within_scrollbar, text='Select your gender:')
    isMale_label.pack(pady=(20, 0))
    values = {"Male": 0,
              "Female": 1,
              "Prefer not to say": 2
              }
    for (text, value) in values.items():
        tk.Radiobutton(frame_within_scrollbar, text=text, value=value, variable=parameter_dict['isMale']).pack(pady=(0, 0))

    weight_kg_label = tk.Label(frame_within_scrollbar, text='Weight (kg):')
    weight_kg_label.pack(pady=(20, 0))
    weight_kg = tk.Scale(frame_within_scrollbar, from_=1, to=225, orient='horizontal', length=150, sliderlength=50, variable=parameter_dict['weight_kg'])
    weight_kg.pack()

    height_cm_label = tk.Label(frame_within_scrollbar, text='Height (cm):')
    height_cm_label.pack(pady=(20, 0))
    height_cm = tk.Scale(frame_within_scrollbar, from_=100, to=300, orient='horizontal', length=150, sliderlength=50, variable=parameter_dict['height_cm'])
    height_cm.pack()

    age_label = tk.Label(frame_within_scrollbar, text='Age:')
    age_label.pack(pady=(20, 0))
    age = tk.Scale(frame_within_scrollbar, from_=1, to=100, orient='horizontal', length=150, sliderlength=50, variable=parameter_dict['age'])
    age.pack(pady=(20, 0))

    submit = tk.Button(frame_within_scrollbar, text='Submit', width=8, justify='center', command=lambda: expected_close_for_forms(window, parameter_dict, save_data))
    submit.pack(pady=(0, 20))

    window.protocol('WM_DELETE_WINDOW', lambda: confirm_close_win_manager(title='Info not saved', text='Warning: closing window will not\nsave information. Are you\nsure you want to quit?', window=window))
    window.mainloop()

    if save_data[0]:
        if parameter_dict['password'].get() != parameter_dict['confirm_password'].get():

            '''
        elif found_in_file(parameter_dict['username']):
            error_window('Username Taken', 'Username already taken. Please use a different username.')
            '''
        else:
            for key in parameter_dict:
                parameter_dict[key] = parameter_dict[key].get()    # Convert tkinter Vars into basic strings and ints and isMale to bool
            if parameter_dict['isMale'] == 1:
                parameter_dict['isMale'] = True
            else:
                parameter_dict['isMale'] = False
            to_return = ra.Account(username=parameter_dict['username'], password=parameter_dict['password'], all_runs=[],
                                   phone_number=parameter_dict['phone_number'], first_name=parameter_dict['first_name'],
                                   last_name=parameter_dict['last_name'], isMale=parameter_dict['isMale'], weight_kg=parameter_dict['weight_kg'],
                                   height_cm=parameter_dict['height_cm'], age=parameter_dict['age'])
            return to_return


def window_view_runs(account: ra.Account):
    all_runs: list[ra.Run] = account.get_all_runs()[::-1]  # reversed for most recent first, because new runs are appended

    root = tk.Tk()
    root.geometry('400x500')
    root.eval('tk::PlaceWindow . center')
    root.resizable(False, False)
    root.title('All Runs')

    window_frame = tk.Frame(root)
    window_frame.pack(fill='both', expand=1)

    window_canvas = tk.Canvas(window_frame)
    window_canvas.pack(side='left', fill='both', expand=1)

    scrollbar = ttk.Scrollbar(window_frame, orient='vertical', command=window_canvas.yview)
    scrollbar.pack(expand=False, side='right', fill='y')

    window_canvas.configure(yscrollcommand=scrollbar.set)
    window_canvas.bind('<Configure>', lambda e: window_canvas.configure(scrollregion=window_canvas.bbox('all')))

    frame_within_scrollbar = tk.Frame(window_canvas)
    window_canvas.create_window((0, 0), window=frame_within_scrollbar, anchor='nw')

    for run in all_runs:
        info = (f'Run on {run.get_date_time()}:\n'
                f'Distance: {run.get_distance_mi()} mi\n'
                f'Time: {run.str_time_elapsed()}\n'
                f'Calories burned: {int(account.calculate_calories_burned(run))}')
        tk.Label(frame_within_scrollbar, height=4, text=info).pack()


def window_view_stats(account: ra.Account):
    time_heading_text = f'Total time spent running:'
    unit_time_text = account.str_total_time_running_sec().split(', ')
    distance_text = f'Total distance ran: {account.get_total_dist_mi():,} mi'
    calories_text = f'Total calories burned: {int(account.get_total_calories_burned()):,}'
    total_runs_text = f'Runs completed: {account.get_runs_completed()}'
    goals_text = f'Goals completed: {account.get_goals_completed():,}'
    time_goals_text = f'Time goals completed: {account.get_time_goals_completed():,}'
    dist_goals_text = f'Distance goals completed:{account.get_distance_goals_completed():,}'
    cal_goals_text = f'Calorie goals completed: {account.get_calorie_goals_completed():,}'

    root = tk.Tk()
    root.geometry('400x500')
    root.eval('tk::PlaceWindow . center')
    root.resizable(False, False)
    root.title('Statistics')

    root_canvas = tk.Canvas(root)
    root_canvas.pack(fill='both')

    tk.Label(root_canvas, text='Stats', justify='left', font='bold', anchor='w').pack(pady=20, padx=(10, 0))

    tk.Label(root_canvas, text=time_heading_text, justify='left', anchor='w').pack(pady=(0, 10), padx=(10, 0))

    for text in unit_time_text:
        tk.Label(root_canvas, text=text, justify='left', anchor='w').pack(pady=(0, 10), padx=(20, 0))

    tk.Label(root_canvas, text=distance_text, justify='left', anchor='w').pack(pady=(10, 10), padx=(10, 0))
    tk.Label(root_canvas, text=calories_text, justify='left', anchor='w').pack(pady=(0, 10), padx=(10, 0))
    tk.Label(root_canvas, text=total_runs_text, justify='left', anchor='w').pack(pady=(0, 10), padx=(10, 0))

    tk.Label(root_canvas, text=goals_text, justify='left', anchor='w').pack(pady=(0, 10), padx=(10, 0))

    tk.Label(root_canvas, text=time_goals_text, justify='left', anchor='w').pack(pady=(0, 10), padx=(20, 0))
    tk.Label(root_canvas, text=dist_goals_text, justify='left', anchor='w').pack(pady=(0, 10), padx=(20, 0))
    tk.Label(root_canvas, text=cal_goals_text, justify='left', anchor='w').pack(pady=(0, 10), padx=(20, 0))


def main_menu(account: ra.Account):
    root = tk.Tk()
    root.geometry('960x720')
    root.eval('tk::PlaceWindow . center')
    root.resizable(False, False)
    root.title('RunApp')

    top_bar = tk.Canvas(root, height=100)
    top_bar.pack()
    welcome_text = tk.Label(top_bar, text=f'Welcome, {account.get_first_name()} {account.get_last_name()}!', font='verdana 24 bold italic')
    welcome_text.pack(side='left', anchor='sw', padx=20, pady=20)

    main_grid = tk.Canvas(root)
    main_grid.pack(expand=True)

    button_view_runs = tk.Button(main_grid, text='View Previous Runs', width=20, height=5, font='arial 32 bold', command=lambda: window_view_runs(account))
    button_view_runs.grid(row=0, column=0)

    button_view_stats = tk.Button(main_grid, text='View Stats', height=5, font='arial 32 bold', command=lambda: window_view_stats(account))
    button_view_stats.grid(row=0, column=1)

#    button_view_goals = tk.Button(main_grid, text='View Goals', command=lambda: window_view_goals(account))
#    button_view_goals.grid(row=1, column=0)

#    button_account_settings = tk.Button(main_grid, text='Account', command=lambda: window_view_account(account))
#    button_account_settings.grid(row=1, column=1)
    
    root.mainloop()


if __name__ == '__main__':
    test_runs = [ra.Run(), ra.Run(), ra.Run(), ra.Run(), ra.Run(), ra.Run(), ra.Run(), ra.Run(), ra.Run()]
    test_account = ra.Account(all_runs=list(test_runs))
    main_menu(test_account)
    print('code continues')
