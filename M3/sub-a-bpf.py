#!/usr/bin/env python
"""Subsystem A unit testing script.
This script measures the frequency response of the pre-mixer BPF."""

import pyvisa
import time
from numpy import *
from matplotlib.pyplot import *
import sys

__author__ = 'Sean Victor Hum'
__copyright__ = 'Copyright 2023'
__license__ = 'GPL'
__version__ = '1.0'
__email__ = 'sean.hum@utoronto.ca'

def user_prompt():
    str = input('Hit Enter to proceed or ! to abort:')
    if (str == '!'):
        print('Measurement aborted')
        user_abort()

def user_abort():
        scope.write(':WGEN:OUTP OFF')
        fxngen.write('OUTPut1 OFF')
        fxngen.write('OUTPut2 OFF')
        scope.close()
        fxngen.close()
        sys.exit(0)
        
# Open instrument connection(s)
rm = pyvisa.ResourceManager()
school_ip = True
#school_ip = False
if (school_ip):
    scope = rm.open_resource('TCPIP0::192.168.0.253::hislip0::INSTR')
    fxngen = rm.open_resource('TCPIP0::192.168.0.254::5025::SOCKET')
else:
    scope = rm.open_resource('TCPIP0::192.168.2.253::hislip0::INSTR')
    fxngen = rm.open_resource('TCPIP0::192.168.2.254::5025::SOCKET')

# Define string terminations and timeouts
scope.write_termination = '\n'
scope.read_termination = '\n'
fxngen.write_termination = '\n'
fxngen.read_termination = '\n'
scope.timeout = 10000           # 10s
fxngen.timeout = 10000          # 10s

# Get ID info
scope_id = scope.query('*IDN?').strip().split(',')
fxngen_id = fxngen.query('*IDN?').strip().split(',')
print('Connected to oscilloscope:', scope_id[1], flush=True)
print('Connected to function generator:', fxngen_id[1], flush=True)

# Set probe scaling to 1:1
scope.write('CHANnel1:PROBe +1.0')
scope.write('CHANnel2:PROBe +1.0')

# Setup trigger
scope.write(':TRIG:SWEep AUTO')
scope.write(':TRIG:EDGE:SOURce CHAN1')
scope.write(':TRIG:EDGE:LEVel +0.0')

#print('Trigger:', scope.query(':TRIG?'), flush=True)

print('Connect your subsystem as shown in the wiring diagram and power it on.')
print('Make sure you have de-asserted the /TXEN line (set it high)!')
user_prompt()

# Setup function generator on scope as stimulus
scope.write(':WGEN:FUNC SIN')
scope.write(':WGEN:OUTP ON')

# Set waveform generator output impedance to high Z
fxngen.write('OUTPUT1:LOAD INF')
fxngen.write('OUTPUT2:LOAD INF')
fxngen.write('UNIT:ANGL DEG')

# Setup waveform generator
fxngen.write('SOUR1:FUNCtion SIN')
fxngen.write('SOUR1:VOLTage:HIGH +3.3')
fxngen.write('SOUR1:VOLTage:LOW +0.0')
fxngen.write('SOUR1:PHASe:SYNC')
fxngen.write('SOUR1:PHASe +0.0')
fxngen.write('OUTPut1 ON')

fxngen.write('SOUR2:FUNCtion SIN')
fxngen.write('SOUR2:VOLTage:HIGH +3.3')
fxngen.write('SOUR2:VOLTage:LOW +0.0')
fxngen.write('SOUR2:PHASe:SYNC')
fxngen.write('SOUR2:PHASe -9.0E+01')
fxngen.write('OUTPut2 ON')

# Setup acquisition
scope.write(':TIMebase:SCAL +5.0E-04') # 500 us/div
scope.write(':CHAN1:COUP AC')
scope.write(':CHAN2:COUP AC')

# Frequency sweep
N = 51
freq = arange(N)/(N-1)*16e6 + 4e6
offset = 1e3                    # Offset between RF and LO frequencies
input_ampl = 50e-3              # Amplitude of wave generator output

# Set up instruments for first frequency point
fxngen.write('SOUR1:FREQuency %e' % (14e6))
fxngen.write('SOUR2:FREQuency %e' % (14e6))
scope.write(':WGEN:FREQ %e' % (14e6+offset))
scope.write(':WGEN:volt %e' % (input_ampl))

print('The following frequency points will be measured:', freq)

# Initialize vectors for storing data
ampl_i = zeros(N, float)
ampl_q = zeros(N, float)
#phdiff = zeros(N, float)

print('Adjust the timebase and triggering so the signals are stable.')
print('Adjust the voltage scale on CH1 and CH2 so they are identical')
print('and the 2 signals occupy most of the screen.')
user_prompt()

# Check the scale is identical on both channels
scale1 = scope.query(':CHAN1:SCAL?')
scale2 = scope.query(':CHAN2:SCAL?')

if (scale1 != scale2):
    print('The scales of the 2 channels do not match.')
    user_abort()

# Frequency sweep loop
scope.write(':TIMebase:SCAL +2.0E-04') 
for k in range(N):
    fxngen.write('SOUR1:FREQuency %e' % freq[k])
    fxngen.write('SOUR2:FREQuency %e' % freq[k])
    scope.write(':WGEN:FREQ %e' % (freq[k]+offset))
    time.sleep(0.5)
    #scope.write(':SINGle')
    ampl_i[k] = float(scope.query(':MEAS:VPP? CHAN1'))
    ampl_q[k] = float(scope.query(':MEAS:VPP? CHAN2'))
    #phdiff[k] = float(scope.query(':MEAS:PHASe? CHAN1'))
    print('Frequency point %d/%d, f=%.2f MHz: %f %f' % (k+1, N, freq[k]/1e6, ampl_i[k], ampl_q[k]))

print('Done')
    
scope.write(':WGEN:OUTP OFF')
fxngen.write('OUTPut1 OFF')
fxngen.write('OUTPut2 OFF')
fxngen.close()
scope.close()
    
# Save and plot data
savetxt('bpf.txt', (freq, ampl_i, ampl_q))

H2 = (ampl_i/input_ampl)**2 + (ampl_q/input_ampl)**2

fig, ax = subplots()
ax.plot(freq/1e6, 10*log10(H2))
ax.set_xlabel('Frequency [MHz]');
ax.set_ylabel('Subsystem gain [dB]');
ax.grid(True)
ax.set_title('Frequency response of BPF')
savefig('bpf.png')