
import pyvisa as visa
import time
rm = visa.ResourceManager(r'C:\WINDOWS\system32\visa64.dll')
print(rm)
print(rm.list_resources('TCPIP0::?*'))

try:
    '''Connect to the instruments'''
    supply = rm.open_resource('TCPIP0::192.168.0.251::5025::SOCKET')

    ''' Set up the power supply IO configuration'''
    supply.timeout = 10000  # 10s

    # Define string terminations
    supply.write_termination = '\n'
    supply.read_termination = '\n'


    # Set string terminations
    print('\nVISA termination string (write) set to newline: ASCII ',
          ord(supply.write_termination))
    print('VISA termination string (read) set to newline: ASCII ',
          ord(supply.read_termination))

    # Get the ID info of the power supply
    print('supply ID string:\n  ', supply.query('*IDN?'), flush=True)

    # Code goes here
    # Do basic setup for the power supply
    supply.write('VOLT:PROT 6, (@1)') # Set overvoltage protection
    print(supply.query('VOLT:PROT? (@1)'))
    supply.write('VOLT 3.7, (@1)') # Set voltage level
    print(supply.query('VOLT? (@1)'))
    supply.write('CURR 2.5, (@1)') # Set current limit
    print(supply.query('CURR? (@1)'))
    
    ''' Turn the output on, wait 5 seconds, then turn it off'''
    supply.write('OUTP 1, (@1)')
    time.sleep(5)
    supply.write('OUTP 0, (@1)')
    
except(KeyboardInterrupt):
    print('Keyboard Interrupted execution!')

except:
    print('Timeout!')
time.sleep(3)
supply.close()
