# -*- coding: utf-8 -*-
"""
dialog.py – QGIS dialog and background worker thread for GML2PostgreSQL

GML2PostgreSQLDialog  : Qt dialog that collects user input and displays the
                        processing log.
Worker                : QThread subclass that drives the import without
                        blocking the QGIS main thread.
"""

import os
from datetime import datetime

from PyQt5 import QtWidgets
from PyQt5.QtCore import QSettings, QThread, pyqtSignal
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox, QPushButton
from PyQt5.uic import loadUi

from .layer_config import MULTI_GEOMETRY_LAYERS, SINGLE_GEOMETRY_LAYERS
from .processing import connect_db, process_multi_layer, process_single_layer


# ---------------------------------------------------------------------------
# Background worker
# ---------------------------------------------------------------------------

class Worker(QThread):
    """Performs the GML import in a separate thread.

    Signals
    -------
    log_message      : str  – a single log line ready for display
    progress_updated : int  – current progress as a percentage (0–100)
    finished_signal  :      – emitted when the run() method returns
    """

    log_message = pyqtSignal(str)
    progress_updated = pyqtSignal(int)
    finished_signal = pyqtSignal()

    def __init__(self, directory, host, port, db_name, schema, user, password):
        super().__init__()
        self.directory = directory
        self.host = host
        self.port = port
        self.db_name = db_name
        self.schema = schema
        self.user = user
        self.password = password

    def run(self):
        # Collect all GML files in the selected directory (recursive)
        gml_files = [
            os.path.join(root, f)
            for root, _, files in os.walk(self.directory)
            for f in files
            if f.lower().endswith(".gml")
        ]

        if not gml_files:
            self.log_message.emit("Keine GML-Dateien im ausgewählten Verzeichnis gefunden.")
            self.finished_signal.emit()
            return

        self.log_message.emit(f"{len(gml_files)} GML-Datei(en) gefunden.")

        conn = connect_db(
            self.host, self.port, self.db_name,
            self.user, self.password,
            self.log_message.emit,
        )
        if conn is None:
            self.finished_signal.emit()
            return

        self.log_message.emit("Datenbankverbindung hergestellt.")

        total = len(gml_files)

        for index, file_path in enumerate(gml_files):
            filename = os.path.basename(file_path)
            self.log_message.emit(f"\nDatei {index + 1}/{total}: {filename}")

            # Mixed-geometry layers first (one OGR pass per base layer)
            for base_name in MULTI_GEOMETRY_LAYERS:
                process_multi_layer(file_path, base_name, conn, self.schema, self.log_message.emit)

            # Fixed-geometry layers
            for layer_name, layer_config in SINGLE_GEOMETRY_LAYERS.items():
                process_single_layer(
                    file_path, layer_name, layer_config,
                    conn, self.schema, self.log_message.emit,
                )

            self.progress_updated.emit(int((index + 1) / total * 100))

        conn.close()
        self.log_message.emit("\nVerarbeitung abgeschlossen.")
        self.finished_signal.emit()


# ---------------------------------------------------------------------------
# Dialog
# ---------------------------------------------------------------------------

