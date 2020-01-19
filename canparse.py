import csv

class CANParser:
    def __init__(self, table_file: str):
        """Initialize a lookup dictionary from a CSV file."""
        self.table = {}
        with open(table_file) as table_file:
            csv_reader = csv.DictReader(table_file)
            for row in csv_reader:
                self.table[int(row['ID'], 16)] = row
                del self.table[int(row['ID'], 16)]['ID']
    def parse(self, message: str) -> dict:
        """
        Take a CAN message in hexadecimal
        and return a dictionary of values.
        """
        #First character not hex => Remove it
        if ord(message[0]) not in range(48, 58) \
            and ord(message[0]) not in range(65, 71) \
            and ord(message[0]) not in range(97, 103):
            message = message[1:]
        #Parse data into a dictionary
        results = {}
        try:
            row = self.table[int(message[0:3], 16)]
        except KeyError:
            return results
        results['Name'] = row['Name']
        #Isolate data
        data_length = int(message[3], 16)
        data_end = data_length * 2 + 4
        data = int(message[4:data_end], 16)
        #Loop through table columns
        frame = 0
        bit_count = int(row['Start'])
        while row['F' + str(frame) + 'N'] is not None \
            and row['F' + str(frame) + 'W'] is not None \
            and row['F' + str(frame) + 'N'] != '' \
            and row['F' + str(frame) + 'W'] != '':
            frame_width = int(row['F' + str(frame) + 'W'])
            #Bitwise magic
            value = data >> int(64 - frame_width - bit_count)
            value = value & int((1 << int(frame_width)) - 1)
            results[row['F' + str(frame) + 'N']] = value
            bit_count += frame_width
            frame += 1
        return results
