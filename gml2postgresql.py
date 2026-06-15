# -*- coding: utf-8 -*-
"""
gml2postgresql.py – QGIS plugin entry point

Registers the plugin action in the QGIS toolbar and menu, and opens the
GML2PostgreSQLDialog when the action is triggered.
"""

import os

from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from .dialog import GML2PostgreSQLDialog


class Gml2PostgreSQL:
    """QGIS plugin class instantiated by classFactory() in __init__.py."""

    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.action = None

    def initGui(self):
        icon_path = os.path.join(self.plugin_dir, "icon.png")
        self.action = QAction(
            QIcon(icon_path),
            "GML2PostgreSQL",
            self.iface.mainWindow(),
        )
        self.action.setToolTip(
            "XPlanung-GML-Dateien in eine PostgreSQL/PostGIS-Datenbank importieren"
        )
        self.action.triggered.connect(self.run)

        self.iface.addPluginToMenu("&GML2PostgreSQL", self.action)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        if self.action:
            self.iface.removePluginMenu("&GML2PostgreSQL", self.action)
            self.iface.removeToolBarIcon(self.action)
            del self.action
            self.action = None

    def run(self):
        dialog = GML2PostgreSQLDialog(self.iface.mainWindow())
        dialog.exec_()
