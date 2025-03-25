from tkinter import *

state = "Vorlesungen"

def switch_timeslot(day, slot):
    match state:
        case "Vorlesungen":
            lectures[weekdays[day]][slot] = "belegt" if lectures[weekdays[day]][slot] == "" else ""
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
finished_button = Button(window, text="Fertig", command=lambda: next())

title_label = Label(window, text="Gib den Namen der Veranstaltung ein:")
title_entry = Entry(window, textvariable=title)

# Organize window
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

window.config(menu=menu_bar)

window.mainloop()
print(lectures)
print(tutorials)