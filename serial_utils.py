from multiprocessing import Queue
import time
import re
from typing import Union
from serial import Serial

from serial.tools.list_ports import comports as getPortInfo
from serial.tools.list_ports_common import ListPortInfo as PortInfo



def readLine_managed(serial: Serial, decode: str = None, strip: bool = False, loopLimit: int = None) -> Union[bytes, str]:
    """
    Pyserial's serial.read methods may return incomplete strings if data is received in chunks.
    This function batches data from the serial port until an endline character is detected.
    
    Args:
        serial (Serial): The serial port object to read from.
        decode (str): The encoding to decode the data into.
        strip (bool): Whether to strip the data of its trailing newline character.
        loopLimit (int): the limit for the number of loops that can be made before returning.
        
    Returns:
        bytes: The data read from the serial port.
    """
    if decode is None and strip is True: raise ValueError('Cannot strip data if datatype is not string. Please specify a decode type.')

    serialBuffer: bytes = b''

    i = 0

    while True if loopLimit is None else i < loopLimit:
        if serial.in_waiting > 0:
            serialBuffer += serial.read_all()
            if serialBuffer[-1] == 10:
                break
        i += 1

    if decode is not None:
         if strip:
             return serialBuffer.decode(decode).strip()
         else:
              return serialBuffer.decode(decode)
    
    return serialBuffer




def find_ardueno_serial_port() -> PortInfo:
    """
    Opens the serial port stream and searches for an Arduino port.
    If an Arduino port is found, it starts reading data from the port and puts it into the queue.
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
                




def establish_serial_port_connection(portInfo: PortInfo, queue: Queue) -> Serial:
    """
    This function will open the Arduino's serial port and establish the connection between the Arduino program and the python program.

    Args:
        portInfo (ListPortInfo): Information about the serial port.
        queue (Queue): A queue to store the incoming data.

    Returns:
        None

    Raises:
        N/A

    This function attempts a 'handshake' with the Arduino program in which crucial data is exchanged.
    """
    
    print(f'Attempting to connect to port "{portInfo.device}"...')

    ser = Serial(portInfo.device, 9600)

    print(f'Connected to port "{portInfo.device}"!')

    # Establish Handshake with Ardueno Program
    while True:
        handshake_data: str = readLine_managed(ser, 'utf-8', True)
        # Expected to Recieve: 'Arduino;ArduinoOscilloscope_Handshake;A1,A2,A15'

        sender, messageType, *pins = re.split(';|,', handshake_data)

        if sender == 'Arduino' and messageType == 'ArduinoOscilloscope_Handshake': 
            print('Recieved Handshake from Ardueno')
            queue.put(pins)
            break
    
    print('Responding to Handshake...')
    ser.write(b'Client;ArduinoOscilloscope_Handshake\n') # Lets the Ardueno program know that the python program is ready to receive data
    time.sleep(0.5)

    while True:
        if readLine_managed(ser, 'utf-8', strip=True) == 'Arduino;Confirmed':
            print('Handshake Complete. Proceeding to data stream...')
            break
    return ser

def runtime_data_stream_manager(ser: Serial, queue: Queue) -> None:
    dataBuffer: list[list[float]] = []

    while True:
        if ser.in_waiting > 0:
            print(readLine_managed(ser))
    
    #print(' '.join(format(ord(x), 'b') for x in ser.readline().decode('utf-8')))
    
    """while True:
        loopStartTime = datetime.datetime.now()
        try:
            # Read the data from the serial port
            # Incoming data example: '{"A0": "1.23", "A1": "1.35"}'
            pinData = json.loads(re.sub("\\r+|\s+|\\n+", "", ser.readline().decode('utf-8'))) 
        except UnicodeDecodeError:
            continue
            
        processingTime      = float((datetime.datetime.now() - loopStartTime).microseconds*1e-6) # Seconds
        processingFrequency = 1.0 / processingTime # Hertz
        queue.put(queueDataStructure(pinData, {'processingTime': processingTime, 'processingFrequency': processingFrequency}))"""

    """
    #ser.flushInput()

    while True:
        print('_______')
        print(ser.in_waiting)
        if ser.in_waiting > 0:
            x = ' '.join(format(ord(x), 'b') for x in ser.readline().decode('utf-8'))
            print(x)
        #print(s)
        
        #ser.write(b'Testing 1 2 3')
    """
    pass

# Main Function for this Module
def main(queue: Queue) -> None:
    arduinoPortInfo: PortInfo = find_ardueno_serial_port()

    ser: Serial = establish_serial_port_connection(arduinoPortInfo, queue)

    runtime_data_stream_manager(ser, queue)
    

