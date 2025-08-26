import copy
import os

from tkinter import *
from tkinter import ttk
from tkinter import messagebox

def load_input_UI():
    heading.grid(row=1, column=2, columnspan=days)
    heading.config(text="Klicke alle Zeitslots für eine Veranstaltung so oft an, dass die korrekte Art der Veranstaltung ausgewählt ist:")
    title_label.grid(row=(slots+3), column=2, columnspan=(days-2), sticky="W")
    title_entry.grid(row=(slots+4), column=2, columnspan=(days-2), sticky="W")

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


def load_timetable(boxes, rectangels, texts, heading1, timetables, direction=""):
    global currentTimetable
    match direction:
        case "previous":
            currentTimetable = (currentTimetable - 1 + len(timetables)) % len(timetables)
        case "next":
            currentTimetable = (currentTimetable + 1) % len(timetables)

    heading1.config(text=f"Dieser Stundenplan erfüllt die ausgewählten Kriterien: ({currentTimetable + 1}/{len(timetables)})")
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

    heading1 = Label(window1, text=f"Dieser Stundenplan erfüllt die ausgewählten Kriterien: (1/{len(timetables)})")
    
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

    previous_button = Button(window1, text="Vorheriges", command=lambda: load_timetable(boxes, rectangles, texts, heading1, timetables, "previous"))
    next_button = Button(window1, text="Nächstes", command=lambda: load_timetable(boxes, rectangles, texts, heading1, timetables, "next"))

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

    if (len(timetables) < 2):
        previous_button.config(state="disabled")
        next_button.config(state="disabled")

    load_timetable(boxes, rectangles, texts, heading1, timetables)

    window1.mainloop()


def switch_timeslot(day, slot):
    match state:
        case "Eingabe":
            temp[weekdays[day]][slot] = event_types[(event_types.index(temp[weekdays[day]][slot]) + 1) % len(event_types)]
        case _:
            raise Exception("State Error")
    
    buttons[(day*slots)+slot].config(text=temp[weekdays[day]][slot])
    buttons[(day*slots)+slot].config(background="snow") if temp[weekdays[day]][slot] == "" else buttons[(day*slots)+slot].config(background="pale turquoise")


def reset_button_label(day, slot):
    buttons[(day*slots)+slot].config(text="")
    buttons[(day*slots)+slot].config(background="snow")


def next_state():
    global state
    global temp
    match state:
        case "Eingabe":
            if (title_entry.get() != ""):
                all_events[title_entry.get()] = temp
                temp = {}
                for weekday in weekdays:
                    temp[weekday] = [""] * slots
                title_entry.delete(0, len(title_entry.get()))
            else:
                all_events[("Modul " + str(len(all_events)+1))] = temp
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
        return [timetable]

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


# Returns timetables that satisfy the selected criteria 
def get_results(timetables):
    if (len(timetables) == 0):
        return []
    criteria["earliest_slot"] = earliest_slot.current()
    criteria["latest_slot"] = latest_slot.current()

    least_days = 5
    least_first_slots = 5
    least_gaps = 30

    if (criteria["least_days"].get() or criteria["least_first_slots"].get() or criteria["compact"].get()):
        num_of_days = 0
        first_slots = 0
        num_of_gaps = 0
        for day in timetables[0].values():
            day_marked = FALSE
            gaps = 0
            previous_event = FALSE
            for i, slot in enumerate(day):
                if (slot != ""):
                    if (i == 0):
                        first_slots += 1
                    if (previous_event):
                        num_of_gaps += gaps
                    else:
                        previous_event = TRUE
                    day_marked = TRUE
                elif (previous_event):
                    gaps += 1
            if (day_marked):
                num_of_days += 1
        
        least_days = num_of_days
        least_first_slots = first_slots
        least_gaps = num_of_gaps

        for timetable in timetables:
            num_of_days = 0
            first_slots = 0
            num_of_gaps = 0
            for day in timetable.values():
                day_marked = FALSE
                gaps = 0
                previous_event = FALSE
                for i, slot in enumerate(day):
                    if (slot != ""):
                        if (i == 0):
                            first_slots += 1
                        if (previous_event):
                            num_of_gaps += gaps
                        else:
                            previous_event = TRUE
                        day_marked = TRUE
                    elif (previous_event):
                        gaps += 1
                if (day_marked):
                    num_of_days += 1
        
            if (num_of_days < least_days):
                least_days = num_of_days
            if (first_slots < least_first_slots):
                least_first_slots = first_slots
            if (num_of_gaps < least_gaps):
                least_gaps = num_of_gaps

    results = []
    for timetable in timetables:
        num_of_days = 0
        first_slots = 0
        num_of_gaps = 0
        earliest_slot_fullfilled = TRUE
        latest_slot_fullfilled = TRUE
        monday = FALSE
        friday = FALSE
        for name, day in timetable.items():
            day_marked = FALSE
            gaps = 0
            previous_event = FALSE
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
                    if (previous_event):
                        num_of_gaps += gaps
                    else:
                        previous_event = TRUE   
                    day_marked = TRUE
                elif (previous_event):
                    gaps += 1        
            if (day_marked):
                num_of_days += 1


        if ((not criteria["least_days"].get()) or (num_of_days <= least_days)):
            if ((not criteria["least_first_slots"].get()) or (first_slots <= least_first_slots)):
                if ((not criteria["compact"].get()) or (num_of_gaps <= least_gaps)):
                    if ((not criteria["free_monday"].get()) or (not monday)):
                        if ((not criteria["free_friday"].get()) or (not friday)):
                            if (earliest_slot_fullfilled):
                                if (latest_slot_fullfilled):
                                    results.append(timetable)
    return results


