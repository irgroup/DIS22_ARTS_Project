# Biases Konzept
In diesem Teil des Projekts, geht es darum, wie die Ergebnisse aus der labeling Session auf Biases untersucht und welche Erkenntnisse daraus geschöpft werden sollen.

---
### Cognitive Biases, die sich in diesem Projekt angesehen werden sollen:

-	**Confirmation Bias:** <br>
Die Tendenz, Informationen selektiv zu interpretieren oder zu suchen, die die eigenen Vorannahmen oder Überzeugungen bestätigen, und dabei Informationen zu ignorieren, die diesen widersprechen könnten. Dies könnte dazu führen, dass Personen Texte als weniger komplex bewerten, wenn sie ihren eigenen Vorstellungen entsprechen. 

-	**Belief perseverance:** <br>
Das Beharren auf einer hartnäckigen ersten Hypothese, obwohl neue Informationen dieser Überzeugung widersprechen.

-	**Dichotomy:** <br>
Ein absolutes Denkmuster und eine kognitive Verzerrung, bei dem eine Person Dinge nur in zwei extreme Stufen bzw. Kategorien unterteilt und ignoriert, dass sich dazwischen noch eine Skala von Graustufen befindet. Daher wird auch vom „Alles-Oder-Nichts-Denken“ gesprochen.


### Forschungsfragen:
1.	Werden Texte, die auf der linken oder rechten Seite stehen eher angeklickt?
2.	Werden längere Texte tendenziell als komplexer eingeschätzt?
3.	Werden kürzer Texte tendenziell als weniger komplex eingeschätzt?
<br>

### Herangehensweise:
-	CSV Dateien aus GitHub ziehen
-	in Jupyter Notebook laden
-	`Python` und `pandas` nutzen
    - einen ersten Überblick verschaffen
    - Verteilung der angeklickten Seiten vergleichen mit Goldstandard
        - Wenn man die „richtig“ gewählten Texte abzieht, bleiben dann besonders häufig Texte einer Seite übrig?
        - Wenn ja, überwiegt dieselbe Seite auch bei andern Teilnehmern?
        - Ähneln sich die entsprechenden Fragen bei den unterschiedlichen Teilnehmern?
    - Bias in der Textlänge
        - Text-Scoring mit Textlänge vergleichen
        - Texte in kurze, lange und ggf. mittellange Texte kategorisieren 
        - Kurze Texte des Goldstandards mit dem Score der Rater vergleichen
            - Werden kurze Texte, die vom Goldstandard als komplex eingeordnet werden, häufig von Teilnehmern als weniger komplex eingestuft?
<br>

### Warum sind diese Fragen interessant für das Gesamtprojekt?
In dem Gesamtprojekt geht es darum, Texte nach ihrer Komplexität einzuordnen. Das Prüfen auf Biases, kann dafür sorgen, vor Fehlschlüsse zu bewahren. Indem z. B. erkannt wird, dass häufig Texte einer Seite bevorzugt werden, kann darauf von der Implementierungs-Gruppe reagiert werden und ein Featur eingeführt werden, dass den Teilnehmer dazu bringt seine Auswahl mehr zu reflektieren. Auf der anderen Seite kann nach dem hinzufügen eines solchen Features durch erneute Analyse der selben Biases herausgefunden werden, ob das Feature einen Effekt hatte.  

---
### Weiterführende Überlegungen:
Sollte zukünftig, das Feature eingebaut werden, dass die Teilnehmer erfahren, für welchen Text sich die Mehrheit entschieden hat, wäre es interessant herauszufinden, ob das Wissen, zu erfahren, dass man der Mehrheit zugestimmt oder widersprochen hat, Einfluss auf die Entscheidung der Teilnehmer hat. Allerdings gestaltet sich die Erhebung dieser Erkenntnis als sehr kompliziert und würde vermutlich eine Umfrage nach der Session benötigen, welche den Rahmen dieses Projektes sprengt.

---
Felix Derksen <br>
Email: felix.derksen@smail.th-koeln.de <br>
Matrikelnummer: 11154081
