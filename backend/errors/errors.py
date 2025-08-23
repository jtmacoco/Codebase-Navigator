class InvalidUrl(Exception):
    def __init__(self,message="Invalid URL"):
        self.message = message
        super().__init__(self.message)

class CloneError(Exception):
    def __init__(self,message="Error Retrieving Repo"):
        self.message = message
        super().__init__(self.message)

class ProcessCodebaseError(Exception):
    def __init__(self,message="Error while processing codebase"):
        self.message = message
        super().__init__(self.message)

class RAGError(Exception):
    def __init__(self,message="Sorry Error while Generating A Resposne"):
        self.message=message
        super().__init__(self.message)
