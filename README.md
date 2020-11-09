# wordDSEGenerator
DSE Generator for Word documents
DSEGenerator Hilfe

1. Installation
Die Anwendung muss nicht wirklich installiert werden. Sie kann bereits auf dem USB Stick ausgeführt werden. Um es lokal auf der Festplatte zu betreiben, muss lediglich das komplette Verzeichnis an den gewünschten Ort kopiert werden.  



2. Starten und Funktionen
2.1 Starten der Anwendungen

Die Anwendung wird durch Doppelklick auf die “DSEGEnerator.exe” gestartet. Darunter findet man bereits eine Verknüpfung, die auch den Desktop oder eine beliebige andere Stelle kopiert werden kann, um schnell die Anwendung aufrufen zu können. 



















Nach dem Starten der Anwendung öffnet sich das Hauptfenster. 


Das Fenster ist in vier Bereiche unterteilt. 

[1] Im oberen Bereich findet sich die Dateiauswahl, um die vom Mandanten ausgefüllte Checkliste zu selektieren. 

[2] Im darunter liegenden Bereich wird die Version der Checkliste gezeigt und das dafür passende XML Template zum parsen der Liste. (dazu später mehr in Kapitel 2.3). 

[3] Im dritten Bereich wird der Verarbeitungsstatus angezeigt. Initial wird zur Auswahl einer Checkliste aufgefordert. 

[4] Im unteren Bereich finden sich die Buttons zum Generieren der Datenschutzerklärungen nach erfolgreichem Einlesen der Checkliste und das Speichern der erzeugten Dokumente an beliebiger Stelle im Dateisystem. 

Im Verzeichnis “test” befindet sich bereits ein Beispiel einer Checkliste, die mit der Anwendung kompatibel ist. (Dazu später mehr in Kapitel 2.3).

Wird diese Datei über den “Browse” Button ausgewählt, wird diese automatisch eingelesen. 















Es wird die Versionsnummer der Checkliste und des dazu ermittelten XML Templates angezeigt. Auch der Verarbeitungsstatus zeigt nun an, dass die Checkliste erfolgreich eingelesen wurde. 
Des Weiteren ist nun auch der Button “Generate DSE document” aktiviert worden. 

Wenn dieser betätigt wird, werden im Hintergrund alle relevanten Datenschutzerklärungen generiert. 


Der Verarbeitungstatus zeigt nun dass alle Dokumente erzeugt wurden und gespeichert werden können. Der Button “Save DSE Document” ist nun aktiv. 

Beim Betätigen des Buttons “Save DSE Document” öffnet sich wieder ein Datei-Dialog der zur Auswahl eines Ordners auffordert. 
Standardmäßig wird das “Output” Verzeichnis unterhalb der Anwendung selektiert. Es kann aber ein beliebiges Verzeichnis ausgewählt werden. 

Sobald die Eingabe bestätigt wird, werden die relevanten Dokumente erzeugt. 

Entsprechend der Auswahl der Test-Checkliste wird die Haupt-Datenschutzerklärung sowie die individuellen DSE-Dokumente für YouTube, Instagram, Facebook und Twitter erzeugt. 

Die Dateien werden mit einem Zeitstempel versehen, um zusammengenerierte Dokumente zu kennzeichnen. 

 






2.2 Verzeichnisstruktur
Wichtig für den Anwender sind lediglich die Verzeichnisse “data”, “templates” und “output”. 
“output”: In diesem Verzeichnis werden default-mäßig die Ausgabe-Dokumente gespeichert. 
“data”: 	Hierunter liegen für die Anwen-dung wichtige Daten. Im speziellen liegt hier die Datei “datenschutzbehoerden.xml” die, die Adressen aller deutschen Datenschutzbehörden im XML Format enthält. Diese werden verwendet, um automatisch in den Datenschutzerklärungen an geeignerter Stelle zu hinterlegen. Die Zuordnung erfolgt aufgrund des hinterlegten Bundeslandes im Erfassungsbogen (Checkliste). 
“templates”: 	In diesem Verzeichnis liegen die XML Templates die für das Einlesen der Checkliste, sowie die Generierung der Datenschutzerklärungen notwendig sind. Die Texte und Zuordnungen sind nicht “hart” kodiert, sondern über diese Konfigurationsdateien hinterlegt. 
2.3. Funktionsweise
Das Herzstück der Anwendung sind die im Ordner “templates” hinterlegten XML Dateien. 

2.3.1 Einleseprozess












Anhand des Checklist XML Templates werden Informationen aus dem Worddokument erkannt, eingeordnet und einem internen Datenmodell zugeführt, welches dann später zum Abfüllen der Datenschutzerklärungen verwendet wird. 

Beispiel: Adressfeld des Verantwortlichen im Erfassungsbogen 












Das Checkliste_template.xml spiegelt die Struktur des Word-Dokuments wieder und gibt an wo welche Information und in welcher Struktur (Checkliste, Freitext, Ja-Nein-Feld) hinterlegt ist. Z.B. kann man hier erkennen, dass der Verantwortliche in der zweiten Tabelle angegeben wird. In der zweiten Zeile der Tabelle wird die Information in einem Textfeld erfasst. 
Nach dem Einlesen kann man dann über “verantwortlicher.adresse” auf die Information zugreifen. 
2.3.2 Ausgabeprozess
Die eingelesenen Informationen werden nun über die Ausgabe Templates aufbereitet und dann in Word-Dokumente geschrieben. Pro Dokument gibt es ein Template. 




Um das vorherige Beispiel nochmals aufzugreifen, wird der Verantwortliche dann in den Dokumenten durch Referenzierung des Verantwortlichen und der adresse abgefüllt. Da die Adresse in einem Textfeld abgelegt war, kann man durch Aufteilung der einzelnen Zeilen auf die einzelnen Informationen wie Straße oder Bundesland zugreifen.



3. Testen
Die Anwendung befindet sich noch in einem frühen Entwicklungsstadium. Deswegen muss sie ausgiebig getestet werden. Falls Fehler erkannt werden sollten – und da bin ich mir sicher wird es einige geben – sind diese in GitHub zentral zu erfassen. GitHub stellt so etwas wie Socail Media für Entwickler dar und kann Projekte hosten inkl. Deren Versionierung (Git). Neben dem Hosting ist auch das managen von Projekten und die Verwaltung der Entwicklung, Releases inkl. Fehlernachverfolgung möglich. Der unten stehende Link führt zum Issue Tool für erkannte Fehlerbilder. 
https://github.com/misc77/wordDSEGenerator/issues


Einfach auf den grünen Button “New Issue” klicken, dann öffnet sich die Erfassungsmaske:
Dort den Titel der den Fehler am besten beschreibt eingeben und durch einen Kommentar weiter detaillieren. Anschließend mit “Submit new issue” den Fehler einstellen. 
Somit können die Fehler zentral festgehalten und bearbeitet werden. 