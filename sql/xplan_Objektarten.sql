-- =============================================================================
-- XPlanung Datenbankschema für GML2PostgreSQL
--
-- Erstellt von der Stadt Wilhelmshaven
-- Kompatibel mit XPlanung 5.x
--
-- Dieses Skript legt alle benötigten Tabellen und räumlichen Indizes an.
-- Bereits vorhandene Tabellen werden zuvor gelöscht (DROP IF EXISTS).
-- Voraussetzung: PostgreSQL mit PostGIS-Erweiterung
--
-- HINWEIS: Den Schemanamen 'xplan' in der naechsten Zeile sowie im gesamten
-- Skript nach Bedarf anpassen. Empfehlung: Suchen & Ersetzen verwenden.
-- =============================================================================

-- Schema: gewünschten Schemanamen hier und im gesamten Skript ersetzen
CREATE SCHEMA IF NOT EXISTS xplan;


-- Drop existing tables

DROP TABLE IF EXISTS xplan.BP_AnpflanzungBindungErhaltung_po;
DROP TABLE IF EXISTS xplan.BP_AnpflanzungBindungErhaltung_li;
DROP TABLE IF EXISTS xplan.BP_AnpflanzungBindungErhaltung_py;
DROP TABLE IF EXISTS xplan.BP_BaugebietsTeilFlaeche_po;
DROP TABLE IF EXISTS xplan.BP_BaugebietsTeilFlaeche_li;
DROP TABLE IF EXISTS xplan.BP_BaugebietsTeilFlaeche_py;
DROP TABLE IF EXISTS xplan.BP_BauGrenze;
DROP TABLE IF EXISTS xplan.BP_GemeinbedarfsFlaeche;
DROP TABLE IF EXISTS xplan.BP_GemeinschaftsanlagenFlaeche;
DROP TABLE IF EXISTS xplan.BP_GenerischesObjekt_po;
DROP TABLE IF EXISTS xplan.BP_GenerischesObjekt_li;
DROP TABLE IF EXISTS xplan.BP_GenerischesObjekt_py;
DROP TABLE IF EXISTS xplan.BP_GewaesserFlaeche;
DROP TABLE IF EXISTS xplan.BP_GruenFlaeche;
DROP TABLE IF EXISTS xplan.BP_Immissionsschutz_li;
DROP TABLE IF EXISTS xplan.BP_Immissionsschutz_py;
DROP TABLE IF EXISTS xplan.BP_LandwirtschaftsFlaeche;
DROP TABLE IF EXISTS xplan.BP_NebenanlagenFlaeche;
DROP TABLE IF EXISTS xplan.BP_NichtUeberbaubareGrundstuecksflaeche;
DROP TABLE IF EXISTS xplan.BP_SchutzPflegeEntwicklungsFlaeche;
DROP TABLE IF EXISTS xplan.BP_SchutzPflegeEntwicklungsMassnahme;
DROP TABLE IF EXISTS xplan.BP_StrassenVerkehrsFlaeche;
DROP TABLE IF EXISTS xplan.BP_UeberbaubareGrundstuecksFlaeche;
DROP TABLE IF EXISTS xplan.BP_VerEntsorgung_po;
DROP TABLE IF EXISTS xplan.BP_VerEntsorgung_li;
DROP TABLE IF EXISTS xplan.BP_VerEntsorgung_py;
DROP TABLE IF EXISTS xplan.BP_VerkehrsflaecheBesondererZweckbestimmung_po;
DROP TABLE IF EXISTS xplan.BP_VerkehrsflaecheBesondererZweckbestimmung_py;
DROP TABLE IF EXISTS xplan.BP_WaldFlaeche;
DROP TABLE IF EXISTS xplan.BP_WasserwirtschaftsFlaeche;
DROP TABLE IF EXISTS xplan.BP_Wegerecht_po;
DROP TABLE IF EXISTS xplan.BP_Wegerecht_li;
DROP TABLE IF EXISTS xplan.BP_Wegerecht_py;


-- Create tables