# Updates the visibility of the show results button according to the number of results
def update_results():
    global possible_timetables
    num_of_results = len(get_results(possible_timetables))
    if (num_of_results == 1):
        show_results_button.config(text=f"{num_of_results} Ergebnis anzeigen")
    else:
        show_results_button.config(text=f"{num_of_results} Ergebnisse anzeigen")
    if (num_of_results == 0):
        show_results_button.config(state="disabled")
    else:
        show_results_button.config(state="normal")


def load_search_UI():
    global state
    if (state != "Suche"):
        menu_bar.add_separator()
        menu_bar.add_command(label="Speichern", command=save_file)

    num_of_criteria = len(checkboxes) + 2
    heading.grid(row=1, column=1, columnspan=2)
    heading.config(text="Wähle die Suchkriterien aus und lasse dir die Ergebnisse anzeigen")
    
    checkboxes["least_days"].grid(row=2, column=1, sticky="W")
    checkboxes["free_monday"].grid(row=3, column=1, sticky="W")
    checkboxes["free_friday"].grid(row=4, column=1, sticky="W")
    checkboxes["compact"].grid(row=5, column=1, sticky="W")
    checkboxes["least_first_slots"].grid(row=6, column=1, sticky="W")
    earliest_slot.grid(row=num_of_criteria, column=2, sticky="W")
    latest_slot.grid(row=(num_of_criteria+1), column=2, sticky="W")

    earliest_slot_label.grid(row=num_of_criteria, column=1, sticky="W")
    latest_slot_label.grid(row=(num_of_criteria+1), column=1, sticky="W")

    select_events_button.grid(row=(num_of_criteria+3), column=1, columnspan=2, sticky="NS", ipadx=20)

    show_results_button.grid(row=(num_of_criteria+5), column=1, columnspan=2, sticky="NS", ipadx=20)
    show_results_button.config(state="disabled")

    # Spacing
    spacer[0].grid(row=0, column=0, padx=7)
    spacer[1].grid(row=(num_of_criteria+6), column=7, padx=7)
    spacer[2].grid(row=(num_of_criteria+2), column=1)
    spacer[3].grid(row=(num_of_criteria+4), column=1)

    state = "Suche"
    update_results()


def use_selection(window2, selection):
    global events
    events = {}
    for name, val in selection.items():
        if (val.get()):
            events[name] = all_events[name]
    window2.destroy()
    evaluate()


def load_select_UI():
    window2 = Toplevel()
    window2.title(title)

    # Create window elements
    spacer2 = []
    for i in range(0, 3):
        spacer2.append(Label(window2, text=""))

    selection = {}
    checkboxes = {}
    for name in all_events.keys():
        if name in events:
            selection[name] = BooleanVar(value=TRUE)
        else:
            selection[name] = BooleanVar(value=FALSE)
        checkboxes[name] = Checkbutton(window2, text=name, variable=selection[name], onvalue=TRUE, offvalue=FALSE)

    finished_button2 = Button(window2, text="Fertig", command=lambda: use_selection(window2, selection))

    heading2 = Label(window2, text="Wähle die Module aus, die abgebildet werden sollen: ")

    # Organise the window
    spacer2[0].grid(row=0, column=0, padx=7)
    heading2.grid(row=1, column=1, columnspan=1)

    for i, name in enumerate(checkboxes.keys()):
        checkboxes[name].grid(row=2+i, column=1, sticky="W")

    spacer2[2].grid(row=(len(all_events)+3), column=1)
    finished_button2.grid(row=(len(all_events)+4), column=1, sticky="NS", ipadx=20)
    spacer2[1].grid(row=(len(all_events)+5), column=2, padx=7)

    window2.mainloop()


def evaluate():
    global possible_timetables
    global events
    if (state != "Suche"):
        next_state()

        # Remove empty events
        empty_events = []
        for name, event in all_events.items():
            marked = FALSE
            for weekday in event.values():
                for slot in weekday:
                    if (slot != ""):
                        marked = TRUE
                        break
                if (marked):
                    break
            if (not marked):
                empty_events.append(name)
        for name in empty_events:
            del all_events[name]
        events = all_events

    # Search for all possible timetables
    lectures = {}
    for weekday in weekdays:
        lectures[weekday] = [""] * slots
    if (len(events) > 0):
        tutorials = copy.deepcopy(events)
        # Seperate lectures and tutorials
        for name, event in events.items():
            for weekday, day in event.items():
                for i, slot in enumerate(day):
                    if (slot == "Vorlesung"):
                        lectures[weekday][i] = name + " - VL"
                        tutorials[name][weekday][i] = ""
                    if (slot == "Zentralübung"):
                        lectures[weekday][i] = name + " - ZÜ"
                        tutorials[name][weekday][i] = ""

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
        possible_timetables = collapse(lectures, tutorials)
    else:
        possible_timetables = [lectures]

    # Change UI
    clear_input_UI()
    load_search_UI()


