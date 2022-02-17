from receiver import Receiver
import struct, binascii

ids_to_names = {
    '400': ('Serial Number', 'Tritium ID'),
    '401': None,
    '402': ('Bus Current', 'Bus Voltage'),
    '403': ('Vehicle Velocity', 'Vehicle Motor Velocity'),
    '404': ('Phase C current', 'Phase B current'),
    '405': ('Vd', 'Vq'),
    '406': ('Id', 'Iq'),
    '407': ('BEMFd', 'BEMFq'),
    '408': ('15V supply', None),
    '409': ('3.3V supply', '1.9V supply'),
    '409': ('3.3V supply', '1.9V supply'),
    '40B': ('Heat-sink Temp', 'Motor Temp'),
    '40C': (None, 'DSB Board Temp'),
    '40E': ('DC Bus AmpHours', 'Odometer'),
    '417': ('Slip Speed', None),
}

count = 0
for packet in Receiver().get_packets():
    if count > 250: break
    count += 1
    print(packet)
    packet_id = packet[0:3]
    if packet_id not in ids_to_names:
        print(f'I dont know this id: {packet_id}')
        continue
    if packet_id == '400':
        low = struct.unpack('<I', binascii.unhexlify(packet[3:11]))[0]
        high = struct.unpack('<I', binascii.unhexlify(packet[11:]))[0]
    elif packet_id == '401':
        print(f'status information: {packet}')
        continue
    else:
        low = struct.unpack('<f', binascii.unhexlify(packet[3:11]))[0]
        high = struct.unpack('<f', binascii.unhexlify(packet[11:]))[0]
    info = ids_to_names.get(packet_id)
    if(info[0] is None):
        print(f'{info[1]}: {low}\n')
    elif(info[1] is None):
        print(f'{info[0]}: {high}\n')
    else:
        print(f'{info[0]}: {high}, {info[1]}: {low}\n')

