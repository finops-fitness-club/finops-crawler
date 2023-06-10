class CloudAPI:
    def __init__(self, credentials):
        self.credentials = credentials

    def get_cost(self, start_date, end_date):
        raise NotImplementedError("This method should be overridden in subclass")
