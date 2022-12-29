class Team:
    def __init__(self, name: str, password: str):
        self.name = name
        self.password = password
        self.score = 0
        self.submissions: list = []

    def add_submission(self, submission):
        self.submissions.append(submission)
        print(submission)
        sorted(self.submissions, key=lambda x: x.timestamp, reverse=True)
