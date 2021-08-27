import time
import zmq
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import threading

HOST = 'localhost'

DATA_PORT = 56792
CMD_PORT = 56791

WS_PORT = 8124

if __name__ != '__main__':
    exit()

one_time = ['click', 'feedback']
DecaMoveStatus = {}

context = zmq.Context()

data_socket = context.socket(zmq.SUB)
data_socket.setsockopt(zmq.SUBSCRIBE, b'')
data_socket.connect("tcp://{host}:{port}".format(host = HOST, port = DATA_PORT))

cmd_socket = context.socket(zmq.PUB)
cmd_socket.connect("tcp://{host}:{port}".format(host = HOST, port = CMD_PORT))

def data_listener(socket):
    while True:
        msg = socket.recv().decode()
        [key, value] = msg.split(' ', 1)
        DecaMoveStatus[key] = value

data_thread = threading.Thread(target = data_listener, args = (data_socket,), daemon = True)
data_thread.start()

class SimpleEcho(WebSocket):

    def handleMessage(self):
        print(self.data)
        if (self.data is not None):
            if (self.data.startswith('cmd')):
                cmd_socket.send(self.data.encode())
            else:
                for key in self.data.split():
                    if (key in DecaMoveStatus):
                        self.sendMessage(key + ' ' + DecaMoveStatus[key])
                        if (key in one_time):
                            DecaMoveStatus.pop(key)

    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')

def wsserver(wsport):
    print("--Starting NeosDeca Websocket Server Process at port %s--" % wsport)
    server = SimpleWebSocketServer('', wsport, SimpleEcho)
    server.serveforever()

ws_thread = threading.Thread(target = wsserver, args = (WS_PORT,), daemon = True)
ws_thread.start()

while True:
    try:
        print(DecaMoveStatus)
        time.sleep(1)
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(e)
