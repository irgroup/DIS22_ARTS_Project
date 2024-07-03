# Biases Konzept
In diesem Teil des Projekts, geht es darum, wie die Ergebnisse aus der labeling Session auf Biases untersucht und welche Erkenntnisse daraus geschöpft werden sollen.

---
## Häufig auftretende Biases, die sich in diesem Projekt angesehen werden sollen:
<br>

**Bias:** <br>
Confirmation Bias / Belief perseverance / Self-consistensy <br>
**Forschungsfrage:** <br>
 Tendieren die Rater dazu, Texte, die in der ersten Runde sehr viel leichter als ihr Vergleichstexte eingestuft wurden, auch weiterhin sehr viel leichter einzustufen, unabhängig vom Vergleichstext? <br>
**1. Hypothese:** <br>
Texte, die in der ersten Runde (d. h., wenn Sie das erste Mal gelesen werden) eindeutig leichter eingeschätzt werden, werden in den darauffolgenden Runden tendenziell immer sehr viel leichter eingeschätzt als der Vergleichstext. <br>
**2. Hypothese:** <br>
Texte, die in der ersten Runde (d. h., wenn Sie das erste Mal gelesen werden) eindeutig leichter eingeschätzt werden, werden in den darauffolgenden Runden tendenziell nicht mehr sehr viel leichter eingeschätzt als der Vergleichstext. <br>
<br>
**Herangehensweise:** <br>
1.	Nach Texten filtern, die in der ersten Runde die Tendenz 0 oder 6 haben
2.	Die nächsten Runden nach diesen Texten Filtern
3.	Prüfen, ob sie weiterhin tendenziell in die extreme eingestuft werden, insbesondere bei Vergleichen zu „leichten“ Texten nach Goldstandard <br>
<br>


**Bias:** <br>
Dichotomy <br>
**Forschungsfrage:** <br>
 Gibt es Rater, die dazu tendieren, vor allem in zwei Stufen auf der Tendenz-Skalar einzuordnen? <br>
**1. Hypothese:** <br>
Es gibt Rater, die dazu tendieren, in zwei Kategorien zu denken, also für jede Seite (links und rechts) nur eine Stufe auf der Tendenz-Skalar zu nutzen. <br>
**2. Hypothese:** <br>
Es gibt Rater, die dazu tendieren, die zwei Stufen auf der Tendenz-Skalar nicht zu nutzen. <br>
<br>
**Herangehensweise:** <br>
1.	Häufigkeit der gewählten Tendenzen anschauen
2.	Nach extremen Verteilungen prüfen
<br>
<br>
<br>

**Bias:** <br>
Unentschlossenheit | Vertrautheitseffekt (Familiarity Effect) / Anchoring Bias / Anpassungs- und Kalibrierungseffekt (Adjustment and Calibration Effect)  <br>
**Forschungsfrage:** <br>
Verändert sich die Entschlossenheit der User von Runde zu Runde? (Nutzung der Tendenz-Skalar) <br>
**1. Hypothese:** <br>
 Die Unentschlossenheit nimmt pro Rund ab. <br>
**2. Hypothese:** <br>
 Die Unentschlossenheit nimmt pro Rund zu. <br>
<br>
**Herangehensweise:** <br>
1.	Rater in Gruppe einordnen:
    1. Rater, die eine starke Entschlossenheit in Runde 1 aufweisen
    2. Rater, die kleine starke Entschlossenheit in Runde 1 aufweisen
2. Pipeline bauen, die die Fragen der 2. Runde bei jedem Rater in eine eiheitliche Reihenfolge bringt
3. Verlauf der Verteilung der Tendenz-Skalar anschauen
<br>
<br>
<br>

User-Gruppen ansehen




### Warum sind diese Fragen interessant für das Gesamtprojekt?
-	In dem Gesamtprojekt geht es darum, Texte nach ihrer Komplexität einzuordnen. Das Prüfen auf Biases, kann dafür sorgen, vor Fehlschlüsse zu bewahren. 
-	Indem z. B. erkannt wird, dass häufig Texte einer Seite bevorzugt werden, kann darauf von der Implementierungs-Gruppe reagiert werden und ein Featur eingeführt werden, dass den Teilnehmer dazu bringt seine Auswahl mehr zu reflektieren. Auf der anderen Seite kann nach dem hinzufügen eines solchen Features durch erneute Analyse der selben Biases herausgefunden werden, ob das Feature einen Effekt hatte.  

---
### Weiterführende Überlegungen:
Sollte zukünftig, das Feature eingebaut werden, dass die Teilnehmer erfahren, für welchen Text sich die Mehrheit entschieden hat, wäre es interessant herauszufinden, ob das Wissen, zu erfahren, dass man der Mehrheit zugestimmt oder widersprochen hat, Einfluss auf die Entscheidung der Teilnehmer hat. Allerdings gestaltet sich die Erhebung dieser Erkenntnis als sehr kompliziert und würde vermutlich eine Umfrage nach der Session benötigen, welche den Rahmen dieses Projektes sprengt.

---
Felix Derksen <br>
Email: felix.derksen@smail.th-koeln.de <br>
Matrikelnummer: 11154081
