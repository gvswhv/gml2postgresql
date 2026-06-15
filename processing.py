# -*- coding: utf-8 -*-
"""
processing.py – GML parsing, geometry conversion and database import

This module contains all processing logic that is independent of the QGIS UI:

  - connect_db          : establish a psycopg2 connection
  - extract_gml_value   : read a single element value from a GML header
  - convert_qvariant    : safely convert QGIS QVariant to a plain Python value
  - convert_geometry    : normalise QGIS geometry objects to a target WKB type
  - process_single_layer: import one fixed-geometry GML layer into PostGIS
  - process_multi_layer : import one mixed-geometry GML layer, dispatching each
                          feature to the correct suffixed table
"""

import os
import xml.etree.ElementTree as ET

import psycopg2

from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsGeometry,
    QgsProject,
    QgsVectorLayer,
    QgsWkbTypes,
)
from PyQt5.QtCore import QVariant

from .layer_config import MULTI_GEOMETRY_LAYERS, SUFFIX_TO_GEOMETRY_TYPE

# Target coordinate reference system used for all imported geometries
TARGET_CRS = QgsCoordinateReferenceSystem("EPSG:25832")


# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------

def connect_db(host, port, db_name, user, password, log_func=None):
    """Open and return a psycopg2 connection, or None on failure."""
    try:
        return psycopg2.connect(
            host=host,
            port=int(port),
            database=db_name,
            user=user,
            password=password,
        )
    except Exception as exc:
        if log_func:
            log_func(f"[FEHLER] Datenbankverbindung fehlgeschlagen: {exc}")
        return None


# ---------------------------------------------------------------------------
# GML / attribute helpers
# ---------------------------------------------------------------------------

def extract_gml_value(gml_file, tag_name, log_func=None):
    """Return the text content of the first matching element in a GML file.

    The XPlanung namespace is detected automatically from the root element,
    so the function works regardless of whether files use XPlanung 5.x or 6.x
    namespaces.
    """
    try:
        tree = ET.parse(gml_file)
        root = tree.getroot()
        namespace = root.tag.split("}")[0].strip("{")
        ns = {"xplan": namespace}
        tag = root.find(f".//xplan:{tag_name}", ns)
        return tag.text if tag is not None else None
    except Exception as exc:
        if log_func:
            log_func(f"[WARNUNG] Fehler beim Lesen von '{tag_name}' aus {os.path.basename(gml_file)}: {exc}")
        return None


def convert_qvariant(value):
    """Convert a QGIS QVariant to a plain Python value, or None if empty."""
    if value is None or value == "" or value == QVariant():
        return None
    if isinstance(value, QVariant):
        return value.toString() if value.canConvert(QVariant.String) else None
    return value


# ---------------------------------------------------------------------------
# Geometry conversion
# ---------------------------------------------------------------------------

def convert_geometry(geom, target_type, log_func=None):
    """Convert a QgsGeometry object to the requested simple geometry type.

    XPlanung GML files frequently contain curve-based geometry types
    (CurvePolygon, CompoundCurve, CircularString, MultiSurface) that PostGIS
    simple-geometry columns do not accept directly.  This function segments
    all curve types and extracts the first part of any multi-geometry so that
    the result always matches the column's declared type.

    Parameters
    ----------
    geom        : QgsGeometry – input geometry (may be None or empty)
    target_type : str         – one of "POINT", "LINESTRING", "POLYGON"
    log_func    : callable    – optional logging callback

    Returns
    -------
    QgsGeometry on success, None if conversion is not possible.
    """
    if geom is None or geom.isEmpty():
        return None

    try:
        wkb = geom.wkbType()

        if target_type == "POLYGON":
            if wkb == QgsWkbTypes.CurvePolygon:
                segmented = QgsGeometry(geom.constGet().segmentize())
                if segmented.wkbType() == QgsWkbTypes.Polygon:
                    return segmented
                if segmented.wkbType() == QgsWkbTypes.MultiPolygon:
                    parts = segmented.asMultiPolygon()
                    return QgsGeometry.fromPolygonXY(parts[0]) if parts else None

            if wkb == QgsWkbTypes.MultiSurface:
                geom = QgsGeometry(geom.constGet().toCurveType().segmentize())
                wkb = geom.wkbType()

            if wkb == QgsWkbTypes.MultiPolygon:
                parts = geom.asMultiPolygon()
                return QgsGeometry.fromPolygonXY(parts[0]) if parts else None

            if wkb == QgsWkbTypes.Polygon:
                return geom

        elif target_type == "LINESTRING":
            if wkb in (QgsWkbTypes.CompoundCurve, QgsWkbTypes.CircularString):
                segmented = QgsGeometry(geom.constGet().segmentize())
                if segmented.wkbType() == QgsWkbTypes.LineString:
                    return segmented
                if segmented.wkbType() == QgsWkbTypes.MultiLineString:
                    parts = segmented.asMultiPolyline()
                    return QgsGeometry.fromPolylineXY(parts[0]) if parts else None

            if wkb == QgsWkbTypes.MultiLineString:
                parts = geom.asMultiPolyline()
                return QgsGeometry.fromPolylineXY(parts[0]) if parts else None

            if wkb == QgsWkbTypes.LineString:
                return geom

        elif target_type == "POINT":
            if wkb == QgsWkbTypes.Point:
                return geom
            if wkb == QgsWkbTypes.MultiPoint:
                parts = geom.asMultiPoint()
                return QgsGeometry.fromPointXY(parts[0]) if parts else None

        return None

    except Exception as exc:
        if log_func:
            log_func(f"[WARNUNG] Geometriekonvertierung fehlgeschlagen: {exc}")
        return None


