## Aufgabenkonzept: Interrater-Agreement bei der Bewertung von Textkomplexität

### Einleitung

Dieses Aufgabenkonzept untersucht verschiedene Korrelationen des Interrater-Agreement zwischen den Ratern, aber auch zwsichen Rater unf Gold-Rating.

Um diese Forschungsfragen zu beantworten, werden verschiedene Methoden und statistische Verfahren eingesetzt, darunter Cohens Kappa, Spearman-Rangkorrelation, Kendall-Tau-Korrelation, usw. Die Analyse wird mithilfe von Python wie `scipy.stats`, `scikit-learn`, `spaCy`, `pandas` und `statsmodels` durchgeführt.

Die Ergebnisse werden wertvolle Erkenntnisse darüber liefern, welche Faktoren das Interrater-Agreement bei der Bewertung der Textkomplexität beeinflussen.

### Forschungsfragen

1. **Unterscheidet sich das Interrater-Agreement bei der Bewertung der Textkomplexität zwischen sachlichen und narrativen Texten?**
    - **Methode:** Cohens Kappa, t-Test (abhängig von der Verteilung der Daten)
    - **Vorgehensweise:**
        1. Einsatz von SpaCy zur Identifikation der Textgattung oder manuell.
        2. **Interrater-Agreement berechnen:** Berechnen Sie das Interrater-Agreement (Cohens Kappa) separat für sachliche und narrative Texte.
        3. **Gruppenvergleich:** Vergleichen des Interrater-Agreement zwischen den beiden Gruppen mit einem geeigneten statistischen Mittel.
    - **Python:** `scipy.stats`, `scikit-learn`, `pandas`, `spaCy`
    - **Ziel:** Untersuchen, ob die Textgattung einen Einfluss auf die Übereinstimmung der Rater bei der Bewertung der Textkomplexität hat.

---

1. **Korreliert das Sprachniveau der Rater mit der Übereinstimmung mit dem Goldstandard?**
    - **Methode:** Spearman-Rangkorrelation, Kendall-Tau-Korrelation
    - **Vorgehensweise:** Berechnung der Korrelation zwischen Sprachniveau (ordinal) und Übereinstimmung mit Goldstandard.
    - **Python:** `scipy.stats`, `pandas`
    - **Ziel:** Untersuchung des Einflusses des Sprachniveaus.
    
    ---
    
2. **Gibt es bestimmte Textmerkmale (z.B. Länge, Satzkomplexität, Wortfrequenz), die das Interrater-Agreement beeinflussen?**
    - **Methode:** Regression (linear, logistisch), Entscheidungsbäume
    - **Vorgehensweise:** Extraktion von Textmerkmalen mit SpaCy. Modellierung der Beziehung zwischen Merkmalen und Übereinstimmung.
    - **Python:** `spaCy`, `scikit-learn`
    - **Ziel:** Identifizierung prädiktiver Textmerkmale.

---

1. **Forschungsfrage: Vergleich der Interrater-Übereinstimmung zwischen Studierenden und Experten**
    
    Forschungsplan:
    
    - **Methode:** Analyse der Interrater-Reliabilität
    - **Vorgehensweise:** Anwendung von Fleiss' Kappa für Gruppenbewertungen, um die Übereinstimmung innerhalb und zwischen den Gruppen zu messen.
    - **Python:** `Statsmodels` oder `scikit-learn`
    - **Ziel:** Ermittlung, ob die Expertise einen Effekt auf die Bewertungskonstanz besitzt.

---

1. **Verändert sich das Interrater-Agreement im Laufe der Zeit? Werden die Rater im Laufe des Experiments konsistenter oder weniger konsistent in ihren Bewertungen?**
    - **Methode:** Zeitreihenanalyse
    - **Vorgehensweise:**
        1. Analysieren der Zeit zwischen jeder Entscheidung, welche aus dem jeweiligen Rater entnommen werden kann
        2. Visualisierung der zeitlichen Dauer zwischen allen Rater
        3. Filtern/Unterscheidung zwischen Sprachnniveau oder Studenten vs Experten
        4. Optional: Interrater nach jedem Step wird berechnet
    - **Python:** `pandas`, `statsmodels`, `plotly`
    - **Ziel:** Untersuchen, ob sich die Übereinstimmung der Rater im Laufe des Experiments verändert besonders zwischen Gruppen.
