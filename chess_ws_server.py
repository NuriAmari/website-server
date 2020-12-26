from typing import Set
import json

import redis
import chess
from tornado.websocket import WebSocketHandler

clients: Set[WebSocketHandler] = set()
r = redis.Redis(host="localhost", port=6379, db=0)


def get_white_wins():
    if not r.exists("W_WINS"):
        r.set("W_WINS", 0)
    return r.get("W_WINS").decode("utf-8")


def get_black_wins():
    if not r.exists("B_WINS"):
        r.set("B_WINS", 0)
    return r.get("B_WINS").decode("utf-8")


def white_win():
    r.incr("W_WIN")


def black_win():
    r_incr("B_WIN")


def reset_board():
    r.set("FEN", chess.STARTING_FEN)


def get_board_state():
    if not r.exists("FEN"):
        reset_board()
    return r.get("FEN").decode("utf-8")


def broadcast(fen):
    for client in clients:
        client.write_message(fen)


class WSHandler(WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        clients.add(self)
        self.write_message(
            json.dumps(
                {
                    "FEN": get_board_state(),
                    "W_WINS": get_white_wins(),
                    "B_WINS": get_black_wins(),
                }
            )
        )

    def on_message(self, message):
        board = chess.Board(get_board_state())

        if board.turn == chess.BLACK:
            # check for auth cookie
            if not r.sismember("COOKIES", self.get_secure_cookie("auth")):
                return

        try:
            board.push_san(message)
        except ValueError:
            # ignore illegal moves
            pass
        else:
            new_board_state = board.fen()
            r.set("FEN", new_board_state)
            r.rpush("HISTORY", message)
            broadcast(json.dumps({"FEN": new_board_state, "SAN": message}))

            if board.is_game_over():
                result = board.result()
                if result == "1-0":
                    white_win()
                elif result == "0-1":
                    black_win()
                else:
                    # draw
                    white_win()
                    black_win()

                reset_board()
                r.delete("HISTORY")

    def on_close(self):
        print("close", self)
        clients.remove(self)
