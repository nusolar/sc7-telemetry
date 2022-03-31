from curses import baudrate
from digi.xbee.devices import XBeeDevice

serial_port = "COM5"
baud_rate = 57600
DATA_TO_SEND = "4th floor" 
REMOTE_NODE_ID = "Router"

device = XBeeDevice(serial_port, baud_rate)

device.open()

xbee_network = device.get_network()

remote = xbee_network.discover_device(REMOTE_NODE_ID)

if remote is None:
    print("Coudn't do it.")
    exit(1)

print("Sending data to %s >> %s..." % (remote.get_64bit_addr(), DATA_TO_SEND))

device.send_data(remote, DATA_TO_SEND)

device.close()
#COM5 - 57600/8/N/1/N - AT