
import pyvisa as visa
import time

rm = visa.ResourceManager(r'C:\WINDOWS\system32\visa64.dll')
print(rm)
print(rm.list_resources('TCPIP0::?*'))

try:
    #Connect to the instruments
    meter =  rm.open_resource('TCPIP0::192.168.0.252::5025::SOCKET')
    
    #Set up the digital multimeter IO configuration
    meter.timeout = 20000

    # Define string terminations
    meter.write_termination = '\n'
    meter.read_termination = '\n'

    # Set string terminations
    print('\nVISA termination string (write) set to newline: ASCII ',
          ord(meter.write_termination))
    print('VISA termination string (read) set to newline: ASCII ',
          ord(meter.read_termination))

    # Get the ID info of the digital multimeter 
    print('meter ID string:\n  ', meter.query('*IDN?'), flush=True)

    # Configure DC voltage measurement
    meter.write('CONF:VOLT:DC') 
    print(meter.query('READ?')) 
    
    # Measure DC voltage
    print(meter.query('MEAS:VOLT:DC?'))
    
except(KeyboardInterrupt):
    print('Keyboard Interrupted execution!')