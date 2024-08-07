Textbasierte Wissensabfrage

Das Projekt
- Eine Anzahl von Texten wird in Paaren miteinander verglichen
- Der simplere Text wird ausgewählt, dann wird das nächste paar miteinander verglichen
- Dadurch entsteht am Ende ein Ranking, bei dem es „einfache Texte“ und „komplexe Texte“ gibt
- Wir wollen durch inhaltliche Wissensabfragen untersuchen, ob ein Muster zu erkennen ist, dass die komplexeren Texte auch inhaltlich als schwerer zu verstehen gelten oder nicht

Methoden
- Abfrage durch 2 Multiple Choice-Fragen (4 Antwortmöglichkeiten mit jeweils nur einer korrekten Antwort) nach jeweils 10 Sortierungen

Entwicklung der Fragen
- Fragen werden von Chat GPT generiert und von uns auf Verständlichkeit geprüft
- Nach jedem 10. Paar, dass man sortiert, sollen 2 Multiple Choice Fragen gestellt werden
- Die Antworten werden in einer CSV-Datei gespeichert und können nach der Labelling-Session ausgewertet werden
- für jeden User wird eine CSV-Datei (user-id_response.csv) erstellt mit den Spalten: User-ID, Text-ID, Frage, Antwort (vom User ausgewählte Antwort) und richtige Antwort

Was wollen wir für Ergebnisse erzielen?

- Fragestellung: Sind Fragen bezogen auf komplexe gerankte Texte schwerer zu beantworten als Fragen, die auf simpler gerankte Texte bezogen sind?
- Vermutung: Fragen zu komplexer gerankten Texten sind schwieriger zu beantworten, da komplexe Texte tendenziell mehr Informationen sowie eine höhere Anzahl an relevanten Details liefern, was für den Annotator schwerer zu verarbeiten ist
- Wir wollen durch die Wissensabfrage herausfinden, ob es ein Muster gibt, bei dem Texte, die im Abschlussranking als komplex geranked werden, weniger Infos vom Nutzer wiedergegeben werden können bzw Fragen richtig beantwortet werden können als bei Texten, die weniger komplex sind
- Diese Ergebnisse werden analysiert und interpretiert sowie grafisch dargestellt (durch die grafische Darstellung lässt sich eine Abweichung/Überschneidung erkennen)

Mario Mitgutsch (11154085) Sebastian Mörs (11155429)
