from tornado.web import RequestHandler


class AuthHandler(RequestHandler):
    def get(self):
        self.write("Hello World")
