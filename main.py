import copy

from tkinter import *

state = "Vorlesungen"


def load_input_UI():
    heading.grid(row=1, column=1, columnspan=(days+1))

    for i, label in enumerate(weekday_labels):
        label.grid(row=2, column=(2+i))

    for i in range(days):
        window.columnconfigure((2+i), minsize=110)

    for i, label in enumerate(timeslot_labels):
        label.grid(row=(3+i), column=1)

    for i in range(0, days):
        for j in range(0, slots):
            buttons[(i*slots)+j].grid(row=(3+j), column=(2+i), sticky="WENS")

    continue_button.grid(row=(slots+4), column=(days), sticky="NS", ipadx=20)
    finished_button.grid(row=(slots+4), column=(days+1), sticky="NS", ipadx=20)

    #Spacing
    spacer[0].grid(row=0, column=0, padx=7)
    spacer[1].grid(row=(slots+5), column=(days+2), padx=7)
    spacer[2].grid(row=(slots+3), column=1)


def clear_input_UI():
    heading.destroy()

    for i, label in enumerate(weekday_labels):
        label.destroy()

    for i in range(days):
        window.columnconfigure((2+i), minsize=0)

    for i, label in enumerate(timeslot_labels):
        label.destroy()

    for i in range(0, days):
        for j in range(0, slots):
            buttons[(i*slots)+j].destroy()

    continue_button.destroy()
    finished_button.destroy()

    spacer[0].destroy()
    spacer[1].destroy()
    spacer[2].destroy()

    title_label.destroy()
    title_entry.destroy()


def switch_timeslot(day, slot):
    match state:
        case "Vorlesungen":
            lectures[weekdays[day]][slot] = "Vorlesung" if lectures[weekdays[day]][slot] == "" else ""
        case "Übungen":
            temp[weekdays[day]][slot] = "belegt" if temp[weekdays[day]][slot] == "" else ""
        case _:
            raise Exception("State Error")
    
    buttons[(day*slots)+slot].config(text="frei") if buttons[(day*slots)+slot].cget("text") == "belegt" else buttons[(day*slots)+slot].config(text="belegt")
    buttons[(day*slots)+slot].config(background="white smoke") if buttons[(day*slots)+slot].cget("background") == "pale turquoise" else buttons[(day*slots)+slot].config(background="pale turquoise")


def reset_button_label(day, slot):
    buttons[(day*slots)+slot].config(text="frei")
    buttons[(day*slots)+slot].config(background="white smoke")


def next_state():
    global state
    global temp
    match state:
        case "Vorlesungen":
            for i in range(0, days):
                for j in range(0, slots):  
                    reset_button_label(i, j)  
            state = "Übungen"
            heading.config(text="Klicke alle Zeitslots an, in denen die selbe Veranstaltung (Übungsgruppe, etc.) angeboten wird:")
            title_label.grid(row=(slots+3), column=2, columnspan=(days-2))
            title_entry.grid(row=(slots+4), column=2, columnspan=(days-2))
        case "Übungen":
            if (title_entry.get() != ""):
                tutorials[title_entry.get()] = temp
                temp = {}
                for weekday in weekdays:
                    temp[weekday] = [""] * slots
                title_entry.delete(0, len(title_entry.get()))
            else:
                tutorials[("Uebung " + str(len(tutorials)+1))] = temp
                temp = {}
                for weekday in weekdays:
                    temp[weekday] = [""] * slots
            for i in range(0, days):
                for j in range(0, slots):  
                    reset_button_label(i, j)  
        case _:
            raise Exception("State Error")


def collapse(timetable, open_tutorials):
    if (len(open_tutorials) == 0):
        return timetable
    
    new_open_tutorials = {}
    for name, tutorial in open_tutorials.items():
        new_open_tutorials[name] = tutorial
    del new_open_tutorials[name]

    possible_timetables = []
    for weekday, day in tutorial.items():
        for i, slot in enumerate(day):
            if (slot != ""):
                if (timetable[weekday][i] == ""):
                    new_timetable = copy.deepcopy(timetable)
                    new_timetable[weekday][i] = name
                    output = collapse(new_timetable, new_open_tutorials)
                    if (isinstance(output, dict)):
                        possible_timetables.append(output)
                    else: 
                        possible_timetables += output
    return possible_timetables