CREATE TABLE xplan.BP_AnpflanzungBindungErhaltung_po (
    fid serial PRIMARY KEY,
    gml_id text,
    massnahme text,
    gegenstand text,
    inkrafttretensDatum date,
    dateiname text,
    bplan text,
    geom geometry(POINT, 25832)
);

CREATE TABLE xplan.BP_AnpflanzungBindungErhaltung_li (
    fid serial PRIMARY KEY,
    gml_id text,
    massnahme text,
    gegenstand text,
    inkrafttretensDatum date,
    dateiname text,
    bplan text,
    geom geometry(LINESTRING, 25832)
);

CREATE TABLE xplan.BP_AnpflanzungBindungErhaltung_py (
    fid serial PRIMARY KEY,
    gml_id text,
    massnahme text,
    gegenstand text,
    inkrafttretensDatum date,
    dateiname text,
    bplan text,
    geom geometry(POLYGON, 25832)
);

CREATE TABLE xplan.BP_BaugebietsTeilFlaeche_po (
    fid serial PRIMARY KEY,
    gml_id text,
    allgArtDerBaulNutzung text,
    besondereArtDerBaulNutzung text,
    sondernutzung text,
    abweichungBauNVO text,
    bauweise text,
    bebauungsArt text,
    bebauungVordereGrenze text,
    bebauungRueckwaertigeGrenze text,
    bebauungSeitlicheGrenze text,
    inkrafttretensDatum date,
    dateiname text,
    bplan text,
    geom geometry(POINT, 25832)
);

CREATE TABLE xplan.BP_BaugebietsTeilFlaeche_li (
    fid serial PRIMARY KEY,
    gml_id text,
    allgArtDerBaulNutzung text,
    besondereArtDerBaulNutzung text,
    sondernutzung text,
    abweichungBauNVO text,
    bauweise text,
    bebauungsArt text,
    bebauungVordereGrenze text,
    bebauungRueckwaertigeGrenze text,
    bebauungSeitlicheGrenze text,
    inkrafttretensDatum date,
    dateiname text,
    bplan text,
    geom geometry(LINESTRING, 25832)
);

CREATE TABLE xplan.BP_BaugebietsTeilFlaeche_py (
    fid serial PRIMARY KEY,
    gml_id text,
    allgArtDerBaulNutzung text,
    besondereArtDerBaulNutzung text,
    sondernutzung text,
    abweichungBauNVO text,
    bauweise text,
    bebauungsArt text,
    bebauungVordereGrenze text,
    bebauungRueckwaertigeGrenze text,
    bebauungSeitlicheGrenze text,
    inkrafttretensDatum date,
    dateiname text,
    bplan text,
    geom geometry(POLYGON, 25832)
);

CREATE TABLE xplan.BP_BauGrenze (
    fid serial PRIMARY KEY,
    gml_id text,
    rechtscharakter text,
    inkrafttretensDatum date,
    dateiname text,
    bplan text,
    geom geometry(LINESTRING, 25832)
);

CREATE TABLE xplan.BP_GemeinbedarfsFlaeche (
    fid serial PRIMARY KEY,
    gml_id text,
    zweckbestimmung text,
    bauweise text,
    bebauungsArt text,
    inkrafttretensDatum date,
    dateiname text,
    bplan text,
    geom geometry(POLYGON, 25832)
);

CREATE TABLE xplan.BP_GemeinschaftsanlagenFlaeche (
    fid serial PRIMARY KEY,
    gml_id text,
    zweckbestimmung text,
    inkrafttretensDatum date,
    dateiname text,
    bplan text,
    geom geometry(POLYGON, 25832)
);

CREATE TABLE xplan.BP_GenerischesObjekt_po (
    fid serial PRIMARY KEY,
    gml_id text,
    zweckbestimmung text,
    inkrafttretensDatum date,
    dateiname text,
    bplan text,
    geom geometry(POINT, 25832)
);

CREATE TABLE xplan.BP_GenerischesObjekt_li (
    fid serial PRIMARY KEY,
    gml_id text,
    zweckbestimmung text,
    inkrafttretensDatum date,
    dateiname text,
    bplan text,
    geom geometry(LINESTRING, 25832)
);

