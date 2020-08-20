class APIError(Exception):
    msg = 'Unexpected error occurred during execution'

    def __init__(self, msg: str = None) -> None:
        if msg:
            self.msg = msg
        super().__init__(self.msg)
