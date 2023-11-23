class ExtentionError(Exception):
    """Exception raised when extention file is not json or csv

    Attributes
    ----------
    extention: str
        extention require for the processus to be done
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
