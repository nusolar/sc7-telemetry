from receiver import Receiver

r = Receiver()

for item in r.get_packets_from_file('examples/collected_cleaned.dat'):
    print(item)
