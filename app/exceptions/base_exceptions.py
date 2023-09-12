"""
    Module for base Exception
"""


class BaseError(Exception):
    def __init__(self, code, detail) -> None:
        self.code = code
        self.detail = detail

    def dict(self):
        return {"code": self.code, "detail": self.detail}
