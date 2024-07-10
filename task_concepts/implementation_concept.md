# Konzept DIS22_ARTS_Project - Logger #

### Erfasste Daten in der History-Datei ###
- Timestamp (jetzt auch als DateTime) am Click-Event
- IDs der einzelnen Texte 
- ID des "Gewinner" Textes (reversed, Gewinner ist der nicht geklickte, "less simple" Text)
- Username des Nutzers und dessen Englischlevel (Englischlevel extern hinzugefügt)
- Stand der letzten Textauswahl 

### Userprofil ###
- Frontend:
    - 2 verschieden Button:
        - "Login" -> startet Login Prozess und prüft ob die Kombination aus Username und Passwort übereinstimmt
        - "Sign-Up" -> startet das Sign-Up Formular, bei welchem man seine Daten hinterlegen kann
            - Falls die Daten im Sign-Up Formular nicht vollständig sind, wird das Userprofil nicht gespeichert und es erscheint eine Fehlermeldung
    - (nicht implementiert) Userprofil Button wenn eingeloggt um Daten ändern zu können
- Username:
    - Muss Unique sein, deswegen wird geprüft, ob es eine Datei: "username.json" bereits gibt
    - Falls der Username bereits vorhanden ist, wird eine Fehlermeldung angezeigt
- Relevante Kenntnisstände zu Themen des Text-Korpus:
    - (nicht implementiert) nicht im Userprofil, da in einem Google-Docs Fragebogen erfasst, könnten aber nachträglich manuell ergänzt werden 
- Englisch-Level:
    - string = "B2.2", "C1.1" 
    - Als Streamlit Selectbox implementiert, damit es nur begrenzte und gleich formatierte Eingaben gibt
- Alter
    - Integer = 26
    - Als Streamlit number_input implementiert, um einen numerischen Wert zu gewährleisten ,mit einem Interval von 1, sowie nur Ganzzahlen
- Geschlecht
    - string = "Male", "Female", "Diverse"
    - Ebenfalls als Streamlit Selectbox implementiert, damit es nur begrenzte und gleich formatierte Eingaben gibt
- User Profil Dateien:
    - Jeder User hat eine JSON-Datei, in welcher alle Informationen festgehalten werden, Name der Datei = username.json  
- Passwort Management:
    - Passwort asymetrisch verschlüsselt (Hash), mit Sha256 Algorithmus
    - (nicht implementiert) Passwortrichtlinien
    - (nicht implementiert) Passwort vergessen Funktion, da es dafür eine Mail-Funktionalität geben müsste
- Erweiterbarkeit:
    - Es sollte sehr einfach sein, zusätzliche Daten im Sign-Up Formular zu erfassen oder an das Userprofil zu schreiben
- (nicht implementiert) Datenschutz akzeptieren beim Sign-Up (Checkbox)
 
### Wissensabfragen/Lückentexte/Fragemodalitäten (Wissensabfragen-Gruppe) ###
- Hilfestellung für die Gruppe, wie man die Daten ablegt und die Antworten der Wissensabfragen speichert

### Konfidenzintervall/Likert-Skala ###
- Als neuer Key am Dictionary bzw. als neue Column an der .csv Datei:
    - Skala sieht wie folgt aus: "I'm very sure the left text is simpler": 0,
    "I'm sure the left text is simpler": 1,
    "I'm pretty sure the left text is simpler": 2,
    "move the slider": 3,
    "I'm pretty sure the right text is simpler": 4,
    "I'm sure the right text is simpler": 5,
    "I'm very sure the right text is simpler": 6
- Skala wird mit Schieberegler hinterlegt werden 
- Implementation eines Weiter-Buttons, damit erst nach Auswahl des Textes und der Likert-Skala zur nächsten Frage gesprungen werden kann

### Design ###
- Lesbarkeit der Fragen durch Anpassen der Text- und Hintergrundfarben verbessern
- Überschrift geändert zu Fortschrittsanzeige: Current status labeling: xx
- Skala unter Fragen, Weiter-Button als ganz nach Unten
- Startseite/Übersichtseite: Anmeldefunktion kommt in die Mitte.
__________________________________________________________________________________________
__________________________________________________________________________________________

### Verworfene logging Möglichkeiten ###
- Um Mouse-Events zu tracken, müsste man um das Streamlit-Framework herum programmieren, daher zu aufwendig:
    - [mouseover Event](https://www.w3schools.com/jsref/event_onmouseover.asp)
    - [mousemove Event](https://www.w3schools.com/jsref/event_onmousemove.asp)
    - [mouseleave Event](https://www.w3schools.com/jsref/event_onmouseleave.asp)
    - [Mouse behavioral patterns and keystroke dynamics in End-User
    Development: What can they tell us about users’ behavioral attributes?](https://doi.org/10.1016/j.chb.2018.02.012)
- Klassische Logging values: Mögliche Fehlermeldungen/Application Errors oder Debug Messages? -> unnötig da die Anwendung nicht so komplex ist
__________________________________________________________________________________________
__________________________________________________________________________________________
### Zeitplan -> abgeschlossen ###

- Themen Grundgerüst fertig (Viki + Zoe):
  - Konfidenzintervall/Likert-Skala bis 30.05 (Viki + Zoe)
  - Weiter Button 30.05 (Viki)
  - Design (UI) 30.05 (Viki + Zoe) (nicht der Hauptfokus)
- Nach Rücksprache mit Björn (Termin noch nicht bekannt): weitere Feinheiten

- Themen fertig (Marvin):
  - User Sign Up soweit fertig, User werden als einzelne JSON Dateien unter workspace/data/userprofiles abgelegt
  - To Do bis 30.05:
    - Login auf die neuen Userprofile anpassen (Was passiert mit history?)
    - Validierung der Sign Up angaben (ist alles vollständig etc.)
  - To Do bis 06.06:
    - 'current_match_id' aus der history, ins Userprofil übernehmen
    - Kenntnisstände zu themen im Userprofil? (Sinnvoll?)
    - Ablage der Wissensabfragen
   
- Themen rund um Skala und Design abgeschlossen und funktional
 
__________________________________________________________________________________________
__________________________________________________________________________________________

### Kontakt ###
Marvin Weihrauch 
- Email: marvin_benedikt.weihrauch@smail.th-koeln.de
- Matrikelnummer: 11154518

Viktoria Hellmann
- Email: viktoria_dora_lotte.hellmann@smail.th-koeln.de
- Matrikelnummer: 11154077

Zoe Bartz
- Email: zoe_bernadette.bartz@smail.th-koeln.de
- Matrikelnummer: 11153679
