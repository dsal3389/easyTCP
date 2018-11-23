

class NotFound404Error(Exception):
    def __str__(self):
        return "Server returned 404 error"

class ForbiddenRequestError(Exception):
    def __str__(self):
        return "Forbidden request"
