from .submission import Submission

class Team:
    def __init__(self, name: str, password: str):
        self.name = name
        self.password = password
        self.score = 0
        self.submissions : list[Submission] = [Submission("0", "example.txt")]