# ---------------------------------------------------------------------------
# Internal insert helper
# ---------------------------------------------------------------------------

def _insert_feature(cursor, conn, schema, table, columns, col_values,
                    extra_values, dateiname, geom_wkt, log_func):
    """Build and execute a single INSERT statement.

    All plan-level extra fields (inkrafttretensDatum, nummer) are appended
    after the per-feature attribute columns.  The geometry is passed as WKT
    and converted to PostGIS geometry inside the SQL using ST_GeomFromText.

    A duplicate check on gml_id prevents re-importing the same feature when
    the plugin is run multiple times on the same directory.
    """
    gml_id = col_values.get("gml_id")

    # Skip if this gml_id already exists in the target table
    cursor.execute(
        f"SELECT 1 FROM {schema}.{table} WHERE gml_id = %s LIMIT 1",
        (gml_id,),
    )
    if cursor.fetchone() is not None:
        return "duplicate"

    all_columns = columns + ["inkrafttretensdatum", "dateiname", "bplan", "geom"]
    placeholders = ", ".join(["%s"] * (len(columns) + 3)) + ", ST_GeomFromText(%s, 25832)"

    sql = (
        f"INSERT INTO {schema}.{table} ({', '.join(all_columns)}) "
        f"VALUES ({placeholders})"
    )
    values = tuple(col_values[c] for c in columns) + (
        extra_values.get("inkrafttretensDatum"),
        dateiname,
        extra_values.get("nummer"),
        geom_wkt,
    )

    try:
        cursor.execute(sql, values)
        conn.commit()
        return "inserted"
    except Exception as exc:
        conn.rollback()
        if log_func:
            log_func(f"[FEHLER] INSERT fehlgeschlagen (gml_id={gml_id}): {exc}")
        return "error"


# ---------------------------------------------------------------------------
# Public processing functions
# ---------------------------------------------------------------------------

def process_single_layer(file_path, layer_name, layer_config, conn, schema, log_func):
    """Import all features of a single fixed-geometry GML layer into PostGIS.

    Parameters
    ----------
    file_path    : str  – absolute path to the GML file
    layer_name   : str  – OGR layer name (matches the XPlanung element name)
    layer_config : dict – entry from SINGLE_GEOMETRY_LAYERS
    conn         : psycopg2 connection
    schema       : str  – target database schema
    log_func     : callable – logging callback
    """
    layer = QgsVectorLayer(f"{file_path}|layername={layer_name}", layer_name, "ogr")
    if not layer.isValid():
        # Layer simply not present in this file – not an error
        return

    feature_count = layer.featureCount()
    if feature_count == 0:
        return

    log_func(f"  → {layer_name}: {feature_count} Features gefunden")

    source_crs = layer.crs()
    transform = (
        QgsCoordinateTransform(source_crs, TARGET_CRS, QgsProject.instance())
        if source_crs != TARGET_CRS
        else None
    )

    extra_values = {
        field: extract_gml_value(file_path, field, log_func)
        for field in layer_config["extra_fields"]
    }
    dateiname = os.path.splitext(os.path.basename(file_path))[0]
    existing_fields = set(layer.fields().names())
    target_type = layer_config["geometry_type"]
    columns = layer_config["columns"]
    table = layer_config["table"]

    inserted = 0
    skipped = 0
    duplicates = 0

    cursor = conn.cursor()

    for feature in layer.getFeatures():
        geom = feature.geometry()

        if transform and geom and not geom.isEmpty():
            geom.transform(transform)

        converted = convert_geometry(geom, target_type, log_func)
        if converted is None or converted.isEmpty():
            log_func(f"    [WARNUNG] Feature {feature.id()} übersprungen – Geometrie nicht konvertierbar")
            skipped += 1
            continue

        col_values = {
            col: convert_qvariant(feature.attribute(col)) if col in existing_fields else None
            for col in columns
        }

        result = _insert_feature(
            cursor, conn, schema, table, columns, col_values,
            extra_values, dateiname, converted.asWkt(), log_func,
        )
        if result == "inserted":
            inserted += 1
        elif result == "duplicate":
            duplicates += 1
        else:
            skipped += 1

    cursor.close()
    log_func(
        f"    [OK] {layer_name}: {inserted} eingefügt, "
        f"{duplicates} Duplikate übersprungen, {skipped} fehlerhaft"
    )


