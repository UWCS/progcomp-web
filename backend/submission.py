class Submission:
    def __init__(self, p_num: str, input_name: str) -> None:
        self.timestamp = "00:00:00"
        self.p_num = p_num
        self.dataset : str = input_name
        self.result : str = "UNKNOWN"

    
    def add_score(self, score):
        pass