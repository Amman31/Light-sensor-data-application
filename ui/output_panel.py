"""
Description: Display area for raw and processed sensor data with MSSP communication to LCU.
Author(s): Mohammad Amman, Thet Htar Zin
Reviewed by: Thet Htar Zin, Salek MD PEASH BEEN
Date: 26 May 2025
Last Updated: 27 May 2025

"""

# Import necessary modules for UI components
from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
    QPushButton, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont
import time
import struct
from datetime import datetime
import random


MSSP_AVAILABLE = False
mssp_error = None

try:
    import sys
    import os
    # We're using tw_mssp.py library given to us.
    # So, we add current directory to path for that file.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    
    MSSP_AVAILABLE = True
    print("✅ MSSP library loaded successfully!")
except Exception as e:
    mssp_error = str(e)
    MSSP_AVAILABLE = False
    print(f"❌ MSSP library failed to load: {e}")

# This thread handles the MSSP communication with the LCU (Light Control Unit).
class MSSPCommunicationThread(QThread):
    message_received = pyqtSignal(str, str, str)  # raw_msg, ctrl_info, response_info
    error_occurred = pyqtSignal(str)
    
    def __init__(self, com_port="COM7", baud_rate=9600):
        super().__init__()
        self.com_port = com_port
        self.baud_rate = baud_rate
        self.mssp = None
        self.running = False
        self.current_light_value = 100
        self.current_temp_value = 25
        self.current_voltage_value = 5
        
    # Initialize the MSSP communication
    def initialize_mssp(self):
        
        try:
            # We import here to avoid issues with main thread
            from tw_mssp import Mssp, Mssp_message, MASTER_BIT
            self.Mssp = Mssp
            self.Mssp_message = Mssp_message  
            self.MASTER_BIT = MASTER_BIT
            self.mssp = Mssp(self.com_port, self.baud_rate, 5, True)
            return True
        
        except Exception as e:
            self.error_occurred.emit(f"Failed to initialize MSSP: {str(e)}")
            return False
    
    # Update sensor values that will be sent to LCU
    def update_sensor_values(self, light, temp, voltage):
        self.current_light_value = int(light)
        self.current_temp_value = int(temp)
        self.current_voltage_value = int(voltage)
    
    # This is the main communication loop that runs in a separate thread.
    def run(self):

        if not self.initialize_mssp():
            return
            
        self.running = True
        self.message_received.emit(" MSSP Communication Started", "", f"Listening on {self.com_port} at {self.baud_rate} baud")
        
        while self.running:
            try:
                # Get message from LCU (this will block until message received or timeout)
                msg = self.mssp.get_msg()
                
                # Check if we got a valid message
                if msg is None or len(msg) < 4:
                    continue
                    
                ctrl = msg.get_ctrl()
                timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                
                # Process the message
                raw_msg = f"[{timestamp}]  Message: {msg.hex()}" # Convert to hex string for display
                ctrl_info = f"[{timestamp}] Control: 0x{ctrl:02X}"
                
                # Extract command and address
                addr = int(msg[2])
                cmd = int(msg[3])
                
                response_info = f"[{timestamp}]  Addr: 0x{addr:02X}, Cmd: 0x{cmd:02X}"
                
                # We tried to follow RespExample and implement process commands
                if cmd == self.mssp.MSG_GET_LIGHT_VALUE_REQ:
                    self.handle_light_value_request(msg, ctrl, timestamp)
                elif cmd == self.mssp.MSG_DEVICE_INFO_REQ:
                    self.handle_device_info_request(msg, ctrl, timestamp)
                else:
                    response_info += f"\n[{timestamp}]  Command: 0x{cmd:02X}"
                
                self.message_received.emit(raw_msg, ctrl_info, response_info)
                
            except Exception as e:
                if self.running:  # Only show error if we're still supposed to be running
                    self.error_occurred.emit(f"Communication error: {str(e)}")
                    time.sleep(1)  # Wait before retrying
    
    # Handle specific requests from LCU
    def handle_light_value_request(self, msg, ctrl, timestamp):
        
        try:
            # Prepare response with current sensor values 
            light_raw = self.current_light_value
            light_avg = self.current_light_value + random.randint(-5, 5)  # Small variation
            light_last = self.current_light_value
            
            # Create response message based on RespExample.py 
            ctrl = ctrl & ~self.MASTER_BIT  # Flip bit 6, keep rest of mask same
            message = self.mssp.create_msg_get_light_value_resp(light_raw, light_avg, light_last)
            message.set_addr(self.mssp.LIGHT_SENSOR_ADDRESS)
            message.set_ctrl(ctrl)
            
            # Send response
            self.mssp.send_msg(message)
            
            response_info = f"[{timestamp}] ✅ Light Value Response Sent"
            response_info += f"\n[{timestamp}]  Raw: {light_raw}, Avg: {light_avg}, Last: {light_last}"
            
            self.message_received.emit("", "", response_info)
            
        except Exception as e:
            self.error_occurred.emit(f"Error handling light request: {str(e)}")
    
    # Handle device info request from LCU based on RespExample.py
    def handle_device_info_request(self, msg, ctrl, timestamp):
        
        try:
            # Device info for TSA0002 sensor (reference from RespExample.py)
            devType = 4096  # 0x00001000 Light sensor – TSA0002x (LSB format)
            devId = 65535
            fw = 16842753
            addr = self.mssp.LIGHT_SENSOR_ADDRESS
            group = 254  # 0xFE
            
            # Create response message (reference from RespExample.py)
            ctrl = ctrl & ~self.MASTER_BIT  # Flip bit 6, keep rest of mask same
            message = self.mssp.create_msg_device_info_resp(devType, devId, fw, addr, group)
            message.set_addr(self.mssp.LIGHT_SENSOR_ADDRESS)
            message.set_ctrl(ctrl)
            
            # Send response
            self.mssp.send_msg(message)
            
            response_info = f"[{timestamp}] ✅ Device Info Response Sent"
            response_info += f"\n[{timestamp}]  Type: {devType}, ID: {devId}, FW: {fw}"
            
            self.message_received.emit("", "", response_info)
            
        except Exception as e:
            self.error_occurred.emit(f"Error handling device info request: {str(e)}")
    
    # Stop the communication thread
    def stop(self):
        self.running = False
        self.quit()
        self.wait()


