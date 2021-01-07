from tornado.web import RequestHandler
from simplejson.src.json import json

from langtools.lexer.exceptions import LexicalError

import json as simplejson


class FormatHandler(RequestHandler):
    def post(self):
        try:
            content_str = self.request.body.decode("utf-8")
            content = json.loads(content_str)
        except LexicalError as le:
            self.write(
                simplejson.dumps(
                    {
                        "content": content_str,
                        "annotations": [
                            {
                                "type": "error",
                                "text": f"Unexpected Character: {le.error_char} at line {le.error_line + 1}, col {le.error_col}",
                                "row": le.error_line,
                                "column": le.error_col,
                            }
                        ],
                        "markers": [
                            {
                                "startRow": le.error_line,
                                "endRow": le.error_line,
                                "startCol": le.error_col,
                                "endCol": le.error_col + 1,
                                "type": "text",
                                "className": "error-marker",
                            }
                        ],
                    }
                )
            )
        except Exception as e:
            print(e)
            self.write(
                simplejson.dumps({"content": '{"oops": true}', "annotations": []})
            )
        else:
            self.write(
                simplejson.dumps({"content": json.dumps(content), "annotations": []})
            )


class LintHandler(RequestHandler):
    def post(self):
        self.write(
            json.dumps(
                {"content": self.request.body.decode("utf-8"), "annotations": []}
            )
        )
