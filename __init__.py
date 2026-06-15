# -*- coding: utf-8 -*-
"""
GML2PostgreSQL – QGIS Plugin

Importiert ausgewählte XPlanung-Objektarten aus GML-Dateien in eine
vorhandene PostgreSQL/PostGIS-Datenbank.

Entwickelt von der Stadt Wilhelmshaven – Geoinformationsverarbeitung und
Stadtentwicklung (GVS), 2025.
"""


def classFactory(iface):
    from .gml2postgresql import Gml2PostgreSQL
    return Gml2PostgreSQL(iface)
