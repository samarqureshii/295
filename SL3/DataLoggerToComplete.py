import matplotlib.pyplot as plt 
import pyvisa as visa
import numpy as n
import time, csv
rm = visa.ResourceManager(r'C:\WINDOWS\system32\visa64.dll')
print(rm)
print(rm.list_resources('TCPIP0::?*'))

try:
    '''Connect to the instruments'''
    meter =  rm.open_resource('TCPIP0::192.168.0.252::5025::SOCKET')
    supply = rm.open_resource('TCPIP0::192.168.0.251::5025::SOCKET')
 

    ''' Set up the digital multimeter and supply IO configuration'''
    meter.timeout = 10000
    supply.timeout = 10000  

    # Define string terminations
    meter.write_termination = '\n'
    meter.read_termination = '\n'
    supply.write_termination = '\n'
    supply.read_termination = '\n'

    # Set string terminations
    print('\nVISA termination string (write) set to newline: ASCII ',
          ord(meter.write_termination))
    print('VISA termination string (read) set to newline: ASCII ',
          ord(meter.read_termination))
    print('\nVISA termination string (write) set to newline: ASCII ',
          ord(supply.write_termination))
    print('VISA termination string (read) set to newline: ASCII ',
          ord(supply.read_termination))

    # Get the ID info of the digital multimeter and supply
    print('meter ID string:\n  ', meter.query('*IDN?'), flush=True)
    print('supply ID string:\n  ', supply.query('*IDN?'), flush=True)
     
    # TODO: Configure the power supply to output 5 VDC and a 
    # current limit of 100 mADC. Turn on the power supply. 
    # Be sure to connect the power supply to the LM335 as shown above.
     
    meter.write('CONF:VOLT: DC')

    # Set the number of datalogger measurements
    num_times = 20
    times = n.linspace(1,num_times,num_times)
    temperature = [0]*num_times

    time_idx = 0
    for i in times:
        # TODO: Take the voltage measurement every 0.25s and convert it to
        # a temperature in Celsius. Add the temperature measurement to the
        # existing array called "temperature" declared above.

    # Plot the resulting temperatures
    plt.plot(times,temperature, label='N/A')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Temperature vs Time')
    plt.legend()
    plt.show()

except(KeyboardInterrupt):
    print('Keyboard Interrupted execution!')