def save_file():
    output = ""
    for name, event in all_events.items():
        name = name.replace("Ä", "&$AE")
        name = name.replace("Ö", "&$OE")
        name = name.replace("Ü", "&$UE")
        name = name.replace("ä", "&$ae")
        name = name.replace("ö", "&$oe")
        name = name.replace("ü", "&$ue")
        output += name + ";;"
        for day in event.values():
            for slot in day:
                output += slot + ",,"
            output += ";;"
        output += "::\n"
    
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "stundenplan.txt"), "w+") as file:
        file.write(output)
    messagebox.showinfo("Hinweis", "Erfolgreich gespeichert.", icon="info")


def load_file():
    global all_events
    global events
    global temp

    try:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "stundenplan.txt"), "r") as file:
            input = str(file.read())
            input = input.replace("&$AE", "Ä")
            input = input.replace("&$OE", "Ö")
            input = input.replace("&$UE", "Ü")
            input = input.replace("&$ae", "ä")
            input = input.replace("&$oe", "ö")
            input = input.replace("&$ue", "ü")
            data = input.split("::\n")

            # Load tutorials
            all_events = {}
            for datum in data:
                event = datum.split(";;")
                name = event[0]
                del event[0]
                all_events[name] = {}
                for weekday, day in zip(weekdays, event):
                    all_events[name][weekday] = []
                    for slot in day.split(",,"):
                        all_events[name][weekday].append(slot)
                    del all_events[name][weekday][slots]
            del all_events[""]

        temp = {}
        messagebox.showinfo("Hinweis", "Datei erfolgreich geladen.", icon="info")
        events = all_events
        evaluate()
    except Exception as error:
        messagebox.showinfo("Fehlermeldung", "Fehler beim Zugriff auf die Datei!", icon="error")
        print("Fehler beim Zugriff auf die Datei!", error)



weekdays = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]
timeslots = ["08:00\n-\n10:00", "10:00\n-\n12:00", "12:00\n-\n14:00", "14:00\n-\n16:00", "16:00\n-\n18:00", "18:00\n-\n20:00"]
event_types = ["", "Vorlesung", "Zentralübung", "Übung"]

state = "Eingabe"
slots = len(timeslots)
days = len(weekdays)
events = {}
all_events = {}
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
criteria["compact"] = BooleanVar(value=FALSE)

# Configure the Main Menu
menu_bar = Menu(window)
menu_bar.add_command(label="Laden", command=load_file)

# Create window objects
spacer = []
for i in range(0, 4):
    spacer.append(Label(window, text=""))

heading = Label(window, text="Lorem ipsum")

weekday_labels = []
for i in range(0, days):
    weekday_labels.append(Label(window, text=weekdays[i]))

timeslot_labels = []
for i in range(0, slots):
    timeslot_labels.append(Label(window, text=timeslots[i]))

buttons = [None] * (days * slots)
for i in range(0, days):
    for j in range(0, slots):
        buttons[(i*slots)+j] = Button(window, text="", background="snow", command=lambda day=i, slot=j: switch_timeslot(day, slot))
    
checkboxes = {}
checkboxes["free_friday"] = Checkbutton(window, text="Freitag frei", variable=criteria["free_friday"], onvalue=TRUE, offvalue=FALSE, command=update_results)
checkboxes["free_monday"] = Checkbutton(window, text="Montag frei", variable=criteria["free_monday"], onvalue=TRUE, offvalue=FALSE, command=update_results)
checkboxes["least_first_slots"] = Checkbutton(window, text="Möglichst wenige 8:00 Uhr Veranstaltungen", variable=criteria["least_first_slots"], onvalue=TRUE, offvalue=FALSE, command=update_results)
checkboxes["least_days"] = Checkbutton(window, text="Möglichst wenige Tage", variable=criteria["least_days"], onvalue=TRUE, offvalue=FALSE, command=update_results)
checkboxes["compact"] = Checkbutton(window, text="Möglichst wenig Lücken", variable=criteria["compact"], onvalue=TRUE, offvalue=FALSE, command=update_results)

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

continue_button = Button(window, text="Weiter", command=next_state)
finished_button = Button(window, text="Fertig", command=evaluate)
select_events_button = Button(window, text="Module auswählen", command=load_select_UI)
show_results_button = Button(window, text="0 Ergebnisse anzeigen", command=lambda: load_timetable_UI("Ergebnisse", get_results(possible_timetables)))

title_label = Label(window, text="Gib den Namen der Veranstaltung ein:")
title_entry = Entry(window, textvariable=title, width=40)

# Organize window
load_input_UI()

window.config(menu=menu_bar)

window.mainloop()