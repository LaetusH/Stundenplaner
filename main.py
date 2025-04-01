import copy

from tkinter import *
from tkinter import ttk
from tkinter import messagebox

state = "Vorlesungen"


def load_input_UI():
    heading.grid(row=1, column=1, columnspan=(days+1))
    heading.config(text="Klicke alle Zeitslots mit fixen Veranstaltungen (Vorlesungen, etc.) an:")

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

    # Spacing
    spacer[0].grid(row=0, column=0, padx=7)
    spacer[1].grid(row=(slots+5), column=(days+2), padx=7)
    spacer[2].grid(row=(slots+3), column=1)


def clear_input_UI():
    heading.grid_forget()

    for i, label in enumerate(weekday_labels):
        label.grid_forget()

    for i in range(days):
        window.columnconfigure((2+i), minsize=0)

    for i, label in enumerate(timeslot_labels):
        label.grid_forget()

    for i in range(0, days):
        for j in range(0, slots):
            buttons[(i*slots)+j].grid_forget()

    continue_button.grid_forget()
    finished_button.grid_forget()

    spacer[0].grid_forget()
    spacer[1].grid_forget()
    spacer[2].grid_forget()

    title_label.grid_forget()
    title_entry.grid_forget()


def load_timetable(boxes, rectangels, texts, timetables, direction=""):
    global currentTimetable
    match direction:
        case "previous":
            currentTimetable = (currentTimetable - 1 + len(timetables)) % len(timetables)
        case "next":
            currentTimetable = (currentTimetable + 1) % len(timetables)

    timetable = timetables[currentTimetable]
    for i, day in enumerate(timetable.values()):
        for j, slot in enumerate(day):
            if (slot == ""):
                boxes[(i*slots)+j].itemconfig(rectangels[(i*slots)+j], fill="snow")
                boxes[(i*slots)+j].itemconfig(texts[(i*slots)+j], text="")
            else:
                boxes[(i*slots)+j].itemconfig(rectangels[(i*slots)+j], fill="pale turquoise")
                boxes[(i*slots)+j].itemconfig(texts[(i*slots)+j], text=slot)


def load_timetable_UI(title, timetables):
    global currentTimetable
    currentTimetable = 0
    window1 = Toplevel()
    window1.title(title)

    # Create window elements
    spacer1 = []
    for i in range(0, 3):
        spacer1.append(Label(window1, text=""))

    heading1 = Label(window1, text="Klicke alle Zeitslots mit fixen Veranstaltungen (Vorlesungen, etc.) an:")

    weekday_labels1 = []
    for i in range(0, days):
        weekday_labels1.append(Label(window1, text=weekdays[i]))

    timeslot_labels1 = []
    for i in range(0, slots):
        timeslot_labels1.append(Label(window1, text=timeslots[i]))

    boxes = [None] * (days * slots)
    rectangles = [None] * (days * slots)
    texts = [None] * (days * slots)
    for i in range(0, days):
        for j in range(0, slots):
            boxes[(i*slots)+j] = Canvas(window1, width=106, height=45)
            rectangles[(i*slots)+j] = boxes[(i*slots)+j].create_rectangle(0, 0, 106, 45, fill="snow", outline="black")
            texts[(i*slots)+j] = boxes[(i*slots)+j].create_text(106/2, 45/2, text="", width=104)

    previous_button = Button(window1, text="Vorheriger", command=lambda: load_timetable(boxes, rectangles, texts, timetables, "previous"))
    next_button = Button(window1, text="Nächster", command=lambda: load_timetable(boxes, rectangles, texts, timetables, "next"))

    # Organise the window
    spacer1[0].grid(row=0, column=0, padx=7)
    spacer1[1].grid(row=(slots+5), column=(days+2), padx=7)
    spacer1[2].grid(row=(slots+3), column=1)

    heading1.grid(row=1, column=1, columnspan=(days+1))

    for i, label in enumerate(weekday_labels1):
        label.grid(row=2, column=(2+i))

    for i, label in enumerate(timeslot_labels1):
        label.grid(row=(3+i), column=1)

    for i in range(0, days):
        for j in range(0, slots):
            boxes[(i*slots)+j].grid(row=(3+j), column=(2+i))

    previous_button.grid(row=(slots+4), column=2, sticky="NS", ipadx=15)
    next_button.grid(row=(slots+4), column=(days+1), sticky="NS", ipadx=15)

    load_timetable(boxes, rectangles, texts, timetables)

    window1.mainloop()


def switch_timeslot(day, slot):
    match state:
        case "Vorlesungen":
            lectures[weekdays[day]][slot] = "Vorlesung" if lectures[weekdays[day]][slot] == "" else ""
        case "Übungen":
            temp[weekdays[day]][slot] = "belegt" if temp[weekdays[day]][slot] == "" else ""
        case _:
            raise Exception("State Error")
    
    buttons[(day*slots)+slot].config(text="frei") if buttons[(day*slots)+slot].cget("text") == "belegt" else buttons[(day*slots)+slot].config(text="belegt")
    buttons[(day*slots)+slot].config(background="snow") if buttons[(day*slots)+slot].cget("background") == "pale turquoise" else buttons[(day*slots)+slot].config(background="pale turquoise")


