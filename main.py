import logging
from receiver import Receiver

#Logger setup
logger_name = 'receiver'
logging.getLogger(logger_name).addHandler(
    logging.FileHandler('log.txt', mode='w'))
logging.getLogger(logger_name).setLevel(logging.INFO)

#Receive packets
receiver = Receiver()
for packet in receiver.get_packets_from_file('examples/live_capture.txt'):
    logging.getLogger(logger_name).info(packet)
