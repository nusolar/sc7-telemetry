import argparse
import canparse
import logging
import logging.handlers
import time
#TODO: from digi.xbee.devices import XBeeDevice

#Command-line arguments
#Note: 'const' is the default value when a flag is added.
#Note: 'default' is the default value when it's not.
parser = argparse.ArgumentParser(
    description='NUSolar telemetry program.',
)
parser.add_argument('--cantable',
    default='can-table.csv',
    metavar='TABLE.CSV',
    help='CAN table to reference.'
)
parser.add_argument('--fromfile',
    metavar='FILE',
    help='Read input from file. Useful for testing.'
)
parser.add_argument('-l', '--log',
    nargs='?',
    const='log.txt',
    metavar='LOGFILE',
    help='Log output to file.'
)
args = parser.parse_args()

if args.log is not None:
    logging.getLogger('can_packets').addHandler(
        logging.handlers.RotatingFileHandler(
            #TODO: Not sure how this behaves.
            #Further investigation needed.
            args.log, mode='w', maxBytes=5e8, backupCount=1
        )
    )
    logging.getLogger('can_packets').setLevel(logging.INFO)

if args.fromfile is not None:
    with open(args.fromfile) as input_file:
        can_parser = canparse.CANParser(args.cantable)
        for line in input_file:
            result = can_parser.parse(line)
            if args.log is not None:
                logging.getLogger('can_packets').info(result)
