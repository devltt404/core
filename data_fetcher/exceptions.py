class APIRateLimitExceeded(Exception):
    def __init__(self, message="API rate limit reached. Please try again tomorrow."):
        self.message = message
        super().__init__(self.message)
