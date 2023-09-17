from typing import Literal
import json


class Message:
    def __init__(self, role: str, content):
        self.role = role
        self.content = content

    def toJSON(self):
        return json.dumps({"role": self.role, "content": self.content})

    def getMessage(self) -> dict:
        return {"role": self.role, "content": self.content}