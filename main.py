from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import os

from tornado.web import Application
from chess_ws_server import WSHandler
from auth import AuthHandler

application = Application(
    [
        (r"^/api/test", AuthHandler),
        (r"^/ws", WSHandler),
    ],
)

if __name__ == "__main__":
    server = HTTPServer(application)
    server.listen(8000)
    IOLoop.current().start()
