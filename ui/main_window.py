"""
Description: This is main application window that merges all panels, manages layout
and handles the main logic of the sensor monitor application.
Author(s): Mohammad Amman, Thet Htar Zin
Reviewed by: Thet Htar Zin, Salek MD PEASH BEEN
Date: 26 May 2025
Last Updated: 27 May 2025

"""

# Import necessary modules for UI components
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt6.QtCore import QTimer
from .situation_panel import SituationPanel
from .render_panel import RenderPanel
from .output_panel import OutputPanel  # Enhanced with scenario responses
from .input_panel import InputPanel
from .view_input_panel import ViewInputPanel
from .styles import apply_main_style


class SensorMonitorMainWindow(QMainWindow):
    # Basically, the start of frontend design for the main window.
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Teknoware Sensor Simulator with LCU Integration")
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        
        # Create panels
        self.situation_panel = SituationPanel()
        self.render_panel = RenderPanel()
        self.output_panel = OutputPanel()  # Enhanced with scenario simulation
        self.input_panel = InputPanel()
        self.view_input_panel = ViewInputPanel()
        
        # Create center section (render + output panels)
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        center_layout.addWidget(self.render_panel)
        center_layout.addWidget(self.output_panel)
        
        # Create right section (input + view panels)
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.addWidget(self.input_panel)
        right_layout.addWidget(self.view_input_panel)
        
        # Add sections to main layout
        main_layout.addWidget(self.situation_panel)
        main_layout.addWidget(center_widget, 1)  # Give center more space
        main_layout.addWidget(right_widget)
        
        # Connect signals
        self.setup_connections()
        
        # Set up data update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_sensor_data)
        self.timer.start(2000)
        
        # Apply styling
        apply_main_style(self)
        button_style = """
            QPushButton {
                background-color: #372a84;
                color: white;
                border-radius: 40px;
                min-height: 60px;
                margin-top: 20px;
                padding: 10px;
                text-align: center;
                font-size: 18px;
                font-weight: bold;
                font-family: 'Poppins', Arial, sans-serif;
            }
            QPushButton:hover {
                background-color: #844cb9;
            }
            QPushButton:pressed {
                background-color: #4e32a7;
            }
        """
        
        # Enhanced SEND DATA button
        send_button = QPushButton("SEND DATA TO LCU")
        send_button.setStyleSheet(button_style)
        send_button.clicked.connect(self.send_data_to_lcu)
        
        right_layout.addWidget(send_button) 
    
    #Basically, the end of frontend design for the main window.

    # Enhanced method to send data to LCU and show responses
    def send_data_to_lcu(self):

        # Get current situation from situation panel
        current_situation = self.situation_panel.get_current_situation()
        intensities = [0, 50, 100, 150, 200, 250, 300, 400, 500, 600, 700, 800, 900, 1000]
        
        # Initialize default values
        light = 0
        temp = 0
        voltage = 0
        time_of_day = "Manual"
        
        # Set values based on the selected situation
        if current_situation == "Enter values manually":
            try:
                light = float(self.input_panel.light_input.text() or "400")
                temp = float(self.input_panel.temp_input.text() or "25")
                voltage = float(self.input_panel.voltage_input.text() or "5")
                time_of_day = self.input_panel.get_selected_time_of_day()
                
                # Update render panel for manual input
                closest_light = min(intensities, key=lambda x: abs(x - light))
                self.render_panel.update_image(time_of_day.lower(), int(closest_light))
                
            except ValueError:
                # Handle invalid input
                light = 400
                temp = 25
                voltage = 5
                time_of_day = "Manual"
                
        else:
            # Handle predefined scenarios with various visuals
            scenario_data = {
                "Train inside a tunnel": {
                    "light": 20, "temp": 21, "voltage": 5,
                    "image": "tunnel", "image_intensity": 1
                },
                "Under direct sunlight": {
                    "light": 1000, "temp": 30, "voltage": 5,
                    "image": "directsunlight", "image_intensity": 1
                },
                "Person blocking sensor": {
                    "light": 50, "temp": 25, "voltage": 3.3,
                    "image": "block", "image_intensity": 1
                },
                "Vandalizing Sensor": {
                    "light": 10, "temp": 22, "voltage": 3.3,
                    "image": "vandalism", "image_intensity": 1
                },
                "Flashing at the Sensor": {
                    "light": 950, "temp": 22, "voltage": 5,
                    "image": "flash", "image_intensity": 1
                },
                "Broken Sensor": {
                    "light": -1000, "temp": -999, "voltage": 0,
                    "image": "broken", "image_intensity": 1
                },
                "Train on fire": {
                    "light": 800, "temp": 80, "voltage": 3.3,
                    "image": "fire", "image_intensity": 1
                }
            }
            
            if current_situation in scenario_data:
                data = scenario_data[current_situation]
                light = data["light"]
                temp = data["temp"]
                voltage = data["voltage"]
                
                # Update render panel for scenario
                self.render_panel.update_image(data["image"], data["image_intensity"])
        
        # Update the view panel to show what was sent
        self.view_input_panel.update_display((str(light), str(temp), str(voltage)))
        
        # Send data to enhanced output panel for LCU simulation
        self.output_panel.process_scenario_data(
            scenario=current_situation,
            light=light,
            temp=temp,
            voltage=voltage,
            time_of_day=time_of_day
        )
        
        # Provide console feedback
        print(f"Sent to LCU: {current_situation}")
        print(f"Data: Light={light}, Temp={temp}°C, Voltage={voltage}V")
        
        if time_of_day != "Manual":
            print(f"Time: {time_of_day}")

    # Connect signals between panels
    def setup_connections(self):
        
        # Connect situation changes to input panel state
        self.situation_panel.situation_changed.connect(
            self.input_panel.set_manual_mode
        )
        
        self.situation_panel.situation_changed.connect(
            self.on_situation_changed
        )
        
    # Only handle situation changes when the button is pressed
    def on_situation_changed(self, is_manual):
        
        if not is_manual:
            # For predefined scenarios, only show preview data in view panel
            current_situation = self.situation_panel.get_current_situation()
            
            # Get scenario data for preview
            scenario_data = {
                "Train inside a tunnel": {"light": 20, "temp": 21, "voltage": 5},
                "Under direct sunlight": {"light": 1000, "temp": 30, "voltage": 5},
                "Person blocking sensor": {"light": 50, "temp": 25, "voltage": 3.3},
                "Vandalizing Sensor": {"light": 10, "temp": 22, "voltage": 3.3},
                "Flashing at the Sensor": {"light": 950, "temp": 22, "voltage": 5},
                "Broken Sensor": {"light": -1000, "temp": -999, "voltage": 0},
                "Train on fire": {"light": 800, "temp": 80, "voltage": 3.3}
            }
            
            if current_situation in scenario_data:
                data = scenario_data[current_situation]
                
                # Show preview in view panel
                self.view_input_panel.update_display((
                    str(data["light"]), 
                    str(data["temp"]), 
                    str(data["voltage"])
                ))
                
                # Clear LCU output and show waiting message
                self.output_panel.clear_outputs()
                self.output_panel.raw_output.append(f" Scenario selected: {current_situation}")
                self.output_panel.raw_output.append(" Preview data shown in 'Sent Data' panel")
                self.output_panel.raw_output.append(" Click 'SEND DATA TO LCU' to see LCU and TSA response")
                self.output_panel.processed_output.append(f" {current_situation}")
                self.output_panel.processed_output.append(" Waiting for send command...")
        else:
            # Manual mode - clear previous data and show manual input message
            self.view_input_panel.update_display(("", "", ""))
            self.output_panel.clear_outputs()
            self.output_panel.raw_output.append(" Manual input mode selected")
            self.output_panel.raw_output.append(" Enter values and click 'SEND DATA TO LCU'")
            self.output_panel.processed_output.append("  Manual mode active")
            self.output_panel.processed_output.append(" Waiting for input...")
        
    def update_sensor_data(self):
        """Update sensor data periodically"""
        self.output_panel.update_automatic_data()
        
    def closeEvent(self, event):
        """Clean up when closing the application"""
        # Stop the timer
        if hasattr(self, 'timer'):
            self.timer.stop()
        
        # Stop MSSP communication
        if hasattr(self.output_panel, 'mssp_thread') and self.output_panel.mssp_thread:
            self.output_panel.mssp_thread.stop()
            
        event.accept()