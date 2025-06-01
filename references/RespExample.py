from tw_mssp import Mssp
from tw_mssp import MASTER_BIT

#Init the Mssp library
#COM can change so check dev manager
#9600 is the baud (found on TSA0002 spec)
#Timeout is not that important
#RS485 mode true (or interestingly false, seems like both work)
mssp = Mssp("COM7", 9600, 5, True)

while True:
    #Get the message from COM port
    msg = mssp.get_msg()
    ctrl = msg.get_ctrl()
    print("Msg:", msg, "Ctrl:",ctrl) 
    #See Table 5. Explanation of the frame structure of MSSP spec
    ctrl = ctrl & ~MASTER_BIT #Only bit 6 needs to be flipped and rest of the mask kept the same (Nobody likes binary operators)
    #Address
    add = int(msg[2])
    #cmd is the command we need to respond to
    cmd = int(msg[3])
    #We need to check the incoming command so that we know what to use to respond to it
    #Read the spec to know what the required response contents are
    if (cmd == mssp.MSG_GET_LIGHT_VALUE_REQ):
        light_raw = 100
        light_avg = 110
        light_last = 100
        #Create and pack the message
        message = mssp.create_msg_get_light_value_resp(light_raw, light_avg, light_last)
        message.set_addr(mssp.LIGHT_SENSOR_ADDRESS)
        message.set_ctrl(ctrl)
        mssp.send_msg(message)

    elif (cmd == mssp.MSG_DEVICE_INFO_REQ):
        #See Table 8. Currently decided addresses
        #devTypeBytes = bytearray(b'\x00\x10\x00\x00') #0x00001000 Light sensor – TSA0002x (Remember LSB)
        #devType = int.from_bytes(devTypeBytes, byteorder='little', signed=False) #Set devtype to TSA
        #NOTE! What is 0x00001000 as an LSB formatted int? Calculate it OR Maybe this is one of those AI questions
        devType = 4096
        devId = 65535
        fw = 16842753
        addr = mssp.LIGHT_SENSOR_ADDRESS 
        group = 254 #See Table 7. Slave / slave group address definitions. 254 = 0xFE
        message = mssp.create_msg_device_info_resp(devType, devId, fw, addr, group)
        message.set_addr(mssp.LIGHT_SENSOR_ADDRESS)
        message.set_ctrl(ctrl)  # add control byte to response
        mssp.send_msg(message)