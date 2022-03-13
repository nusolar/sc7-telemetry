# SC-7 Telemetry
Python parsing for new motor-controllers.
## Using the code
The main script is contained in no_gui.py, and running `$ python no_gui.py`
in the terminal will print parsed CAN data to standard output. The data
may be read directly from a serial port, or from a file (for testing
purposes). 

## Understanding the code

### no_gui.py
This is the top-level script that you can run to get CAN data. It's not
very compicated, since it delegates most of the work to reciever.py. Right
now, it simply prints the parsed data to the screen, but in the future it
will send data to the base-station or to the driver display gui as needed.
The important thing to know is that if you want to read directly of the serial
port, you should call `get_packets` instead of `get_packets_from_file`.
If you want to use `get_packet_from_file`, as it stands right now, you
have to specifiy a filename referring to a 'cleaned' data file (like 
examples/collected_cleaned.dat).

### reciever.py
The purpose of the `Reciever` class is to open a connection with a serial
port, read in CAN data, send it to the parser for processing, and assemble
a generator object and return it to `no_gui.py`.

A Reciever object has 4 fields:
    * `can_table`    -  a .csv file which specifies the data values we can
                        find within a packet with a specific 'CAN_ID', and
                        how to parse that data value.
    * `log_file`     -  this is currently not being used.
    * `serial_port`  -  the name of the serial port off which to read CAN
                      data. This is specific to the CAN-USB that you use
                      as well as the operating system (macOS, Raspbian, ...).
                      Getting this right is crucial and may involve some trial
                      and error.
    * `baud_rate`    -  the baudrate at which data is read off the serial port.
                      Getting this right is also crucial. If a value of 500000 
                      bps stops working, then you will have to dig around in
                      the documention of the motor-controllers and maybe the 
                      CAN-USB to find the new value.


