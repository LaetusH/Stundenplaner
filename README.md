# Stundenplaner

Dieses Python-Programm soll Studenten beim Planen ihres Stundenplans unterstützen. Es hilft dabei, die verschiedenen Kombinationsmöglichkeiten aus parallel stattfindenden Übungsgruppen zu berechnen, wobei bestimmte Kriterien eingestellt werden können. 

## Installation
### Voraussetzungen
Python muss auf dem System installiert sein. Falls noch nicht geschehen, kann es von der offiziellen [Python-Website](https://www.python.org/downloads/) heruntergeladen werden.

### Installation und Ausführung
1. Klone das Repository:
```bash
 git clone https://github.com/LaetusH/Stundenplaner.git
 cd stundenplaner
```

2. Führe das Programm aus:
```bash
 python main.py
```
oder
```bash
 python3 main.py
```

**Alternativ:**
Lade die Datei *main.py* herunter. Tippe dann in eine Konsole deiner Wahl den Befehl ```python``` oder ```python3``` und den Dateipfad ein. Die meisten Konsolen unterstützen auch die Möglichkeit, die Datei per Drag and Drop hinter den Befehl zu ziehen und fügen dann automatisch den Dateipfad ein.
    
## Nutzung

+ Nach dem Start des Programms kannst du zuerst alle Zeitslots auswählen, in denen zeitlich nicht flexible Veranstaltungen (z.B. Vorlesungen) stattfinden.

+ Mit **Weiter** kommst du zur Auswahl der Veranstaltungen, die parallel stattfinden (z.B. Übungen). Hier kannst du einen Titel für die Veranstaltung eingeben und alle parallel stattfindenden Gruppen der selben Veranstaltung auswählen.

+ Mit erneutem Drücken auf **Weiter** kannst du die nächste Veranstaltung eingeben.

+ Hast du alle Veranstaltungen eingegeben drücke **Fertig**. Im folgenden Menü hast du die Möglichkeit verschiedene Kriterien auszuwählen anhand derer die zutreffenden Stundenpläne ausgewählt werden. Diese kannst du dir mit Klick auf den unteren Knopf anzeigen lassen.

+ Du hast jederzeit die Möglichkeit über das Menü einen Veranstaltungsplan zu **laden**. Dies überschreibt alle bis dahin eingegebenen Veranstaltungen und lädt die Veranstaltungen aus der Datei *stundenplan.txt*. Diese Datei muss sich im selben Ordner wie das Python-Programm befinden.

+ Bei der Auswahl der Kriterien hast du außerdem die Möglichkeit den Veranstaltungsplan zu **speichern**. Dies erzeugt die Datei *stundenplan.txt* im selben Ordner wie das Python-Programm oder überschreibt sie.

## Auswahlkriterien

- **Möglichst wenige Tage:** zeigt Stundenpläne mit der kleinsten Anzahl an Tagen an
- **Montag frei:** zeigt Stundenpläne an, bei den montags frei ist
- **Freitag frei:** zeigt Stundenpläne an, bei den freitags frei ist
- **Möglichst wenige Lücken:** zeigt Stundenpläne an, die die kleinstmögliche Anzahl an Lücken haben
- **Möglichst wenige 8:00 Uhr Veranstaltungen:** zeigt Stundenpläne an, die die wenigsten Veranstaltungen im ersten Zeitslot haben
- **Früheste Uhrzeit:** zeigt Stundenpläne an, die keine wählbare Veranstaltung haben, die vor der gewählten Uhrzeit beginnt
- **Späteste Uhrzeit:** zeigt Stundenpläne an, die keine wählbare Veranstaltung haben, die nach der gewählten Uhrzeit endet
