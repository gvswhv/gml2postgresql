# GML2PostgreSQL – QGIS Plugin

**Sprache / Language:** [Deutsch](#deutsch) | [English](#english)

---

## Deutsch

### Übersicht

GML2PostgreSQL ist ein QGIS-Plugin zur automatisierten Übernahme von XPlanung-Objekten aus GML-Dateien in eine bestehende PostgreSQL/PostGIS-Datenbank. Es wurde entwickelt, um Kommunen den Aufwand der manuellen Datenaufbereitung zu ersparen und die Digitalisierung von Bauleitplänen nach dem XPlanung-Standard zu unterstützen.

Das Plugin wurde von der **Stadt Wilhelmshaven** entwickelt und als Open-Source-Werkzeug für andere Kommunen und Planungsbehörden bereitgestellt.

**Herausgeber:** Stadt Wilhelmshaven – Geoinformatik, Vermessung und Statistik (GVS)
**Entwickler:** Ahmed Letaief
**Kontakt:** GVS@wilhelmshaven.de

---

### Funktionsumfang

- Auswahl eines Ordners mit GML-Dateien (inkl. Unterordner)
- Automatische Erkennung und Verarbeitung relevanter XPlanung-Objektarten
- Unterstützung gemischter Geometrietypen (Punkt, Linie, Fläche) innerhalb einer Objektart
- Koordinatentransformation in EPSG:25832 (UTM Zone 32N)
- Duplikaterkennung anhand der `gml_id` – erneutes Ausführen ist sicher
- Verarbeitungsprotokoll im Plugin-Fenster mit Export als Logdatei
- Speicherung der Datenbankverbindungsparameter zwischen Sitzungen

---

### Unterstützte XPlanung-Objektarten

Das Plugin verarbeitet folgende Objektarten gemäß XPlanung 5.x:

| Objektart | Geometrie |
|---|---|
| BP_AnpflanzungBindungErhaltung | Punkt, Linie, Fläche |
| BP_BaugebietsTeilFlaeche | Punkt, Linie, Fläche |
| BP_BauGrenze | Linie |
| BP_GemeinbedarfsFlaeche | Fläche |
| BP_GemeinschaftsanlagenFlaeche | Fläche |
| BP_GenerischesObjekt | Punkt, Linie, Fläche |
| BP_GewaesserFlaeche | Fläche |
| BP_GruenFlaeche | Fläche |
| BP_Immissionsschutz | Linie, Fläche |
| BP_LandwirtschaftsFlaeche | Fläche |
| BP_NebenanlagenFlaeche | Fläche |
| BP_NichtUeberbaubareGrundstuecksflaeche | Fläche |
| BP_SchutzPflegeEntwicklungsFlaeche | Fläche |
| BP_SchutzPflegeEntwicklungsMassnahme | Fläche |
| BP_StrassenVerkehrsFlaeche | Fläche |
| BP_UeberbaubareGrundstuecksFlaeche | Fläche |
| BP_VerEntsorgung | Punkt, Linie, Fläche |
| BP_VerkehrsflaecheBesondererZweckbestimmung | Punkt, Fläche |
| BP_WaldFlaeche | Fläche |
| BP_WasserwirtschaftsFlaeche | Fläche |
| BP_Wegerecht | Punkt, Linie, Fläche |

---

### Voraussetzungen

- QGIS 3.x
- PostgreSQL mit PostGIS-Erweiterung
- Python-Paket `psycopg2` (in der QGIS-Python-Umgebung installiert)
- Ein vorbereitetes Datenbankschema (siehe [Datenbankeinrichtung](#datenbankeinrichtung))

#### psycopg2 installieren

**Windows (OSGeo4W Shell):**
```
pip install psycopg2-binary
```

**Linux/macOS:**
```bash
pip3 install psycopg2-binary
```

---

### Installation

1. Dieses Repository als ZIP-Datei herunterladen oder klonen:
   ```
   git clone https://github.com/gvswhv/gml2postgresql.git
   ```

2. Den Ordner `gml2postgresql` (der Ordner mit `__init__.py`) in das QGIS-Plugin-Verzeichnis kopieren:

   - **Windows:** `C:\Users\<Benutzername>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\`
   - **Linux:** `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
   - **macOS:** `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/`

3. QGIS starten (oder neu starten), dann unter **Erweiterungen → Erweiterungen verwalten und installieren → Installiert** das Plugin `gml2postgresql` aktivieren.

4. Das Plugin erscheint anschließend in der Symbolleiste und im Menü unter **Erweiterungen → GML2PostgreSQL**.

---

### Datenbankeinrichtung

Vor dem ersten Einsatz muss das Datenbankschema mit allen benötigten Tabellen angelegt werden.

1. Die Datei `sql/xplan_Objektarten.sql` öffnen.

2. In **Zeile 16** sowie im **gesamten Skript** den Schemanamen `xplan` durch den gewünschten Namen ersetzen. Empfehlung: Funktion „Suchen & Ersetzen" im Texteditor oder in pgAdmin verwenden.

3. Das Skript in pgAdmin oder psql gegen die Zieldatenbank ausführen:
   ```bash
   psql -h localhost -U <Benutzer> -d <Datenbank> -f sql/xplan_Objektarten.sql
   ```

> **Hinweis:** Das Skript löscht vorhandene Tabellen mit `DROP TABLE IF EXISTS`, bevor es sie neu anlegt. Bei einer Neueinrichtung gehen dabei alle vorhandenen Daten verloren.

---

### Verwendung

1. Plugin über die Symbolleiste oder das Menü **Erweiterungen → GML2PostgreSQL** öffnen.
2. Über **Durchsuchen** den Ordner mit den GML-Dateien auswählen. Unterordner werden automatisch einbezogen.
3. Datenbankverbindungsparameter eintragen:
   - **Host** – z. B. `localhost`
   - **Port** – Standard: `5432`
   - **Datenbankname**
   - **Schema** – der zuvor eingerichtete Schemaname
   - **Benutzer**
   - **Passwort**
4. Auf **Starten** klicken. Der Fortschritt wird im Protokollbereich angezeigt.
5. Nach Abschluss kann das Protokoll über **Log speichern** als Textdatei exportiert werden.

Die Verbindungsparameter (außer dem Passwort) werden automatisch für die nächste Sitzung gespeichert.

---

### Hinweise zur Logdatei

Nach jeder Verarbeitung sollte die Logdatei auf Einträge mit `[FEHLER]` oder `[WARNUNG]` geprüft werden:

- `[FEHLER] INSERT fehlgeschlagen` – Ein Feature konnte nicht importiert werden, z. B. wegen ungültiger oder unerwarteter Attributwerte in der GML-Datei. Das Feature wird übersprungen, die Verarbeitung läuft weiter.
- `[WARNUNG] Geometrie nicht konvertierbar` – Die Geometrie eines Features konnte nicht in den Zieltyp umgewandelt werden. Das Feature wird übersprungen.
- `[WARNUNG] unbekannter Geometrietyp` – Ein Feature enthält einen Geometrietyp, der vom Plugin nicht unterstützt wird.

Duplikate (Features mit einer bereits vorhandenen `gml_id`) werden stillschweigend übersprungen und als `Duplikate` gezählt, nicht als Fehler.

---

### Bekannte Einschränkungen

- Das Plugin unterstützt ausschließlich **XPlanung 5.x**. Ältere Versionen (4.x) wurden nicht getestet und werden voraussichtlich nicht korrekt verarbeitet.
- Es werden nur die in der obigen Tabelle aufgeführten Objektarten importiert. Weitere XPlanung-Objektarten (z. B. FP_, LP_, RP_) werden nicht berücksichtigt.
- Kurvengeometrien (CurvePolygon, CompoundCurve, CircularString) werden automatisch segmentiert, da PostGIS-Tabellen einfache Geometrietypen erwarten. Bei sehr stark gekrümmten Geometrien kann dabei eine leichte Abweichung von der Originalgeometrie entstehen.
- Bei Objektarten mit gemischten Geometrietypen (z. B. `BP_Wegerecht`) wird jedes Feature anhand seiner tatsächlichen Geometrie automatisch der entsprechenden Tabelle (`_po`, `_li`, `_py`) zugeordnet.
- Die Qualität der importierten Daten hängt von der Qualität der GML-Quelldateien ab. Fehlerhafte oder nicht standardkonforme GML-Dateien können zu übersprungenen Features führen.

---

### Layerstile / Symbologie

Das Plugin importiert die Geometrie- und Attributdaten der XPlanung-Objekte, enthält jedoch keine Layerstile. Für eine normkonforme Darstellung der importierten Layer entsprechend der XPlanung-Farbgebung empfehlen wir das Plugin **xplan-reader** des Kreises Viersen:

> [https://github.com/kreis-viersen/xplan-reader](https://github.com/kreis-viersen/xplan-reader)

Die dort enthaltenen QML-Stile können in QGIS über **Layereigenschaften → Stil → Stil speichern → In Datenbank (PostgreSQL)** dauerhaft in der Datenbank hinterlegt werden. QGIS lädt den Stil dann beim nächsten Hinzufügen des Layers automatisch.

---

### Lizenz

GNU General Public License v3.0 – © 2025 Stadt Wilhelmshaven

Weitere Details: [LICENSE](LICENSE) · [https://www.gnu.org/licenses/gpl-3.0.html](https://www.gnu.org/licenses/gpl-3.0.html)

---

## English

### Overview

GML2PostgreSQL is a QGIS plugin for automated import of XPlanung objects from GML files into an existing PostgreSQL/PostGIS database. It is designed to reduce manual data preparation effort for municipalities and support the digitisation of land-use plans according to the XPlanung standard.

The plugin was developed by the **City of Wilhelmshaven** and released as an open-source tool for other municipalities and planning authorities.

**Developer:** Ahmed Letaief
**Publisher:** City of Wilhelmshaven – Geoinformatics, Surveying and Statisitcs (GVS)
**Contact:** GVS@wilhelmshaven.de

---

### Features

- Select a folder of GML files (subfolders included)
- Automatic detection and processing of supported XPlanung object types
- Mixed geometry support (point, line, polygon) within a single object type
- Coordinate transformation to EPSG:25832 (UTM Zone 32N)
- Duplicate detection by `gml_id` – safe to re-run on the same folder
- Processing log displayed in the plugin window, exportable as a text file
- Database connection parameters saved between sessions

---

### Requirements

- QGIS 3.x
- PostgreSQL with PostGIS extension
- Python package `psycopg2` installed in QGIS's Python environment
- A prepared database schema (see [Database Setup](#database-setup))

#### Installing psycopg2

**Windows (OSGeo4W Shell):**
```
pip install psycopg2-binary
```

**Linux/macOS:**
```bash
pip3 install psycopg2-binary
```

---

### Installation

1. Download this repository as a ZIP file or clone it:
   ```
   git clone https://github.com/gvswhv/gml2postgresql.git
   ```

2. Copy the `gml2postgresql` folder (the one containing `__init__.py`) into your QGIS plugins directory:

   - **Windows:** `C:\Users\<Username>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\`
   - **Linux:** `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
   - **macOS:** `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/`

3. Start (or restart) QGIS, then go to **Plugins → Manage and Install Plugins → Installed** and enable `gml2postgresql`.

4. The plugin will appear in the toolbar and under **Plugins → GML2PostgreSQL**.

---

### Database Setup

The database schema must be created before the plugin can be used.

1. Open `sql/xplan_Objektarten.sql`.

2. Replace the schema name `xplan` on **line 16** and throughout the entire script with your preferred schema name. Using Find & Replace in a text editor or pgAdmin is recommended.

3. Run the script against your target database using pgAdmin or psql:
   ```bash
   psql -h localhost -U <user> -d <database> -f sql/xplan_Objektarten.sql
   ```

> **Note:** The script drops existing tables with `DROP TABLE IF EXISTS` before recreating them. All existing data in those tables will be lost when re-running the script.

---

### Usage

1. Open the plugin from the toolbar or via **Plugins → GML2PostgreSQL**.
2. Click **Browse** to select the folder containing your GML files. Subfolders are included automatically.
3. Enter the database connection parameters:
   - **Host** – e.g. `localhost`
   - **Port** – default: `5432`
   - **Database name**
   - **Schema** – the schema name you set up earlier
   - **User**
   - **Password**
4. Click **Starten** (Run). Progress is displayed in the log area.
5. Once complete, click **Log speichern** (Save Log) to export the log as a text file.

Connection parameters (except the password) are saved automatically for the next session.

---

### Reading the Log File

After each run, the log file should be checked for `[FEHLER]` (error) and `[WARNUNG]` (warning) entries:

- `[FEHLER] INSERT fehlgeschlagen` – A feature could not be imported, e.g. due to invalid or unexpected attribute values in the GML file. The feature is skipped and processing continues.
- `[WARNUNG] Geometrie nicht konvertierbar` – A feature's geometry could not be converted to the target type. The feature is skipped.
- `[WARNUNG] unbekannter Geometrietyp` – A feature contains a geometry type not supported by the plugin.

Duplicates (features with a `gml_id` already present in the database) are silently skipped and counted as `Duplikate`, not as errors.

---

### Known Limitations

- The plugin supports **XPlanung 5.x only**. Older versions (4.x) have not been tested and are unlikely to be processed correctly.
- Only the object types listed in the table above are imported. Other XPlanung object types (e.g. FP_, LP_, RP_) are not supported.
- Curve geometries (CurvePolygon, CompoundCurve, CircularString) are automatically segmented to simple geometry types as required by PostGIS. This may introduce minor deviations from the original geometry for strongly curved shapes.
- For object types with mixed geometry (e.g. `BP_Wegerecht`), each feature is automatically routed to the correct table (`_po`, `_li`, `_py`) based on its actual geometry.
- Import quality depends on the quality of the source GML files. Non-conformant or malformed GML files may result in skipped features.

---

### Layer Styles / Symbology

This plugin imports geometry and attribute data for XPlanung objects but does not include layer styles. For standards-compliant visualisation of the imported layers using official XPlanung colours, we recommend the **xplan-reader** plugin by Kreis Viersen:

> [https://github.com/kreis-viersen/xplan-reader](https://github.com/kreis-viersen/xplan-reader)

The QML styles included there can be saved permanently to the database in QGIS via **Layer Properties → Style → Save Style → In Database (PostgreSQL)**. QGIS will then load the style automatically the next time the layer is added.

---

### License

GNU General Public License v3.0 – © 2025 Stadt Wilhelmshaven

See [LICENSE](LICENSE) · [https://www.gnu.org/licenses/gpl-3.0.html](https://www.gnu.org/licenses/gpl-3.0.html)
