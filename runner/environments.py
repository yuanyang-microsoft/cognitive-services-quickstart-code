import os


class Environments:
    def __init__(self, _root_path):
        self.env = os.environ.copy()
