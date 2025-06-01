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
git clone https://github.com/thethtarzin111/teknoware_hackathon.git
cd teknoware_hackathon (or path to your extracted zip file)

### 2. Create a virtual environment
python -m venv venv

### 3. Activate your virtual environment 
venv\Scripts\activate

### 4. Install dependencies
pip install -r requirements.txt

### 5. Run the application
python main.py

## Common Issues

### 1) MSSP Library Not Available
- Ensure that you've installed pyserial.
- Verify that tw_mssp.py and tw_fast_crc.py are in project root directory.

### 2) COM Port Connection Failed
- Check Device Manager for correct COM port.
- Ensure no other applications are using the port.
- Verify LCU is powered and connected.
- Try different COM ports (COM6, COM3, etc.)

### 3) Directory Error
- Make sure that virtual environment is created in the same directory as ui and assets folders.

## Authors
### Mohammad Amman - Lead Developer, UI Designer
### Salek Md Peash Been - Developer, Code Reviewer
### Thet Htar Zin - Developer, Code Reviewer


##  AI DECLARATION
This application was developed with the help of AI tools such as ChatGPT and Claude. They were used to understand the possible different real-life based scenarios such as tuneel and vandalism. It was also used to get UI design configurations. However, the code provided by the tools wasn't directly copied but rather modified based on our preference. It was also used to solve common issues such as directory error, dependencies installation and error finding. 
