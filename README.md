# Willkommen auf Refugium - Praxisarbeit

# Webanwendung für Praxisarbeit - ipso! Bildungsmarken

## Überblick
Dieses Projekt ist im Rahmen der Praxisarbeit für das 3. Studienjahr (6. Semester) an der ipso! Bildungsmarken entstanden. Es umfasst die Fächer Datenbanken und Webentwicklung (DBWE), IT-Architektur (ITAR) sowie Virtualisierung und Cloud Computing (VICC) und demonstriert die Anwendung der erlernten Technologien und Methoden in einem praktischen Kontext.

## Ziel der Anwendung
Die Webanwendung bietet eine Plattform, auf der Benutzer interaktiv agieren können. Sie ermöglicht das Erstellen, Verwalten und Anzeigen von spezifischen Daten über eine intuitive Weboberfläche sowie den Zugriff über eine RESTful API.

## Technologiestack
- **Datenbanksystem:** PostgreSQL
- **Programmiersprache:** Python 3.9
- **Web-Framework:** Flask
- **Webserver:** Gunicorn in Kombination mit Nginx

## Architektur
Die Anwendung folgt einer modularen Architektur, wobei die Geschäftslogik, Datenpersistenz und die Präsentationsschicht klar voneinander getrennt sind. Ein detailliertes Architekturdiagramm und eine Beschreibung finden sich in der beigefügten Dokumentation.

## Setup und Deployment
Die Anwendung ist in einer Cloud-Umgebung bereitgestellt, um Hochverfügbarkeit und Skalierbarkeit zu gewährleisten. Details zur Einrichtung und zum Deployment-Prozess sind in der Dokumentation im Abschnitt "Infrastruktur" enthalten.

## Benutzerdokumentation
Eine kurze Bedienungsanleitung für Endnutzer ist im Anhang der Dokumentation zu finden. Diese beschreibt die wichtigsten Funktionen und den Umgang mit der Webanwendung.

## Entwicklung und Beiträge
### Lokale Entwicklung
Um das Projekt lokal zu starten, führen Sie die folgenden Schritte aus:

1. Klone das Repository:
git clone <https://github.com/Giofox47/refugium.git>

markdown
Copy code
2. Installiere die Abhängigkeiten:
pip install -r requirements.txt

markdown
Copy code
3. Starte die Anwendung:
flask run

perl
Copy code

### Tests
Die für die Anwendung entwickelten Tests können mit dem folgenden Befehl ausgeführt werden:
pytest

perl
Copy code
Eine ausführliche Beschreibung der Tests und des Testprotokolls ist in der Dokumentation enthalten.

## Zugang zur Anwendung
Die Anwendung ist über die folgende URL erreichbar: `<refugium.zarbo.ch>`
Login-Informationen und weitere Details zur Nutzung der API sind in der beigefügten Dokumentation bereitgestellt.

## Lizenz
This is an example application featured in my [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world). See the tutorial for instructions on how to work with it.

## Autoren
- Giovanni Zarbo

## Danksagung
Besonderer Dank gilt den Dozenten und Betreuern bei ipso! Bildungsmarken für die Unterstützung und Anleitung während des Projekts.
Passen Sie die Inhalte entsprechend den spezifischen Details Ihres Projekts und Ihrer Infrastruktur an. Die angegebenen Kommandos und URL-Platzhalter sollten durch die tatsächlichen Werte ersetzt werden.
