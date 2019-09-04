from drivers import DataClient
import socket

class TcpClient(DataClient.DataClient):
    def __init__(self,host,port,device):
        super(TcpClient, self).__init__()

	self.host = host
	self.port = int(port)
	self.sock = None
	self.device = device

        # Set default variables
	self.CONNECT_TIMEOUT = 5
        socket.setdefaulttimeout(self.CONNECT_TIMEOUT)

    def connect(self):
        if self.sock is not None:
	     # Socket is already open
	     return

	# Create socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	self.sock.connect((self.host, self.port))

    def close(self):
        if self.sock:
	    self.sock.close()
	    self.sock = None

    def read(self, packet_type):
        packet = None
        try:
	    self.connect()
	    packet = self.device.poll(packet_type, self.sock)
	except socket.timeout:
	    print "Socket timeout"
	except socket.error, e:
	    print e
        finally:
	    self.close()
        
	return packet


        

