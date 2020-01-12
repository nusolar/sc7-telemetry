import canparse
import logging
import logging.handlers
import time
import serial
from typing import Callable

class Receiver:
    """Receives & decodes CAN packets from a radio transmitter."""
    def __init__(self,
        can_table: str = 'can-table.csv',
        log_file: str = 'log.txt',
        serial_port: str = '/dev/ttyUSB0',
        baud_rate: int = 57600):
        #Initialize fields
        self.can_table = can_table
        self.log_file = log_file
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        #Logging setup
        logging.getLogger('can_receiver').addHandler(
            logging.handlers.RotatingFileHandler(
                #TODO: Not completely sure how this behaves.
                self.log_file, mode='w', maxBytes=5e8, backupCount=1))
        logging.getLogger('can_receiver').setLevel(logging.INFO)

    def get_packet(self) -> iter:
        """Generates CAN Packets."""
        with serial.Serial(self.serial_port, self.baud_rate) as receiver:
            can_parser = canparse.CANParser(self.can_table)
            while(True):
                raw = receiver.read_until(b'\n').decode()
                packet = can_parser.parse(raw)
                logging.getLogger('can_receiver').info(packet)
                packet['time'] = time.time()
                yield packet

    def get_packet_from_file(self, input_file: str) -> iter:
        """Generates CAN packets from file. Useful for testing."""
        with open(input_file) as input_file:
            can_parser = canparse.CANParser(self.can_table)
            for line in input_file:
                packet = can_parser.parse(line)
                logging.getLogger('can_receiver').info(packet)
                packet['time'] = time.time()
                yield packet
