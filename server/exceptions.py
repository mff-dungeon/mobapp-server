
class HttpException(Exception):
    def __init__(self, status, message, *args, **kwargs) -> None:
        self.status = status
        self.message = message
        super().__init__(*args, **kwargs)