CREATE TABLE xplan.BP_GenerischesObjekt_py (
    fid serial PRIMARY KEY,
    gml_id text,
    zweckbestimmung text,
    inkrafttretensDatum date,
    dateiname text,
    bplan text,
    geom geometry(POLYGON, 25832)
);

CREATE TABLE xplan.BP_GewaesserFlaeche (
    fid serial PRIMARY KEY,
    gml_id text,
    zweckbestimmung text,
    inkrafttretensDatum date,
    dateiname text,
    bplan text,
    geom geometry(POLYGON, 25832)
);

CREATE TABLE xplan.BP_GruenFlaeche (
    fid serial PRIMARY KEY,
    gml_id text,
    zweckbestimmung text,
    nutzungsform text,
    inkrafttretensDatum date,
    dateiname text,
    bplan text,
    geom geometry(POLYGON, 25832)
);

CREATE TABLE xplan.BP_Immissionsschutz_li (
    fid serial PRIMARY KEY,
    gml_id text,
    laermpegelbereich text,
    typ text,
    technVorkehrung text,
    inkrafttretensDatum date,
    dateiname text,
    bplan text,
    geom geometry(LINESTRING, 25832)
);

CREATE TABLE xplan.BP_Immissionsschutz_py (
    fid serial PRIMARY KEY,
    gml_id text,
    laermpegelbereich text,
    typ text,
    technVorkehrung text,
    inkrafttretensDatum date,
    dateiname text,
    bplan text,
    geom geometry(POLYGON, 25832)
);

CREATE TABLE xplan.BP_LandwirtschaftsFlaeche (
    fid serial PRIMARY KEY,
    gml_id text,
    zweckbestimmung text,
    inkrafttretensDatum date,
    dateiname text,
    bplan text,
    geom geometry(POLYGON, 25832)
);

CREATE TABLE xplan.BP_NebenanlagenFlaeche (
    fid serial PRIMARY KEY,
    gml_id text,
    zweckbestimmung text,
    inkrafttretensDatum date,
    dateiname text,
    bplan text,
    geom geometry(POLYGON, 25832)
);

CREATE TABLE xplan.BP_NichtUeberbaubareGrundstuecksflaeche (
    fid serial PRIMARY KEY,
    gml_id text,
    nutzung text,
    inkrafttretensDatum date,
    dateiname text,
    bplan text,
    geom geometry(POLYGON, 25832)
);

CREATE TABLE xplan.BP_SchutzPflegeEntwicklungsFlaeche (
    fid serial PRIMARY KEY,
    gml_id text,
    ziel text,
    inkrafttretensDatum date,
    dateiname text,
    bplan text,
    geom geometry(POLYGON, 25832)
);

CREATE TABLE xplan.BP_SchutzPflegeEntwicklungsMassnahme (
    fid serial PRIMARY KEY,
    gml_id text,
    ziel text,
    massnahme text,
    inkrafttretensDatum date,
    dateiname text,
    bplan text,
    geom geometry(POLYGON, 25832)
);

CREATE TABLE xplan.BP_StrassenVerkehrsFlaeche (
    fid serial PRIMARY KEY,
    gml_id text,
    nutzungsform text,
    inkrafttretensDatum date,
    dateiname text,
    bplan text,
    geom geometry(POLYGON, 25832)
);

CREATE TABLE xplan.BP_UeberbaubareGrundstuecksFlaeche (
    fid serial PRIMARY KEY,
    gml_id text,
    bauweise text,
    bebauungsArt text,
    bebauungVordereGrenze text,
    bebauungRueckwaertigeGrenze text,
    bebauungSeitlicheGrenze text,
    inkrafttretensDatum date,
    dateiname text,
    bplan text,
    geom geometry(POLYGON, 25832)
);

CREATE TABLE xplan.BP_VerEntsorgung_po (
    fid serial PRIMARY KEY,
    gml_id text,
    zweckbestimmung text,
    detaillierteZweckbestimmung text,
    inkrafttretensDatum date,
    dateiname text,
    bplan text,
    geom geometry(POINT, 25832)
);

