#!/usr/bin/python

from drivers import TcpClient
from drivers import GEM

device = GEM.GEM()
driver = TcpClient.TcpClient("192.168.10.21", 80, device)

while(True):
    driver.read(GEM.GEM48CHBinaryPacket()).print_packet()


