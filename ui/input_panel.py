"""
Description: Right panel for entering values such as light intensity, temperature and voltage 
with input fields and dropdown.
Author(s): Mohammad Amman
Reviewed by: Salek MD PEASH BEEN, Thet Htar Zin
Date: 26 May 2025
Last Updated: 27 May 2025

"""

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QLineEdit, QGraphicsOpacityEffect, QComboBox
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

class InputPanel(QFrame):

    #Basically, start of the frontend design for the input panel.
    def __init__(self):
        super().__init__()
        self.setObjectName("inputPanel")
        self.setFrameStyle(QFrame.Shape.StyledPanel)
        
        self.setStyleSheet("""
        QFrame#inputPanel {
            background-color:rgba(121, 112, 174, 0.73);
        }
    """)
        
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Title
        title = QLabel("Enter the values")
        title.setFont(QFont("Poppins", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            color: #edf2f4;
            margin-bottom: 10px;
            border: none;
        """)
        layout.addWidget(title)
        
        # Dropdown menu with label
        dropdown_layout = QVBoxLayout()
        dropdown_layout.setSpacing(6)
        
        dropdown_label = QLabel("Time of Day")
        dropdown_label.setFont(QFont("Poppins", 14, QFont.Weight.Bold))
        dropdown_label.setStyleSheet("""
            color: #edf2f4;
            background-color: transparent;
            padding: 4px 0;
            border: none;
        """)
        dropdown_layout.addWidget(dropdown_label)
        
        self.time_dropdown = QComboBox()
        self.time_dropdown.addItems(["Dawn", "Morning", "Noon", "Afternoon", "Evening", "Night"])
        self.time_dropdown.setFont(QFont("Poppins", 14))
        self.time_dropdown.setStyleSheet("""
            QComboBox {
                background-color: #1e1e2e;
                color: #f5f5f5;
                border: 1px solid #3b3b4f;
                border-radius: 8px;
                padding: 10px 35px 10px 10px;
                font-size: 14pt;
            }
            QComboBox:hover {
                background-color: #2a2a3b;
                border: 1px solid #6366f1;
            }
            QComboBox::drop-down {
                border: none;
                width: 35px;
            }
            QComboBox::down-arrow {
                qproperty-text: "-";
                color: #f5f5f5;
                font-size: 16pt;
                font-family: Poppins;
                width: 12px;
                height: 12px;
            }
            QComboBox QAbstractItemView {
                background-color: #1e1e2e;
                color: #f5f5f5;
                selection-background-color: #6366f1;
                selection-color: #f5f5f5;
                border: 1px solid #3b3b4f;
                border-radius: 8px;
                padding: 8px;
            }
            QComboBox QSAbstractItemView::item {
                padding: 10px;
                min-height: 30px;
            }
        """)
        dropdown_layout.addWidget(self.time_dropdown)
        layout.addLayout(dropdown_layout)
        
        # Input fields
        self.light_input = self.create_input_field("Light Intensity (0 - 1000)", layout)
        self.temp_input = self.create_input_field("Temperature (Degree celcius)", layout)
        self.voltage_input = self.create_input_field("Voltage", layout)
        
        layout.addStretch()
        
    def create_input_field(self, label_text, layout):
        """Create a modern input field with label"""
        field_layout = QVBoxLayout()
        field_layout.setSpacing(6)
        
        label = QLabel(label_text)
        label.setFont(QFont("Poppins", 14, QFont.Weight.Bold))
        label.setStyleSheet("""
            color: #edf2f4;
            background-color: transparent;
            padding: 4px 0;
            font-size: 16px;  
            border: none;
        """)
        field_layout.addWidget(label)
        
        input_field = QLineEdit()
        input_field.setMinimumHeight(44)
        input_field.setFont(QFont("Poppins", 14))
        input_field.setStyleSheet("""
            QLineEdit {
                background-color: #3d405b;
                color: #edf2f4;
                border: 1px;
                border-radius: 8px;
                font-size: 16px;                  
                padding: 10px;
            }
            QLineEdit:hover {
                border: 1px solid #6366f1;
            }
            QLineEdit:focus {
                border: 1px solid #30E0B1;
                background-color: #4a4e69;
            }
        """)
        field_layout.addWidget(input_field)

        #Basically, the end of the frontend design for the input panel.
        
        layout.addLayout(field_layout)
        return input_field
    
    # Getters for input values of time of the day such as dawn, morning, noon, afternoon, evening and night
    def get_selected_time_of_day(self):
        return self.time_dropdown.currentText()

    # When the user selects a situation, this method is called to enable or disable the input panel and dropdown.
    # If "Enter values manually" is selected, the input panel and dropdown are enabled.
    # Otherwise, they are disabled and set to semi-transparent.
    def set_manual_mode(self, is_manual):
        """Enable/disable input panel and dropdown based on situation selection, with opacity effect."""
        self.setEnabled(is_manual)  # Disable inputs and dropdown functionality-wise
        self.time_dropdown.setEnabled(is_manual)  # Explicitly enable/disable dropdown
        
        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(1.0 if is_manual else 0.4)  # Fully visible or semi-transparent
        self.setGraphicsEffect(opacity_effect)
    