def reset_button_label(day, slot):
    buttons[(day*slots)+slot].config(text="frei")
    buttons[(day*slots)+slot].config(background="snow")


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
                tutorials[("Übung " + str(len(tutorials)+1))] = temp
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


def get_results(timetables):
    if (len(timetables) == 0):
        return []
    criteria["earliest_slot"] = earliest_slot.current()
    criteria["latest_slot"] = latest_slot.current()

    least_days = 5
    least_first_slots = 5

    if (criteria["least_days"].get() or criteria["least_first_slots"].get()):
        num_of_days = 0
        first_slots = 0
        for day in timetables[0].values():
            for i, slot in enumerate(day):
                if (slot != ""):
                    if (i == 0):
                        first_slots += 1
                    num_of_days += 1
                    break
        
        least_days = num_of_days
        least_first_slots = first_slots

        for timetable in timetables:
            num_of_days = 0
            first_slots = 0
            for day in timetable.values():
                for i, slot in enumerate(day):
                    if (slot != ""):
                        if (i == 0):
                            first_slots += 1
                        num_of_days += 1
                        break
        
            if (num_of_days < least_days):
                least_days = num_of_days
            if (first_slots < least_first_slots):
                least_first_slots = first_slots

    results = []
    for timetable in timetables:
        num_of_days = 0
        first_slots = 0
        earliest_slot_fullfilled = TRUE
        latest_slot_fullfilled = TRUE
        monday = FALSE
        friday = FALSE
        for name, day in timetable.items():
            day_marked = FALSE
            for i, slot in enumerate(day):
                if (slot != ""):
                    if (i == 0):
                        first_slots += 1
                    if (name == "Montag"):
                        monday = TRUE
                    if (name == "Freitag"):
                        friday = TRUE
                    if ((i < criteria["earliest_slot"]) and (slot != "Vorlesung")):
                        earliest_slot_fullfilled = FALSE
                    if ((i > criteria["latest_slot"]) and (slot != "Vorlesung")):
                        latest_slot_fullfilled = FALSE    
                    day_marked = TRUE        
            if (day_marked):
                num_of_days += 1


        if ((not criteria["least_days"].get()) or (num_of_days <= least_days)):
            if ((not criteria["least_first_slots"].get()) or (first_slots <= least_first_slots)):
                if ((not criteria["free_monday"].get()) or (not monday)):
                    if ((not criteria["free_friday"].get()) or (not friday)):
                        if (earliest_slot_fullfilled):
                            if (latest_slot_fullfilled):
                                results.append(timetable)
    return results


def update_results():
    global possible_timetables
    num_of_results = len(get_results(possible_timetables))
    show_results_button.config(text=f"{num_of_results} Ergebnisse anzeigen")
    if (num_of_results == 0):
        show_results_button.config(state="disabled")
    else:
        show_results_button.config(state="normal")


def load_search_UI():
    menu_bar.add_separator()
    menu_bar.add_command(label="Speichern", command=lambda: save_file())

    num_of_criteria = len(checkboxes) + 2
    heading.grid(row=1, column=1, columnspan=2)
    heading.config(text="Wähle die Suchkriterien aus und lasse dir die Ergebnisse anzeigen")
    
    checkboxes["least_days"].grid(row=2, column=1, sticky="W")
    checkboxes["free_monday"].grid(row=3, column=1, sticky="W")
    checkboxes["free_friday"].grid(row=4, column=1, sticky="W")
    checkboxes["least_first_slots"].grid(row=5, column=1, sticky="W")
    earliest_slot.grid(row=(len(checkboxes)+2), column=2, sticky="W")
    latest_slot.grid(row=(len(checkboxes)+3), column=2, sticky="W")

    earliest_slot_label.grid(row=(len(checkboxes)+2), column=1, sticky="W")
    latest_slot_label.grid(row=(len(checkboxes)+3), column=1, sticky="W")

    show_results_button.grid(row=(num_of_criteria+3), column=1, columnspan=2, sticky="NS", ipadx=20)
    show_results_button.config(state="disabled")

    # Spacing
    spacer[0].grid(row=0, column=0, padx=7)
    spacer[1].grid(row=(num_of_criteria+4), column=7, padx=7)
    spacer[2].grid(row=(num_of_criteria+2), column=1)

    update_results()


def evaluate():
    global possible_timetables
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

    # Searches for all possible timetables
    if (len(tutorials) > 0):
        possible_timetables = collapse(lectures, tutorials)
    else:
        possible_timetables = [lectures]

    # Change UI
    clear_input_UI()
    load_search_UI()


