"""
Description: Left panel for selecting sensor situations with radio buttons.
Author(s): Mohammad Amman
Reviewed by: Thet Htar Zin, Salek MD PEASH BEEN
Date: 26 May 2025
Last Updated: 27 May 2025

"""
#import necessary modules for UI components
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QRadioButton, QButtonGroup, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class SituationPanel(QFrame):
    situation_changed = pyqtSignal(bool)  # True if manual mode
    
    def __init__(self):
        super().__init__()
        self.setObjectName("situationPanel")
        self.setFrameStyle(QFrame.Shape.StyledPanel)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Style customization for title
        title = QLabel("Select one of the simulations")
        title.setFont(QFont("Poppins", 12, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: white; margin-bottom: 30px;")
        layout.addWidget(title)

        # Style for box selectors
        box_style = """
            QPushButton {
                background-color: #ffffff;
                color: black;
                border: 2px ;
                border-radius: 8px;
                padding: 10px;
                margin-bottom: 10px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #844cb9;
                color: white;
            }
            QPushButton:checked {
                background-color: #4e32a7;
                color: white;
                border: 2px ;
            }
        """

        self.button_group = QButtonGroup()
        self.button_group.setExclusive(True)  # Only one button checked at a time

        self.situations = [
            "Enter values manually",
            "Train inside a tunnel", 
            "Under direct sunlight",
            "Person blocking sensor",
            "Vandalizing Sensor",
            "Flashing at the Sensor",
            "Broken Sensor",
            "Train on fire"
        ]

        # Loop through each situation and create a corresponding clickable button
        for i, situation in enumerate(self.situations):
            box = QPushButton(situation)
            box.setCheckable(True)
            box.setStyleSheet(box_style)
            box.setFont(QFont("Poppins", 10))
            if i == 0:
                box.setChecked(True)    # Set the first button as checked by default
            self.button_group.addButton(box, i)
            layout.addWidget(box)

        self.button_group.buttonClicked.connect(self.on_situation_changed)
        layout.addStretch()
        
    #This method is called when a situation button is clicked.    
    def on_situation_changed(self, button):
        button_id = self.button_group.id(button)
        is_manual = button_id == 0
        self.situation_changed.emit(is_manual)

    # This method returns the currently selected situation based on the button group.    
    def get_current_situation(self):
        current_id = self.button_group.checkedId()
        return self.situations[current_id] if current_id >= 0 else None