CREATE TABLE xplan.BP_VerEntsorgung_li (
    fid serial PRIMARY KEY,
    gml_id text,
    zweckbestimmung text,
    detaillierteZweckbestimmung text,
    inkrafttretensDatum date,
    dateiname text,
    bplan text,
    geom geometry(LINESTRING, 25832)
);

CREATE TABLE xplan.BP_VerEntsorgung_py (
    fid serial PRIMARY KEY,
    gml_id text,
    zweckbestimmung text,
    detaillierteZweckbestimmung text,
    inkrafttretensDatum date,
    dateiname text,
    bplan text,
    geom geometry(POLYGON, 25832)
);

CREATE TABLE xplan.BP_VerkehrsflaecheBesondererZweckbestimmung_po (
    fid serial PRIMARY KEY,
    gml_id text,
    zweckbestimmung text,
    detaillierteZweckbestimmung text,
    nutzungsform text,
    inkrafttretensDatum date,
    dateiname text,
    bplan text,
    geom geometry(POINT, 25832)
);

CREATE TABLE xplan.BP_VerkehrsflaecheBesondererZweckbestimmung_py (
    fid serial PRIMARY KEY,
    gml_id text,
    zweckbestimmung text,
    detaillierteZweckbestimmung text,
    nutzungsform text,
    inkrafttretensDatum date,
    dateiname text,
    bplan text,
    geom geometry(POLYGON, 25832)
);

CREATE TABLE xplan.BP_WaldFlaeche (
    fid serial PRIMARY KEY,
    gml_id text,
    zweckbestimmung text,
    detaillierteZweckbestimmung text,
    eigentumsart text,
    betreten text,
    inkrafttretensDatum date,
    dateiname text,
    bplan text,
    geom geometry(POLYGON, 25832)
);

CREATE TABLE xplan.BP_WasserwirtschaftsFlaeche (
    fid serial PRIMARY KEY,
    gml_id text,
    zweckbestimmung text,
    detaillierteZweckbestimmung text,
    inkrafttretensDatum date,
    dateiname text,
    bplan text,
    geom geometry(POLYGON, 25832)
);

CREATE TABLE xplan.BP_Wegerecht_po (
    fid serial PRIMARY KEY,
    gml_id text,
    typ text,
    inkrafttretensDatum date,
    dateiname text,
    bplan text,
    geom geometry(POINT, 25832)
);

CREATE TABLE xplan.BP_Wegerecht_li (
    fid serial PRIMARY KEY,
    gml_id text,
    typ text,
    inkrafttretensDatum date,
    dateiname text,
    bplan text,
    geom geometry(LINESTRING, 25832)
);

CREATE TABLE xplan.BP_Wegerecht_py (
    fid serial PRIMARY KEY,
    gml_id text,
    typ text,
    inkrafttretensDatum date,
    dateiname text,
    bplan text,
    geom geometry(POLYGON, 25832)
);

-- Spatial indexes

