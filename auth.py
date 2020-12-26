import secrets
import json

import redis
from tornado.web import RequestHandler

r = redis.Redis(host="localhost", port=6379, db=0)


class AuthHandler(RequestHandler):
    def get(self):
        self.write("Hello World")

    def post(self):
        data = json.loads(self.request.body)
        print("aa", data)
        if data["username"] == "username" and data["password"] == "password":
            auth_cookie = secrets.token_urlsafe()
            r.sadd("COOKIES", auth_cookie)
            self.set_secure_cookie("auth", auth_cookie)
            self.write(json.dumps({"success": True}))
        else:
            self.write(json.dumps({"success": False}))
