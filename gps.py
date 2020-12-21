#!/usr/bin/env python3.5
# coding=utf-8
"""TriviaL example using the thread triumvirate
        agps_thread = AGPS3mechanism()
        agps_thread.stream_data()
        agps_thread.run_thread()
    imported from the agps3threaded.py class AGPS3mechanism.  The unordered associative array
    from the gpsd is then exposed as attributes of that 'data_stream'

from time import sleep

from gps3.agps3threaded import AGPS3mechanism

__author__ = 'Moe'
__copyright__ = 'Copyright 2016  Moe'
__license__ = 'MIT'
__version__ = '0.2'

agps_thread = AGPS3mechanism()  # Instantiate AGPS3 Mechanisms
agps_thread.stream_data()  # From localhost (), or other hosts, by example, (host='gps.ddns.net')
agps_thread.run_thread()  # Throttle time to sleep after an empty lookup, default 0.2 second, default daemon=True

while True:  # All data is available via instantiated thread data stream attribute.
    # line #140-ff of /usr/local/lib/python3.5/dist-packages/gps3/agps.py
    print('---------------------')
    print(                   agps_thread.data_stream.time)
    print('Lat:{}   '.format(agps_thread.data_stream.lat))
    print('Lon:{}   '.format(agps_thread.data_stream.lon))
    print('Speed:{} '.format(agps_thread.data_stream.speed))
    print('Course:{}'.format(agps_thread.data_stream.track))
    print('---------------------')
    sleep(2)  # Sleep, or do other things for as long as you like.

"""
#!/usr/bin/env python3

import gpsd

# Connect to the local gpsd
gpsd.connect()

# Connect somewhere else
gpsd.connect()

# Get gps position
packet = gpsd.get_current()

# See the inline docs for GpsResponse for the available data
print(" ************ PROPERTIES ************* ")
print("  Mode: " + str(packet.mode))
print("Satellites: " + str(packet.sats))
if packet.mode >= 2:
    print("  Latitude: " + str(packet.lat))
    print(" Longitude: " + str(packet.lon))
    print(" Track: " + str(packet.track))
    print("  Horizontal Speed: " + str(packet.hspeed))
    print(" Time: " + str(packet.time))
    print(" Error: " + str(packet.error))
else:
    print("  Latitude: NOT AVAILABLE")
    print(" Longitude: NOT AVAILABLE")
    print(" Track: NOT AVAILABLE")
    print("  Horizontal Speed: NOT AVAILABLE")
    print(" Error: NOT AVAILABLE")

if packet.mode >= 3:
    print("  Altitude: " + str(packet.alt))
    print(" Climb: " + str(packet.climb))
else:
    print("  Altitude: NOT AVAILABLE")
    print(" Climb: NOT AVAILABLE")

print(" ************** METHODS ************** ")
if packet.mode >= 2:
    print("  Location: " + str(packet.position()))
    print(" Speed: " + str(packet.speed()))
    print("Position Precision: " + str(packet.position_precision()))
    print("  Time UTC: " + str(packet.time_utc()))
    print("Time Local: " + str(packet.time_local()))
    print("   Map URL: " + str(packet.map_url()))
else:
    print("  Location: NOT AVAILABLE")
    print(" Speed: NOT AVAILABLE")
    print("Position Precision: NOT AVAILABLE")
    print("  Time UTC: NOT AVAILABLE")
    print("Time Local: NOT AVAILABLE")
    print("   Map URL: NOT AVAILABLE")

if packet.mode >= 3:
    print("  Altitude: " + str(packet.altitude()))
    # print("  Movement: " + str(packet.movement()))
    # print("  Speed Vertical: " + str(packet.speed_vertical()))
else:
    print("  Altitude: NOT AVAILABLE")
    # print("  Movement: NOT AVAILABLE")
    # print(" Speed Vertical: NOT AVAILABLE")

print(" ************* FUNCTIONS ************* ")
print("Device: " + str(gpsd.device()))