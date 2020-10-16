# IRIS Challenge – Vorgehen

## Generelle Organisation

Für alle Kompetenzen, welche wir innerhalb der Challenge bearbeiten, haben wir jeweils eine verantwortliche Person definiert. Die Zuteilung ist wie folgt:

* gdb/ddi/daw: @ChristopherFrame
* wet: @eugencuic
* sko: @lukasreber

Ziel ist es, dass wir uns zu Beginn der Challenge alle in unseren Kompetenz das nötige Grundwissen aneignen und anschliessend den anderen Teammitglieder ihr Wissen weitergeben.

Ein wöchentliches Teammeeting findet jeweils am Donnerstag 15:00 Online per Teams statt.

## Requirements

###Produkt
Das Endprodukt (die Webseite) muss folgende Anforderungen erfüllen:
(V1)
* Anzeige einer Auswahlliste von Centroids (hierbei kann der/die Anwender/in einen Wert zwischen 1-53 wählen)
* Nach der Selektion eines bestimmten Centroids, bekommt der/die Anwender/in eine Auswahl an Beobachtungen angezeigt, welche den entsprechenden Centroid beinhalten.
* Durch die Auswahl eine dieser Beobachtungen, wird dem Benutzer detaillierte Informationen zu der entsprechenden Centroid/Beobachtung Auswahl angezeigt. Dies ist:
  * Anzeige eines Diagramms mit der Anzahl Vorkommnissen des Centroids pro Zeiteinheit
  * Optional: Zusätzliche Informationen wie Anzahl Steps, Zeitpunkt der Beobachtung und weitere Informationen falls vorhanden
(V2)
* In der detaillierten Ansicht der Beobachtung kann zusätzlich pro Step das entsprechenden Image (?) mit den visualisierten Y-Streifen angezeigt werden.

### Datenbank / Data Wrangling
* Alle nötigen Informationen sind in der Datenbank vorhanden und abrufbar
* Das Datenbankmodell ist so konzipiert, dass die Abfragen welche über die Webseite aufgerufen werden, in angemessener Zeit bearbeitet werden können.

### Softwarekonstruktion
* Sourcecode wird über ein Repository getracked
* CI/CD Pipeline besteht und wird für die Entwicklung der Website verwendet
* Tests für die Applikation sind vorhanden und in der CI Pipeline integriert
* Der Code ist sauber strukturiert und kommentiert

## Timeline
Die Arbeitspakete werden mittels GitHub Projects gemanaged. Hierbei wurde eine initiale Liste an Arbeitspaketen (Issues) erfasst, welche im weiteren Verlauf des Projekt noch erweitert werden. Die jeweiligen Issues sind einem Meilenstein zugewiesen. Die Meilensteine sind wie folgt terminiert: (Alle zwei Wochen ist ein Meilenstein fertig)

22.10: Meilenstein 1 
Datenbank
* Datenbankmodell ist erstellt
* Postgres auf der VM installiert
* Datenbankmodell ist auf der DB umgesetzt
* Datenextraktion ist erfolgt (Wichtig: Hierbei ist noch nicht die komplette Extraktion der Daten nötigt. Es reicht, wenn z.B. 1 Tag an Beobachtungen in der DB sind)
Softwarekonstruktion
* CI/CD Pipeline ist erstellt: Was dies genau alles beinhaltet muss noch im Detail geklärt werden
* Testkonzept ist skizziert

05.11: Meilenstein 2
Datenbank
* ETL Pipeline ist umgesetzt
* Alle benötigten Daten befinden sich in der Datenbank
Webseite
* Grundgerüst der Webseite ist erstellt

19.11: Meilenstein 3
Webseite
* Webseite ist umgesetzt gemäss Requirements (V1)

03.12: Meilenstein 4
Webseite
* Webseite (V2) ist umgesetzt, alle bekannten Bugfixes sind behoben

## Risiken
Risiken können allenfalls zu einer Verschiebung des Zeitplans führen.

Technische Probleme: 
* Zugriff von Quellserver auf DB Server funktioniert nicht
* Performanceprobleme beim Lesen der Daten

Organisatorische Probleme:
* Die benötigten Fachexperten stehen nicht zur Verfügung
* Unerwartete andere grosse Aufwände der Teammembers
* Erforderliches technisches Know-How stellt sich als grösser als erwartet heraus

## Anmerkung
Wir sind uns zudem bewusst, dass wir noch mehr Zeit bis zur Abgabe der Challenge haben, jedoch möchten wir durch den definierten Zeitplan frühzeitig zu einem Resultat kommen um uns falls möglich gegen Ende des HS21 mehr auf andere Kompetenzen fokussieren zu können.
