

class NotAcceptable406Error(Exception):
    def __str__(self):
        return "given data is not acceptible"

class AnuthenticationFail401Error(Exception):
    def __str__(self):
        return "login failed"

class NotFound404Error(Exception):
    def __str__(self):
        return "Server returned 404 error"

class ForbiddenRequestError(Exception):
    def __str__(self):
        return "Forbidden request"