def save_file():
    output = ""
    for day in lectures.values():
        for slot in day:
            output += slot + ",,"
        output += ";;"
    output += "::\n"
    for name, tutorial in tutorials.items():
        name = name.replace("Ä", "&$AE")
        name = name.replace("Ö", "&$OE")
        name = name.replace("Ü", "&$UE")
        name = name.replace("ä", "&$ae")
        name = name.replace("ö", "&$oe")
        name = name.replace("ü", "&$ue")
        output += name + ";;"
        for day in tutorial.values():
            for slot in day:
                output += slot + ",,"
            output += ";;"
        output += "::\n"
    with open("stundenplan.txt", "w+") as file:
        file.write(output)
    messagebox.showinfo("Hinweis", "Erfolgreich gespeichert.", icon="info")


def load_file():
    global lectures
    global tutorials
    
    try:
        with open("stundenplan.txt", "r") as file:
            input = str(file.read())
            input = input.replace("&$AE", "Ä")
            input = input.replace("&$OE", "Ö")
            input = input.replace("&$UE", "Ü")
            input = input.replace("&$ae", "ä")
            input = input.replace("&$oe", "ö")
            input = input.replace("&$ue", "ü")
            events = input.split("::\n")
            lectures = {}
            for weekday, day in zip(weekdays, events[0].split(";;")):
                lectures[weekday] = []
                for slot in day.split(",,"):
                    lectures[weekday].append(slot)
                del lectures[weekday][slots]
            del events[0]        
            tutorials = {}
            for event in events:
                tutorial = event.split(";;")
                name = tutorial[0]
                del tutorial[0]
                tutorials[name] = {}
                for weekday, day in zip(weekdays, tutorial):
                    tutorials[name][weekday] = []
                    for slot in day.split(",,"):
                        tutorials[name][weekday].append(slot)
                    del tutorials[name][weekday][slots]
            del tutorials[""]

        evaluate()
    except:
        messagebox.showinfo("Fehlermeldung", "Fehler beim Zugriff auf die Datei!", icon="error")
        print("Fehler beim Zugriff auf die Datei!")



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

window = Tk()
window.title("Stundenplaner")

title = ""
criteria = {}
criteria["free_monday"] = BooleanVar(value=FALSE)
criteria["free_friday"] = BooleanVar(value=FALSE)
criteria["least_first_slots"] = BooleanVar(value=FALSE)
criteria["least_days"] = BooleanVar(value=FALSE)

# Configure the Main Menu
menu_bar = Menu(window)
menu_bar.add_command(label="Laden", command=lambda: load_file())

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
        buttons[(i*slots)+j] = Button(window, text="frei", background="snow", command=lambda day=i, slot=j: switch_timeslot(day, slot))
    
checkboxes = {}
checkboxes["free_friday"] = Checkbutton(window, text="Freitag frei", variable=criteria["free_friday"], onvalue=TRUE, offvalue=FALSE, command=lambda: update_results())
checkboxes["free_monday"] = Checkbutton(window, text="Montag frei", variable=criteria["free_monday"], onvalue=TRUE, offvalue=FALSE, command=lambda: update_results())
checkboxes["least_first_slots"] = Checkbutton(window, text="Wenigste 8:00 Uhr Veranstaltungen", variable=criteria["least_first_slots"], onvalue=TRUE, offvalue=FALSE, command=lambda: update_results())
checkboxes["least_days"] = Checkbutton(window, text="Wenigste Tage", variable=criteria["least_days"], onvalue=TRUE, offvalue=FALSE, command=lambda: update_results())

start_hours = ["08:00", "10:00", "12:00", "14:00", "16:00", "18:00"]
earliest_slot = ttk.Combobox(window, state="readonly", values=start_hours)
earliest_slot.bind("<<ComboboxSelected>>", lambda _ : update_results())
earliest_slot.current(0)
end_hours = ["10:00", "12:00", "14:00", "16:00", "18:00", "20:00"]
latest_slot = ttk.Combobox(window, state="readonly", values=end_hours)
latest_slot.bind("<<ComboboxSelected>>", lambda _ : update_results())
latest_slot.current(len(end_hours)-1)

earliest_slot_label = Label(window, text="Früheste Uhrzeit:")
latest_slot_label = Label(window, text="Späteste Uhrzeit:")

continue_button = Button(window, text="Weiter", command=lambda: next_state())
finished_button = Button(window, text="Fertig", command=lambda: evaluate())
show_results_button = Button(window, text="0 Ergebnisse anzeigen", command=lambda: load_timetable_UI("Ergebnisse", get_results(possible_timetables)))

title_label = Label(window, text="Gib den Namen der Veranstaltung ein:")
title_entry = Entry(window, textvariable=title)

# Organize window
load_input_UI()

window.config(menu=menu_bar)

window.mainloop()