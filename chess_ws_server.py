from typing import Set

import redis
import chess
from tornado.websocket import WebSocketHandler

clients: Set[WebSocketHandler] = set()
r = redis.Redis(host="localhost", port=6379, db=0)


def reset_board():
    r.set("FEN", chess.STARTING_FEN)


def get_board_state():
    return r.get("FEN")


def get_turn():
    pass


def broadcast(fen):
    for client in clients:
        client.write_message(fen)


class WSHandler(WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        clients.add(self)
        self.write_message("Connected".encode("utf-8"))
        # self.write_message(get_board_state())

    def on_message(self, message):
        self.write_message("Reply".encode("utf-8"))
        # board = chess.Board(get_board_state())
        # try:
        #     board.push_san(message)
        # except ValueError:
        #     # illegal move
        #     # TODO probably want a better sentinal value for invalid move
        #     # also need messages for game end etc
        #     self.write_message("")
        # else:
        #     new_board_state = board.board_fen()
        #     r.set("FEN", new_board_state)
        #     boardcast(new_board_state)

    def on_close(self):
        clients.remove(self)
