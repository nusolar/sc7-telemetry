"""Creates a massive CSV table of packet values"""

from receiver import Receiver
from tempfile import TemporaryFile

with TemporaryFile(mode='w+t') as tempfile,\
    open('log.csv', mode='w') as logfile:
    receiver = Receiver()
    headers = []
    for packet in receiver.get_packets_from_file('examples/live_capture.txt'):
        #Skip invalid packets
        if 'Name' not in packet.keys():
            continue
        #Include Cell ID in name
        if 'Cell ID' in packet.keys():
            packet['Name'] = packet['Name'] + ' ' + str(packet['Cell ID'])
            del packet['Cell ID']
        #Append name to all keys
        name = packet['Name'] + ' '
        del packet['Name']
        for key in list(packet):
            packet[name + key] = packet[key]
            #Add nonexistent headers
            if name + key not in headers:
                headers.append(name + key)
            del packet[key]
        #Write to CSV
        result = []
        for header in headers:
            if header in packet.keys():
                result.append(str(packet[header]))
            else:
                result.append('')
        tempfile.write(','.join(result) + '\n')
    logfile.write(','.join(headers) + ',\n')
    tempfile.seek(0)
    logfile.write(tempfile.read())
