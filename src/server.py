import socket
import processor
import logging
from multiprocessing.pool import ThreadPool

class Server:
    def __init__(self, address: str, port: int, cp: processor.Processor) -> None:
        self.address = address
        self.port = port
        self.__cp = cp

    def __enter__(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.bind((self.address, self.port))
        self.__socket.listen()
        self.__pool = ThreadPool()
        return self
    
    def listen(self):
        while(True):
            r_sock, r_ep = self.__socket.accept()
            logging.info("Client {}:{} connected".format(r_ep[0], r_ep[1]))
            self.__pool.apply_async(self.__process, kwds={'sock': r_sock, 'ep_ip': r_ep[0]})

    def __process(self, sock, ep_ip):
        data = sock.recv(1024)
        self.__cp.process(data, ep_ip)
        sock.close()
    
    def __exit__(self, *args):
        self.__socket.close()
        self.__pool.close()