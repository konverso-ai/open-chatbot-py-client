

class openchatbot_error(Exception):
    """Parent of all exceptions raised by this package"""

class chatbot_server_error(openchatbot_error):
    """Exception raised when an error occurs retrieving data from a chatbot server"""
    def __init__(self, status: int, description: str):
        super().__init__()
        self.status = status
        self.description = description

    def __str__(self):
        return "chatbot_server_error: %s: %s" % (self.status, self.description)

#
# Exception related to the processing of descriptor files
#
class repository_exception(openchatbot_error):
    pass

class no_chatbot_descriptor(repository_exception):
    def __str__(self):
        return "No chatbot descriptor found"

class invalid_chatbot_descriptor(repository_exception):
    def __str__(self):
        return "An invalid chatbot description was found"
