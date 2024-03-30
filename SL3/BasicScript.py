import pyvisa as visa
rm = visa.ResourceManager(r'C:\WINDOWS\system32\visa64.dll')
print(rm)
print(rm.list_resources('TCPIP0::?*'))

'''Connect to the Power Supply'''
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