import socket
import threading
import pickle
from player import Player
from game import Game
from buttonfunctions import server_btns as sb

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5555

########## Socket Setup ##########

SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# SOCK.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# uncomment for testing so that multiple servers can be created
# this saves waiting for the server to disconnect when restarting

try:
    SOCK.bind((SERVER, PORT))
except socket.error as e:
    print(e)

SOCK.listen()
print("[Server started] Waiting for connection")

########## Thread ##########

players = []  # list to store player objects
connections = set()  # set to store connected players

actions = {
    "pass": sb.pass_btn,
    "m_card": sb.middle_card,
    "deck": sb.deck,
    "reset": sb.reset,
    "change_reset": sb.change_reset,
    "reset_ready": sb.reset_ready,
    "play": sb.play_btn,
    "win": sb.win_btn,
    "hand": sb.hand,
    "ready": sb.ready,
    "new_game_ready": sb.new_game_ready,
    "new_game": sb.new_game

}


def handle_client(conn, player, game_id):
    """
    Constantly runs while client is connected. Handles sending and receiving data to and from the client

    :param conn: socket connection
    :param player: player object
    :param game_id: int
    """
    global player_count
    conn.sendall(pickle.dumps(player))
    game = games[game_id]
    while True:
        try:
            data = conn.recv(1024).decode()
            if game in games:
                if not data:
                    break
                else:
                    if ' ' not in data and 'get' not in data:
                        actions[data](game=game, conn=conn, player=player)

                    elif data[:4] == 'hand' or data[:4] == 'play':
                        actions[data[:4]](game=game, data=data, player=player)

                    elif data[:5] == 'ready':
                        actions[data[:5]](game=game, data=data, player=player)

                    elif data[:3] == 'win':
                        actions[data[:3]](game=game, data=data, player=player)

                    conn.sendall(pickle.dumps(game))
            else:
                print("Game not in list")
                break
        except socket.error:
            break

    print("Lost connection\nClosing game")

    try:
        del games[game_id]
        print("Closing Game", game_id)
    except:
        pass

    player_count -= 1

    conn.close()


########## Main Server ##########

games = []  # can be changed to a dictionary to store player IDs along with games respectively
player_count = 0

while True:
    conn, addr = SOCK.accept()
    print("Connected to:", addr)

    player_count += 1
    game_id = 0

    if player_count % 2 == 1:
        games.append(Game(game_id))
        # game_id += 1  # for possible multiple games
        player = Player(0, games[game_id])
        print("Creating a new game...")
    else:
        games[game_id].ready = True
        player = Player(1, games[game_id])

    thread = threading.Thread(target=handle_client, args=(conn, player, game_id))
    thread.start()
