class Configuration:

    def __init__(self, host: str, headers: dict = None, enable_log: bool = True):
        self.host = host
        self.headers = headers
        self.enable_log = enable_log
