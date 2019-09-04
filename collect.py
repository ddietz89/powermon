#!/usr/bin/python

from drivers import TcpClient
from drivers import GEM
from drivers import mysql

db = mysql.Database()

db.connect("localhost", "powermon", "powermongem", "powermon")

# Get list of known channels
channels = db.query("SELECT id, channel_num FROM channels WHERE device_id = '4'")

device = GEM.GEM()
driver = TcpClient.TcpClient("192.168.10.21", 80, device)

while(True):
    packet = driver.read(GEM.GEM48CHBinaryPacket())

    for packet_channel in packet.channels.keys():
        for channel in channels:
	    if channel['channel_num'] == packet_channel:
	        db.execute("INSERT INTO channel_packets (channel_id, voltage, seconds, wattsec, datetime) VALUES ('" + db.escape(str(channel['id'])) + "','" + db.escape(str(packet.voltage*10)) + "','" + db.escape(str(packet.seconds)) + "','" + db.escape(str(packet.channels[packet_channel].abs_wattsecond)) + "',NOW())")
