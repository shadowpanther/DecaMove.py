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

msgCount = 0

context = zmq.Context()

class SimpleEcho(WebSocket):
    def data_listener(self):
        global msgCount
        data_socket = context.socket(zmq.SUB)
        data_socket.setsockopt(zmq.SUBSCRIBE, b'')
        data_socket.connect("tcp://{host}:{port}".format(host = HOST, port = DATA_PORT))
        while True:
            msg = data_socket.recv_string()
            self.sendMessage(msg)
            msgCount = msgCount + 1
            if(self.data_thread_terminate.is_set()):
                break
        data_socket.close()

    def handleMessage(self):
        print(self.data)
        if (self.data is not None):
            self.cmd_socket.send_string(self.data)

    def handleConnected(self):
        self.data_thread = threading.Thread(target = self.data_listener, args = (), daemon = True)
        self.data_thread_terminate = threading.Event()
        self.data_thread.start()
        self.cmd_socket = context.socket(zmq.PUB)
        self.cmd_socket.connect("tcp://{host}:{port}".format(host = HOST, port = CMD_PORT))
        print(self.address, 'connected')

    def handleClose(self):
        self.data_thread_terminate.set()
        print(self.address, 'closed')

def wsserver(wsport):
    print("--Starting NeosDeca Websocket Server Process at port %s--" % wsport)
    server = SimpleWebSocketServer('', wsport, SimpleEcho)
    server.serveforever()

ws_thread = threading.Thread(target = wsserver, args = (WS_PORT,), daemon = True)
ws_thread.start()

while True:
    try:
        print(msgCount, " messages processed in the last second")
        msgCount = 0
        time.sleep(1)
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(e)