def analyse_timetables(timetables):
    num_of_days = 0
    early_slots = 0
    for day in timetables[0].values():
        for i, slot in enumerate(day):
            if (slot != ""):
                if (i == 0):
                    early_slots += 1
                num_of_days += 1
                break
    
    least_days = (num_of_days, timetables[0])
    least_early_slots = (early_slots, timetables[0])
    free_monday = {}
    free_friday = {}

    for timetable in timetables:
        num_of_days = 0
        early_slots = 0
        monday = FALSE
        friday = FALSE
        for name, day in timetable.items():
            for i, slot in enumerate(day):
                if (slot != ""):
                    if (i == 0):
                        early_slots += 1
                    if (name == "Montag"):
                        monday = TRUE
                    if (name == "Freitag"):
                        friday = TRUE
                    num_of_days += 1
                    break
    
        if (num_of_days < least_days[0]):
            least_days = (num_of_days, timetable)
        if (early_slots < least_early_slots[0]):
            least_early_slots = (early_slots, timetable)
        if (not monday):
            free_monday = timetable
        if (not friday):
            free_friday = timetable

    print(least_days)
    print(least_early_slots)
    print(free_monday)
    print(free_friday)


def evaluate():
    next_state()

    # Remove empty tutorials
    empty_tutorials = []
    for name, tutorial in tutorials.items():
        marked = FALSE
        for weekday in tutorial.values():
            for slot in weekday:
                if (slot != ""):
                    marked = TRUE
                    break
            if (marked):
                break
        if (not marked):
            empty_tutorials.append(name)
    for name in empty_tutorials:
        del tutorials[name]

    # The magic happens
    possible_timetables = collapse(lectures, tutorials)
    analyse_timetables(possible_timetables)

    # Change UI
    clear_input_UI()



weekdays = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]
timeslots = ["08:00\n-\n10:00", "10:00\n-\n12:00", "12:00\n-\n14:00", "14:00\n-\n16:00", "16:00\n-\n18:00", "18:00\n-\n20:00"]

slots = len(timeslots)
days = len(weekdays)
lectures = {}
for weekday in weekdays:
    lectures[weekday] = [""] * slots
tutorials = {}
temp = {}
for weekday in weekdays:
    temp[weekday] = [""] * slots
title = ""

window = Tk()
window.title("Stundenplaner")

# Configure the Main Menu
menu_bar = Menu(window)
menu_bar.add_command(label="Speichern")
menu_bar.add_separator()
menu_bar.add_command(label="Laden")
menu_bar.add_separator()
menu_bar.add_command(label="Beenden", command=window.quit)

# Create window objects
spacer = []
for i in range(0, 3):
    spacer.append(Label(window, text=""))
heading = Label(window, text="Klicke alle Zeitslots mit fixen Veranstaltungen (Vorlesungen, etc.) an:")

weekday_labels = []
for i in range(0, days):
    weekday_labels.append(Label(window, text=weekdays[i]))

timeslot_labels = []
for i in range(0, slots):
    timeslot_labels.append(Label(window, text=timeslots[i]))

buttons = [None] * (days * slots)
for i in range(0, days):
    for j in range(0, slots):
        buttons[(i*slots)+j] = Button(window, text="frei", background="white smoke",command=lambda day=i, slot=j: switch_timeslot(day, slot))

continue_button = Button(window, text="Weiter", command=lambda: next_state())
finished_button = Button(window, text="Fertig", command=lambda: evaluate())

title_label = Label(window, text="Gib den Namen der Veranstaltung ein:")
title_entry = Entry(window, textvariable=title)

# Organize window
load_input_UI()

window.config(menu=menu_bar)

window.mainloop()
print(lectures)
print(tutorials)