class GML2PostgreSQLDialog(QDialog):
    """Main plugin dialog.

    Provides input fields for the GML folder and database connection
    parameters, a log area showing processing output, a Run button that
    launches the Worker thread, and a Save Log button to export the log
    to a timestamped text file.

    Connection settings (excluding the password) are persisted via
    QSettings between sessions.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi(os.path.join(os.path.dirname(__file__), "form.ui"), self)

        self.setWindowTitle("GML2PostgreSQL")
        self._setup_ui()
        self._load_settings()

        self.worker = None

    # ------------------------------------------------------------------
    # UI setup
    # ------------------------------------------------------------------

    def _setup_ui(self):
        self.lineEdit.setPlaceholderText("Ordner mit GML-Dateien auswählen ...")
        self.hostInput.setPlaceholderText("z. B. localhost")
        self.portInput.setPlaceholderText("z. B. 5432")
        self.dbNameInput.setPlaceholderText("Datenbankname")
        self.schemaInput.setPlaceholderText("Schemaname")
        self.userInput.setPlaceholderText("Datenbankbenutzer")
        self.passwordInput.setPlaceholderText("Passwort")
        self.passwordInput.setEchoMode(QtWidgets.QLineEdit.Password)

        self.pushButton.clicked.connect(self._browse_directory)

        run_button = self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok)
        run_button.setText("Starten")
        # Disconnect the default accept() slot so we can run the worker instead
        run_button.clicked.disconnect()
        run_button.clicked.connect(self._start_processing)

        self.buttonBox.rejected.connect(self.reject)

        self.logArea.setReadOnly(True)
        self.logArea.setPlaceholderText("Verarbeitungsprotokoll ...")

        # Add Save Log button to the button box
        self._save_log_button = QPushButton("Log speichern")
        self._save_log_button.setEnabled(False)
        self.buttonBox.addButton(self._save_log_button, QtWidgets.QDialogButtonBox.ActionRole)
        self._save_log_button.clicked.connect(self._save_log)

    # ------------------------------------------------------------------
    # Slots
    # ------------------------------------------------------------------

    def _browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Ordner auswählen")
        if directory:
            self.lineEdit.setText(directory)

    def _start_processing(self):
        directory = self.lineEdit.text().strip()
        if not directory:
            QMessageBox.warning(self, "Eingabe fehlt", "Bitte einen GML-Ordner auswählen.")
            return

        host = self.hostInput.text().strip()
        port = self.portInput.text().strip()
        db_name = self.dbNameInput.text().strip()
        schema = self.schemaInput.text().strip()
        user = self.userInput.text().strip()
        password = self.passwordInput.text()

        if not all([host, port, db_name, schema, user, password]):
            QMessageBox.warning(
                self,
                "Eingabe unvollständig",
                "Bitte alle Datenbankverbindungsparameter ausfüllen.",
            )
            return

        self._save_settings()
        self.logArea.clear()
        self._save_log_button.setEnabled(False)
        self._set_ui_enabled(False)

        self.worker = Worker(directory, host, port, db_name, schema, user, password)
        self.worker.log_message.connect(self._append_log)
        self.worker.finished_signal.connect(self._on_finished)
        self.worker.start()

    def _append_log(self, message):
        self.logArea.append(message)
        self.logArea.ensureCursorVisible()

    def _on_finished(self):
        self._set_ui_enabled(True)
        self._save_log_button.setEnabled(True)
        self.worker = None

    def _save_log(self):
        log_content = self.logArea.toPlainText().strip()
        if not log_content:
            QMessageBox.information(self, "Log leer", "Es gibt keinen Loginhalt zum Speichern.")
            return

        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        default_filename = f"log_{timestamp}.txt"

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Log speichern",
            default_filename,
            "Textdateien (*.txt);;Alle Dateien (*)",
        )

        if not file_path:
            return  # User cancelled

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(log_content)
            QMessageBox.information(
                self,
                "Log gespeichert",
                f"Log wurde gespeichert unter:\n{file_path}",
            )
        except Exception as exc:
            QMessageBox.critical(
                self,
                "Fehler beim Speichern",
                f"Log konnte nicht gespeichert werden:\n{exc}",
            )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _set_ui_enabled(self, enabled):
        run_button = self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok)
        if run_button:
            run_button.setEnabled(enabled)
        self.logArea.setEnabled(enabled)
        self.pushButton.setEnabled(enabled)

    def _load_settings(self):
        s = QSettings("Stadt Wilhelmshaven", "gml2postgresql")
        self.lineEdit.setText(s.value("directory", ""))
        self.hostInput.setText(s.value("host", ""))
        self.portInput.setText(s.value("port", "5432"))
        self.dbNameInput.setText(s.value("db_name", ""))
        self.schemaInput.setText(s.value("schema", ""))
        self.userInput.setText(s.value("user", ""))

    def _save_settings(self):
        s = QSettings("Stadt Wilhelmshaven", "gml2postgresql")
        s.setValue("directory", self.lineEdit.text())
        s.setValue("host", self.hostInput.text())
        s.setValue("port", self.portInput.text())
        s.setValue("db_name", self.dbNameInput.text())
        s.setValue("schema", self.schemaInput.text())
        s.setValue("user", self.userInput.text())
        # Password is intentionally not persisted


