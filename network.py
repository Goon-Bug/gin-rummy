import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = socket.gethostbyname(socket.gethostname())
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def get_player(self):
        return self.p

    def connect(self):
        """
        Connect client to server and assign each player their ID number
        """
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(1024))  # assign each player a number
        except socket.error as e:
            print(e)

    def send_string_receive_game(self, data):
        """
        Takes string to send to the server and returns an object

        :param data: str
        :return: object
        """
        try:
            self.client.send(str.encode(data))

            game = self.client.recv(2048)
            return pickle.loads(game)
        except socket.error as e:
            print(e)

    def send_string_receive_card(self, data):
        """
        Takes string to send to the server and returns an object whilst removing excess game data from the server

        :param data: str
        :return: object
        """
        try:
            self.client.send(str.encode(data))

            card = self.client.recv(512)
            game = self.client.recv(1024)  # removes excess data
            return pickle.loads(card)
        except socket.error as e:
            print(e)