CREATE INDEX idx_BP_AnpflanzungBindungErhaltung_po_geom ON xplan.BP_AnpflanzungBindungErhaltung_po USING GIST (geom);
CREATE INDEX idx_BP_AnpflanzungBindungErhaltung_li_geom ON xplan.BP_AnpflanzungBindungErhaltung_li USING GIST (geom);
CREATE INDEX idx_BP_AnpflanzungBindungErhaltung_py_geom ON xplan.BP_AnpflanzungBindungErhaltung_py USING GIST (geom);
CREATE INDEX idx_BP_BaugebietsTeilFlaeche_po_geom ON xplan.BP_BaugebietsTeilFlaeche_po USING GIST (geom);
CREATE INDEX idx_BP_BaugebietsTeilFlaeche_li_geom ON xplan.BP_BaugebietsTeilFlaeche_li USING GIST (geom);
CREATE INDEX idx_BP_BaugebietsTeilFlaeche_py_geom ON xplan.BP_BaugebietsTeilFlaeche_py USING GIST (geom);
CREATE INDEX idx_BP_BauGrenze_geom ON xplan.BP_BauGrenze USING GIST (geom);
CREATE INDEX idx_BP_GemeinbedarfsFlaeche_geom ON xplan.BP_GemeinbedarfsFlaeche USING GIST (geom);
CREATE INDEX idx_BP_GemeinschaftsanlagenFlaeche_geom ON xplan.BP_GemeinschaftsanlagenFlaeche USING GIST (geom);
CREATE INDEX idx_BP_GenerischesObjekt_po_geom ON xplan.BP_GenerischesObjekt_po USING GIST (geom);
CREATE INDEX idx_BP_GenerischesObjekt_li_geom ON xplan.BP_GenerischesObjekt_li USING GIST (geom);
CREATE INDEX idx_BP_GenerischesObjekt_py_geom ON xplan.BP_GenerischesObjekt_py USING GIST (geom);
CREATE INDEX idx_BP_GewaesserFlaeche_geom ON xplan.BP_GewaesserFlaeche USING GIST (geom);
CREATE INDEX idx_BP_GruenFlaeche_geom ON xplan.BP_GruenFlaeche USING GIST (geom);
CREATE INDEX idx_BP_Immissionsschutz_li_geom ON xplan.BP_Immissionsschutz_li USING GIST (geom);
CREATE INDEX idx_BP_Immissionsschutz_py_geom ON xplan.BP_Immissionsschutz_py USING GIST (geom);
CREATE INDEX idx_BP_LandwirtschaftsFlaeche_geom ON xplan.BP_LandwirtschaftsFlaeche USING GIST (geom);
CREATE INDEX idx_BP_NebenanlagenFlaeche_geom ON xplan.BP_NebenanlagenFlaeche USING GIST (geom);
CREATE INDEX idx_BP_NichtUeberbaubareGrundstuecksflaeche_geom ON xplan.BP_NichtUeberbaubareGrundstuecksflaeche USING GIST (geom);
CREATE INDEX idx_BP_SchutzPflegeEntwicklungsFlaeche_geom ON xplan.BP_SchutzPflegeEntwicklungsFlaeche USING GIST (geom);
CREATE INDEX idx_BP_SchutzPflegeEntwicklungsMassnahme_geom ON xplan.BP_SchutzPflegeEntwicklungsMassnahme USING GIST (geom);
CREATE INDEX idx_BP_StrassenVerkehrsFlaeche_geom ON xplan.BP_StrassenVerkehrsFlaeche USING GIST (geom);
CREATE INDEX idx_BP_UeberbaubareGrundstuecksFlaeche_geom ON xplan.BP_UeberbaubareGrundstuecksFlaeche USING GIST (geom);
CREATE INDEX idx_BP_VerEntsorgung_po_geom ON xplan.BP_VerEntsorgung_po USING GIST (geom);
CREATE INDEX idx_BP_VerEntsorgung_li_geom ON xplan.BP_VerEntsorgung_li USING GIST (geom);
CREATE INDEX idx_BP_VerEntsorgung_py_geom ON xplan.BP_VerEntsorgung_py USING GIST (geom);
CREATE INDEX idx_BP_VerkehrsflaecheBesondererZweckbestimmung_po_geom ON xplan.BP_VerkehrsflaecheBesondererZweckbestimmung_po USING GIST (geom);
CREATE INDEX idx_BP_VerkehrsflaecheBesondererZweckbestimmung_py_geom ON xplan.BP_VerkehrsflaecheBesondererZweckbestimmung_py USING GIST (geom);
CREATE INDEX idx_BP_WaldFlaeche_geom ON xplan.BP_WaldFlaeche USING GIST (geom);
CREATE INDEX idx_BP_WasserwirtschaftsFlaeche_geom ON xplan.BP_WasserwirtschaftsFlaeche USING GIST (geom);
CREATE INDEX idx_BP_Wegerecht_po_geom ON xplan.BP_Wegerecht_po USING GIST (geom);
CREATE INDEX idx_BP_Wegerecht_li_geom ON xplan.BP_Wegerecht_li USING GIST (geom);
CREATE INDEX idx_BP_Wegerecht_py_geom ON xplan.BP_Wegerecht_py USING GIST (geom);
