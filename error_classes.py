class PDFParsingError(Exception):
    def __init__(self, message: str, file_path: str, original_error: Exception):
        super().__init__(message)
        self.file_path = file_path
        self.original_error = original_error