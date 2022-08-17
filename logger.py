class UploadStatus:
    def __init__(self, status, message, name):
        self.status = status
        self.message = message
        self.name = name

    def __str__(self):
        return f"Upload {self.status}: {self.name}"


def logger(status):
    print(status)
