
"""
Description: This is the small view panel that displays the last sent data values 
such as light intensity, temperature, and voltage.
Author(s): Mohammad Amman
Reviewed by: Thet Htar Zin, Salek MD PEASH BEEN
Date: 26 May 2025
Last Updated: 26 May 2025

"""

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class ViewInputPanel(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("viewInputPanel")
        self.setFrameStyle(QFrame.Shape.StyledPanel)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        
        # Title
        title = QLabel("Sent Data")
        title.setFont(QFont("Poppins", 11, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            color: #edf2f4;
            border: none;
        """)
        layout.addWidget(title)
        
        # Data display
        self.data_display = QLabel("No data has been sent")
        self.data_display.setFont(QFont("Poppins", 11))
        self.data_display.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.data_display.setStyleSheet("""
            color: #f5f5f5;
            background-color: #1e1e1e;
            border: 1px solid #5c6370;
            min-height: 80px;
            border-radius: 8px;
            padding: 5px 10px 0px 10px;
        """)
        layout.addWidget(self.data_display)
        
        layout.addStretch()
        
    def update_display(self, data):
        """Update the data display with new values"""
        light, temp, voltage = data
        self.data_display.setText(
            f"Light Intensity: {light}\n"
            f"Temperature: {temp} degree\n"
            f"Voltage: {voltage} V"
        )