# Teknoware Sensor Simulator with LCU Integration

We developed a PyQt6-based GUI application utilizing python language to simulate various conditions and situations using TSA0002 light sensors. Our application provides real-time MSSP (Master-Slave Serial Protocol) communication with LCU (Lighting Control Unit) provided by Teknoware. This simulator imitates real life scenarios and is solely for testing puroses. 

## Features
**1) Real-time MSSP Communication**
Implements full TSA0002 sensor protocol communication with LCU

**2) Multiple Scenario Simulation**
Offers predefined scenarios including tunnel, direct sunlight, sensor blocking, vandalism, and emergency situations such as fire outbreak.

**3) Manual Input Mode**
Apart from predefined scenarios, user can give their own manual sensor value input together with time-of-day selection.

**4) Visual Environment Rendering**
Our application offers intuitive and dynamic background images that change based on user's selected scenarios.

**5) Live Data Monitoring**
User can see real-time display of TSA sensor responses and LCU communication.

## Note
- The main backend library for communicating with the sensor is not provided because of NDA

## Communication and Responses
- MSSP protocol support
- TSA0002 device info responses such as identification and specification
- Light Value Responses
- Raw Message Display
- Error Handling

## Requirements
### System & Hardware Requirements
- Python 3.8 or higher (Preferably python 3.11+ to avoid bugs and errors)
- Windows/Linux/macOS
- Available COM/Serial port for LCU communication
- Teknoware LCU unit

### Python Dependencies
- pip install PyQt6 pyserial cobs
- pip install pyserial

## Installation
### 1. Clone the repository

### 2. Create a virtual environment
python -m venv venv

### 3. Activate your virtual environment 
venv\Scripts\activate

### 4. Install dependencies
pip install -r requirements.txt

### 5. Run the application
python main.py

## Authors
### Mohammad Amman - Lead Developer, UI Designer
### Salek Md Peash Been - Developer, Code Reviewer
### Thet Htar Zin - Developer, Code Reviewer
