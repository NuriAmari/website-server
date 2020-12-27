import secrets
import json
import os

import redis
from tornado.web import RequestHandler

r = redis.Redis(host="localhost", port=6379, db=0)

username = os.environ.get("WEBSITE_USERNAME")
password = os.environ.get("WEBSITE_PASSWORD")


class AuthHandler(RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
        if data["username"] == username and data["password"] == password:
            auth_cookie = secrets.token_urlsafe()
            r.sadd("COOKIES", auth_cookie)
            self.set_secure_cookie("auth", auth_cookie)
            self.write(json.dumps({"success": True}))
        else:
            self.write(json.dumps({"success": False}))
