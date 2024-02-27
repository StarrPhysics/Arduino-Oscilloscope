from multiprocessing import Queue
import re
import numpy as np

from serial import Serial
from serial.tools.list_ports import comports as getPortInfo
from serial.tools.list_ports_common import ListPortInfo as PortInfo

def find_ardueno_serial_port() -> PortInfo:
    """
    Opens the serial port stream and searches for an Arduino port.
    If an Arduino port is found, it starts reading data from the port and puts it into the queue.

    Returns:
        PortInfo: Information about the Arduino serial port.

    Raises:
        N/A
    """
    avaliablePorts: list[PortInfo] = getPortInfo()

    print('Scanning Ports...')
    for portInfo in avaliablePorts:
            if (manufacturer := portInfo.manufacturer) == None: continue
                
            if manufacturer.find('Arduino') >= 0:
                print('Found Arduino Port!')
                return portInfo
            
    print('No Arduino Port Found')    
    exit(0)

def establish_serial_port_connection(portInfo: PortInfo,
                                     queue: Queue,
                                     baud: int
                                    ) -> Serial:
    """
    This function will open the Arduino's serial port and establish the connection between the Arduino program and the python program.

    Args:
        portInfo (ListPortInfo): Information about the serial port.
        queue (Queue): A queue to store the incoming data.

    Returns:
        Serial: The serial connection object.

    Raises:
        N/A

    This function attempts a 'handshake' with the Arduino program in which crucial data is exchanged.
    """
    
    print(f'Attempting to connect to port "{portInfo.device}"...')

    ser = Serial(portInfo.device, baud)
    ser.flushInput()

    print(f'Connected to port "{portInfo.device}"!')

    # Establish Handshake with Ardueno Program
    while True:
        parsedMessage: list[str] = re.split(';|,', ser.read_until(b'\n').strip(b'\r\n').decode('utf-8', errors='ignore'))

        if len(parsedMessage) < 3: continue
        
        sender, messageType, *pins = parsedMessage

        if sender == 'Arduino' and messageType == 'ArduinoOscilloscope_Handshake': 
            print('Recieved Handshake from Ardueno')
            queue.put(pins)
            break
    
    print('Responding to Handshake...')
    ser.write(b'Client;ArduinoOscilloscope_Handshake\n') # Lets the Ardueno program know that the python program is ready to receive data
    return ser

def runtime_data_manager(ser: Serial, queue: Queue) -> None:
    """
    Manages the reception and precessing of the data from the ardueno during the plot's runtime.
    """
    dataBuffer: list[list] = [] # Multidimentional array, containing lists whose first index is the specific index of the pin and whose second index is the measured the electric potential.

    while True:
        if queue.empty(): dataBuffer  = [] # Resets the data buffer if the queue is empty, implying the data was recieved on the other end.

        if ser.in_waiting != 0:
            
            incomingPacketList: list[bytes] = ser.readlines(20) #Ex: [b'\x80\xf8\x80\n', b'\x80\xf8\x80\n']
            
            parsedDataPacketList = [[byte - 128 for byte in packet.strip()] for packet in incomingPacketList] # Byte values shifted by 128 as part of decoding process. Refer to the ardueno-side of the code for more information.

            for parsedDataPacket in parsedDataPacketList: # Interprets each of the parsed data packets and appends result it to the data buffer.
                if len(parsedDataPacket) != 3: continue
                dataBuffer.append(
                    [   parsedDataPacket[0], # First entry is the pin index
                        np.round(np.float16(parsedDataPacket[1] + (parsedDataPacket[2]<< 7)) * np.float16(5.0) / np.float16(1023.0), 2) # Second entry is the electric potential. This is interpreted from the two bytes in the packet. Refer to the ardueno-side of the code for more information.
                    ])
            queue.put(dataBuffer)

# Main Function for this Module
            
def main(queue: Queue, baud: int) -> None:
    """
    The main function for the `serial_utils.py` file, which:
    1. Searches and detects for the ardueno's serial port.
    2. Establishes a connection with the ardueno's serial port to initalize the program.
    3. Manages the data recieved from the ardueno during the plot's runtime from the ardueno.
    """

    arduinoPortInfo: PortInfo = find_ardueno_serial_port()

    ser: Serial = establish_serial_port_connection(arduinoPortInfo, queue, baud)

    runtime_data_manager(ser, queue)
    

