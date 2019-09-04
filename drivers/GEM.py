from drivers import Device

class GEM(Device.Device):
    def __init__(self):
        super(GEM, self).__init__()

	self.name = "GEM"

	# Defaults
	self.RETRIES = 5


    def poll(self, packet_type, socket):
       tries = 0
       while tries < self.RETRIES:
           tries += 1
	   try:
	       self.request(socket)

	       return self.read_packet(packet_type, socket)
	   except Exception as e:
	       print e

    def request(self, socket):
        socket.sendall('^^^APISPK')

    def read_packet(self, packet_type, socket):
        packets = []
	n = 0
	while n < 10:
	    n += 1
	    ret = packet_type.read(socket)
	    if ret:
	        return ret

class DataPacket():
    def __init__(self):
        self.voltage = None
	self.serial = None
	self.channels = {}

    def print_packet(self):
        print "Packet"
	print ""
	print "Voltage: " + str(self.voltage) + " V"
        
	for num in self.channels.keys():
	    if num >= 32:
	        continue
	    print "Channel: " + str(num)
	    channel = self.channels[num]
	    print str(channel.abs_wattsecond) + " Ws " + str(channel.net_wattsecond) + " Ws"
	    print str(channel.amp)  + " A"
	    print str(channel.watt)  + " W"

	print ""


class Channel():
    def __init__(self):
        self.abs_wattsecond = None
        self.net_wattsecond = None
        self.serial = None
	self.current = None
	self.watt = None



# GEM-PKT_Packet_Format_2_1.pdf
class Packet(object):
    def __init__(self):
        
	self.LENGTH_BYTES = None

    def validateByte(self, byte, expected):

        byte = ord(byte)
        if byte == expected:
	    return True
	else:
	    print "Invalid format"
	    print "Got " + hex(byte) + " expected " + hex(expected)
	    return False

    def read(self, socket):

        bytes = []

        self.validateByte(socket.recv(1), self.HEADER1)
        self.validateByte(socket.recv(1), self.HEADER2)
        self.validateByte(socket.recv(1), self.HEADER3)

	packet = ""

	while len(packet) < self.LENGTH_BYTES:
	    r = socket.recv(self.LENGTH_BYTES - len(packet))
	    if not r:
	        print "Error, EOF"
	        return False
	    packet += r

        self.validateByte(socket.recv(1), self.FOOTER1)
        self.validateByte(socket.recv(1), self.FOOTER2)

	checksum = ord(socket.recv(1))

	if checksum != self.calculate_checksum([ord(p) for p in packet]):
	    print "Error, checksum failed."
	    return False

	return self.parse(packet)

    def calculate_checksum(self, data):
        checksum = self.HEADER1
	checksum += self.HEADER2
	checksum += self.HEADER3
	checksum += sum(data)
	checksum += self.FOOTER1
	checksum += self.FOOTER2
        return checksum & 0xff

    def lohi(self, data):
        val = 0
	pos = 0
        for p in data:
	    val += ord(p) * 256**pos
	    pos += 1
	return val
	    
    def hilo(self, data):
        val = 0
	pos = len(data)-1
        for p in data:
	    val += ord(p) * 256**pos
	    pos -= 1
	return val



	    

class GEM48CHBinaryPacket(Packet):
    def __init__(self):
        super(GEM48CHBinaryPacket, self).__init__()

	self.LENGTH_BYTES = 613
	self.HEADER1 = 254
	self.HEADER2 = 255
	self.HEADER3 = 5

	self.FOOTER1 = 255
	self.FOOTER2 = 254

	self.channels = 48

    def parse(self, packet):
        dp = DataPacket()

        dp.voltage = self.hilo(packet[0:2]) / 10.0

	for i in range(1,self.channels+1):
	    ch = Channel()
	    ch.voltage = dp.voltage
	    ch.abs_wattsecond = self.lohi(packet[2+5*(i-1):2+5*i])
	    ch.net_wattsecond = self.lohi(packet[242+5*(i-1):242+5*i])
	    ch.amp = round(self.lohi(packet[486+2*(i-1):486+2*i]) / 50.0, 2)
	    ch.watt = round(ch.voltage * ch.amp, 2)

	    dp.channels[i] = ch

	return dp





