import socket
import processor
from multiprocessing.pool import ThreadPool

class Server:
    def __init__(self, address: str, port: int, cp: processor.Processor) -> None:
        self.address = address
        self.port = port
        self.__cp = cp

    def __enter__(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Binding socket")
        self.__socket.bind((self.address, self.port))
        print("Socket binded")
        self.__socket.listen()
        print("Socket opened")
        self.__pool = ThreadPool()
        self.__pool.apply_async(self.__listen)
        return self
    
    def __listen(self):
        while(True):
            r_sock, r_ep = self.__socket.accept()
            print("Client {} connected", r_ep)
            self.__pool.apply_async(self.__process, r_sock)

    def __process(self, sock: socket.socket):
        data = sock.recv(80)
        self.__cp.process(data)
        sock.close()
    
    def __exit__(self, *args):
        self.__socket.close()
        self.__pool.close()