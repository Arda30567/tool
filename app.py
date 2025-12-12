#!/usr/bin/env python3
"""
Python Toolbox - Profesyonel Araç Seti
Tüm hakları saklıdır.
"""

import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from ui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    app.setApplicationName("Python Toolbox")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Python Toolbox")
    
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())