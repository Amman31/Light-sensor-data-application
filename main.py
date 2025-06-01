"""
Description: Main entry point that launches our sensor monitor application.
Author(s): Mohammad Amman
Reviewed by: Salek MD PEASH BEEN, Thet Htar Zin
Date: 26 May 2025
Last Updated: 26 May 2025

"""
import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import SensorMonitorMainWindow

def main():
    app = QApplication(sys.argv)
    window = SensorMonitorMainWindow()
    window.showMaximized() 
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
