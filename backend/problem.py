import os

class Problem:
    def __init__(self, name: str):
        self.name = name
        self.test_names : list[str] = []
        self.update()

    def update(self):
        path = os.path.join(os.getcwd(), "problems", self.name, "input")
        self.test_names = os.listdir(path)

    def get_test(self):
        pass