class OutputPanel(QFrame):

    # Basically, the start of frontend UI design.
    def __init__(self):
        super().__init__()
        self.setObjectName("outputPanel")
        self.setFrameStyle(QFrame.Shape.StyledPanel)
        self.mssp_thread = None
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)

        # Raw output section - 70%
        raw_frame = self.create_raw_output_section()
        raw_frame.setStyleSheet("border: none;")
        raw_frame.setMinimumWidth(400)
        layout.addWidget(raw_frame, 7)

        # Processed output section - 20%
        processed_frame = self.create_processed_output_section()
        processed_frame.setStyleSheet("border: none;")
        processed_frame.setMaximumWidth(350)
        layout.addWidget(processed_frame,3)

    def create_raw_output_section(self):
        raw_frame = QFrame()
        raw_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        raw_layout = QVBoxLayout(raw_frame)

        raw_title = QLabel("Raw MSSP Output")
        raw_title.setFont(QFont("Poppins", 12, QFont.Weight.Bold))
        raw_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        raw_title.setStyleSheet("color: white;")
        raw_layout.addWidget(raw_title)

        self.raw_output = QTextEdit()
        self.raw_output.setFont(QFont("Consolas", 9))
        self.raw_output.setStyleSheet(
            "background-color: #1e1e1e; color: #d4d4d4; border: 2px solid #3583d0; padding: 3px;"
        )
        self.raw_output.setReadOnly(True)
        self.raw_output.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByKeyboard | 
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        
        # Initial message
        if MSSP_AVAILABLE:
            self.raw_output.setPlainText(
                " TSA0002 Sensor Simulator Ready\n"
                " MSSP Library Loaded Successfully\n"
                " Click 'SEND DATA TO LCU' to start communication\n"
                " Select scenario or enter manual data first"
            )
        else:
            self.raw_output.setPlainText(
                "❌ MSSP Library Not Available\n"
                f"Error: {mssp_error}\n"
                "Running in simulation mode\n"
                "Install tw_mssp library for real communication"
            )
        
        raw_layout.addWidget(self.raw_output)
        return raw_frame

    def create_processed_output_section(self):
        processed_frame = QFrame()
        processed_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        processed_layout = QVBoxLayout(processed_frame)

        processed_title = QLabel("LCU Communication Status")
        processed_title.setFont(QFont("Poppins", 12, QFont.Weight.Bold))
        processed_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        processed_title.setStyleSheet("color: white;")
        processed_layout.addWidget(processed_title)

        self.processed_output = QTextEdit()
        self.processed_output.setReadOnly(True)
        self.processed_output.setFont(QFont("Poppins", 9))
        self.processed_output.setStyleSheet(
            "background-color: #1e1e1e; color: #d4d4d4; border: 2px solid #3583d0; padding: 3px;"
        )
        
        if MSSP_AVAILABLE:
            self.processed_output.setPlainText(
                "MSSP Communication Ready\n"
                "Status: Waiting\n"
                "Port: COM7 (default)\n"
                "Sensor responses ready"
            )
        else:
            self.processed_output.setPlainText(
                "MSSP Not Available\n"
                "Check COM port connection"
            )
        
        processed_layout.addWidget(self.processed_output)

        # Clear button
        clear_button = QPushButton("Clear All")
        clear_button.setCursor(Qt.CursorShape.PointingHandCursor)
        clear_button.setStyleSheet("""
            QPushButton {
                background-color: #372a84;
                color: white;
                border: none;
                border-radius: 6px;
                min-width: 100;
                margin-top: 5px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2c6cab;
            }
        """)
        clear_button.clicked.connect(self.clear_outputs)
        
        # Stop communication button
        stop_button = QPushButton("Stop")
        stop_button.setCursor(Qt.CursorShape.PointingHandCursor)
        stop_button.setStyleSheet("""
            QPushButton {
                background-color: #d35400;
                color: white;
                border: none;
                border-radius: 6px;
                min-width: 100px;
                margin-top: 5px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e67e22;
            }
        """)
        stop_button.clicked.connect(self.stop_communication)

        button_layout = QHBoxLayout()
        button_layout.addWidget(clear_button)
        button_layout.addWidget(stop_button)
        processed_layout.addLayout(button_layout)

        return processed_frame
    
    # Basically, the end of frontend UI design.

    # Process scenario data and start MSSP communication
    def process_scenario_data(self, scenario, light, temp, voltage, time_of_day=None):
        if not MSSP_AVAILABLE:
            self.show_simulation_fallback(scenario, light, temp, voltage, time_of_day)
            return
        
        # Stop any existing communication
        if self.mssp_thread and self.mssp_thread.isRunning():
            self.mssp_thread.stop()
        
        # Clear previous output
        self.clear_outputs()
        
        # Create and start MSSP communication thread
        self.mssp_thread = MSSPCommunicationThread()
        self.mssp_thread.message_received.connect(self.on_mssp_message_received)
        self.mssp_thread.error_occurred.connect(self.on_mssp_error)
        
        # Update sensor values in the thread
        self.mssp_thread.update_sensor_values(light, temp, voltage)
        
        # Start communication
        self.mssp_thread.start()
        
        # Show initial info
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        self.raw_output.append(f"[{timestamp}] Starting MSSP Communication")
        self.raw_output.append(f"[{timestamp}] Scenario: {scenario}")
        self.raw_output.append(f"[{timestamp}] Light: {light} lux")
        self.raw_output.append(f"[{timestamp}] Temperature: {temp}°C")
        self.raw_output.append(f"[{timestamp}] Voltage: {voltage}V")
        self.raw_output.append(f"[{timestamp}] Waiting for LCU messages...")
        
        self.processed_output.clear()
        self.processed_output.append("MSSP Communication Active")
        self.processed_output.append(f"Scenario: {scenario}")
        self.processed_output.append(f"Light: {light} lux")
        self.processed_output.append("Listening for LCU...")

    # Handle received MSSP messages and update outputs
    def on_mssp_message_received(self, raw_msg, ctrl_info, response_info):
        if raw_msg:
            self.raw_output.append(raw_msg)
        if ctrl_info:
            self.raw_output.append(ctrl_info)
        if response_info:
            self.raw_output.append(response_info)
            
        # Update status when successful response is sent
        if "Light Value Response Sent" in response_info:
            self.processed_output.append("Success! Light data sent to LCU")
        elif "Device Info Response Sent" in response_info:
            self.processed_output.append("Success! Device info sent to LCU")
            
        self.scroll_to_bottom()

    # Handle MSSP communication errors
    def on_mssp_error(self, error_message):
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        self.raw_output.append(f"[{timestamp}] ERROR: {error_message}")
        self.processed_output.append(f" Error: {error_message}")
        self.scroll_to_bottom()

    # Show simulation fallback when MSSP is not available
    def show_simulation_fallback(self, scenario, light, temp, voltage, time_of_day):
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        self.raw_output.clear()
        self.raw_output.append(f"[{timestamp}]  MSSP Simulation Mode")
        self.raw_output.append(f"[{timestamp}]  Scenario: {scenario}")
        self.raw_output.append(f"[{timestamp}]  Light: {light} lux")
        self.raw_output.append(f"[{timestamp}]   Temperature: {temp}°C")
        self.raw_output.append(f"[{timestamp}]  Voltage: {voltage}V")
        self.raw_output.append(f"[{timestamp}]  tw_mssp library not available")
        self.raw_output.append(f"[{timestamp}]  Install library for real communication")
        
        self.processed_output.clear()
        self.processed_output.append(" Simulation Mode")
        self.processed_output.append(f" {scenario}")
        self.processed_output.append(f" Light: {light} lux")
        self.processed_output.append(" MSSP library required")

    # Stop MSSP communication when user clicks stop button
    # Otherwise, it will run until user closes the application.
    def stop_communication(self):
        if self.mssp_thread and self.mssp_thread.isRunning():
            self.mssp_thread.stop()
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            self.raw_output.append(f"[{timestamp}] 🛑 Communication stopped by user")
            self.processed_output.append("🛑 Communication stopped")

    # Placeholder for automatic data updates (if needed in future)
    def update_automatic_data(self):
    
        pass

    # Scroll both outputs to the bottom
    def scroll_to_bottom(self):
        self.raw_output.verticalScrollBar().setValue(
            self.raw_output.verticalScrollBar().maximum()
        )
        self.processed_output.verticalScrollBar().setValue(
            self.processed_output.verticalScrollBar().maximum()
        )

    # Clear both output areas
    def clear_outputs(self):
        self.raw_output.clear()
        self.processed_output.clear()
        if MSSP_AVAILABLE:
            self.raw_output.append(" Communication log cleared")
            self.processed_output.append(" Ready for communication")
        else:
            self.raw_output.append(" Cleared - MSSP not available")
            self.processed_output.append(" Cleared - Simulation mode")
    
    # Handle window close event to stop MSSP thread
    def closeEvent(self, event):
        if self.mssp_thread and self.mssp_thread.isRunning():
            self.mssp_thread.stop()
        event.accept()