def process_multi_layer(file_path, base_layer_name, conn, schema, log_func):
    """Import features from a mixed-geometry GML layer.

    Features are read from the OGR layer identified by *base_layer_name*.
    Each feature's actual geometry type determines which suffixed target table
    (_po, _li, _py) receives the row.

    Parameters
    ----------
    file_path       : str  – absolute path to the GML file
    base_layer_name : str  – XPlanung base element name (e.g. "BP_Wegerecht")
    conn            : psycopg2 connection
    schema          : str  – target database schema
    log_func        : callable – logging callback
    """
    suffix_configs = MULTI_GEOMETRY_LAYERS[base_layer_name]

    layer = QgsVectorLayer(
        f"{file_path}|layername={base_layer_name}", base_layer_name, "ogr"
    )
    if not layer.isValid():
        return

    feature_count = layer.featureCount()
    if feature_count == 0:
        return

    log_func(f"  → {base_layer_name}: {feature_count} Features gefunden (gemischte Geometrie)")

    source_crs = layer.crs()
    transform = (
        QgsCoordinateTransform(source_crs, TARGET_CRS, QgsProject.instance())
        if source_crs != TARGET_CRS
        else None
    )

    # Extra fields are identical across all geometry variants – use any suffix
    any_config = next(iter(suffix_configs.values()))
    extra_values = {
        field: extract_gml_value(file_path, field, log_func)
        for field in any_config["extra_fields"]
    }
    dateiname = os.path.splitext(os.path.basename(file_path))[0]
    existing_fields = set(layer.fields().names())

    counters = {suffix: {"inserted": 0, "skipped": 0, "duplicates": 0} for suffix in suffix_configs}
    unsupported = 0

    cursor = conn.cursor()

    for feature in layer.getFeatures():
        geom = feature.geometry()

        if transform and geom and not geom.isEmpty():
            geom.transform(transform)

        geom_type_str = QgsWkbTypes.displayString(geom.wkbType()).upper()

        # Determine target suffix from the geometry type string
        if "POINT" in geom_type_str:
            suffix = "_po"
        elif "LINESTRING" in geom_type_str or "COMPOUNDCURVE" in geom_type_str:
            suffix = "_li"
        elif "POLYGON" in geom_type_str or "SURFACE" in geom_type_str:
            suffix = "_py"
        else:
            log_func(
                f"    [WARNUNG] Feature {feature.id()} übersprungen – "
                f"unbekannter Geometrietyp: {geom_type_str}"
            )
            unsupported += 1
            continue

        if suffix not in suffix_configs:
            # This geometry variant has no target table defined (e.g. _po for
            # BP_Immissionsschutz which only has _li and _py)
            continue

        cfg = suffix_configs[suffix]
        target_type = SUFFIX_TO_GEOMETRY_TYPE[suffix]

        converted = convert_geometry(geom, target_type, log_func)
        if converted is None or converted.isEmpty():
            log_func(
                f"    [WARNUNG] Feature {feature.id()} übersprungen – "
                f"Geometriekonvertierung fehlgeschlagen ({geom_type_str} -> {target_type})"
            )
            counters[suffix]["skipped"] += 1
            continue

        col_values = {
            col: convert_qvariant(feature.attribute(col)) if col in existing_fields else None
            for col in cfg["columns"]
        }

        result = _insert_feature(
            cursor, conn, schema, cfg["table"], cfg["columns"], col_values,
            extra_values, dateiname, converted.asWkt(), log_func,
        )
        if result == "inserted":
            counters[suffix]["inserted"] += 1
        elif result == "duplicate":
            counters[suffix]["duplicates"] += 1
        else:
            counters[suffix]["skipped"] += 1

    cursor.close()

    for suffix, c in counters.items():
        if c["inserted"] or c["duplicates"] or c["skipped"]:
            log_func(
                f"    [OK] {base_layer_name}{suffix}: {c['inserted']} eingefügt, "
                f"{c['duplicates']} Duplikate, {c['skipped']} fehlerhaft"
            )
    if unsupported:
        log_func(f"    [WARNUNG] {unsupported} Features mit nicht unterstütztem Geometrietyp übersprungen")
