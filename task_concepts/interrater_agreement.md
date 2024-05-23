Um die "Einfachheit" eines Textes zu messen, muss man bedenken, dass dieser Prozess von Menschenhand und mit Hilfe von Large Language Models (LLMs) wie OpenAI GPT4 durchgeführt wird.


Obwohl dieser Prozess nach ersten Experimenten gut funktionierte, haben wir uns dennoch die Mühe gemacht, die Texte manuell zu beschriften. Jeder Benutzer wird ein anderes Englischniveau haben und kein Muttersprachler sein.

Ein wichtiges Maß, um besser vergleichen zu können, wie nahe sich die Rater bei der Auswahl waren, ist die Inter-Rater Agreement-Reliabilität.
Für das Projekt gibt es verschiedene Maße der Inter-Rater Agreement, von denen zwei für uns von Bedeutung sind.

## Fleiss’ Kappa

Das $ \kappa$ gibt die Übereinstimmung zwischen mehreren Beurteilern, wenn die Nominalmetrik bei der Bewertung angewendet wird.

$$
\begin{equation}
\kappa = \frac{\bar{P} - \bar{P_e}}{1 - \bar{P_e}}
\end{equation}
$$

$P$: Der Mittelwert des Anteils der übereinstimmenden Beurteilerpaare über alle Items.

$P_e$: Der Mittelwert der quadrierten Anteile der Übereinstimmung (d.h. die erwartete Übereinstimmung).

In unserem Fall erweist sich dies als nützlich, da wir auf diese Weise in einfacher Weise einen Text als leichter oder schwerer beurteilen können. Für die Anwendung dieses Ansatzes ist es nicht erforderlich, das Elo-Rating zu berücksichtigen, da lediglich die Zuverlässigkeit der Rater bei der Messung desselben bewertet wird.

### Interpretation

$\kappa$ ≤ 0: Zufällige Übereinstimmung
0 ≤ $\kappa$ ≤ 0.2: Geringe Übereinstimmung
0.2 ≤ $\kappa$ ≤ 0.4: Mäßige Übereinstimmung
0.4 ≤ $\kappa$ ≤ 0.6: Moderate Übereinstimmung
0.6 ≤ $\kappa$ ≤ 0.8: Starke Übereinstimmung
0.80 ≤ $\kappa$ ≤ 1.00: (fast) perfekte Übereinstimmung

## Krippendorff’s Alpha Koeffizient

Der Krippendorff’s Alpha Koeffizient ist ein Maß für die Übereinstimmung zwischen mehreren Ratern, das sich durch seine Flexibilität auszeichnet. Es kann mit einer Vielzahl an Variablen, darunter die Anzahl der Rater oder die Art der Daten, verwendet werden. Dadurch ist es in der Lage, sowohl nominale, ordinale als auch kardinale Daten zu verarbeiten.

Im Normalfall ist $\alpha \lt \kappa$ gültig

$\alpha > 0,8$ ist eine perfekte Übereinstimmung zwischen den Beurteilern

## Auswertung in unserem Experiment

Mithilfe von Streamlit kann der Klick aufgezeichnet werden als einfach interpretiert werden und der nicht ausgewählte Text als schwer. Die Daten können in einer Dataframe umgewandelt werden und mithilfe von [Scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.cohen_kappa_score.html) oder [Statsmodel](https://www.statsmodels.org/dev/generated/statsmodels.stats.inter_rater.fleiss_kappa.html) bewertet werden.

Im Rahmen des Prozesses erfolgt keine Nutzung des ELO-Systems, da die Komplexität des Vorhabens einen Vergleich aller Kombinationen von Texten erforderlich machen würde.^

---

Arthur Ndiema, 11153672 arthur-muanza.ndiema@smail.th-koeln.de
