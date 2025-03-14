class RequiredInputError(Exception):
    def __init__(self, message):
        self._message = message
        
        
class InvalidInputError(Exception):
    def __init__(self, message):
        self._message = message


class RecordAlreadyExistError(Exception):
    def __init__(self, message):
        self._message = message


class RecordNotFound(Exception):
    def __init__(self, message):
        self._message = message


class AuthorizationError(Exception):
    def __init__(self, message, status = None, path = None):
        self._message = message
        self._status = status
        self._path = path
        

class SqlAlchemyError(Exception):
    def __init__(self, message, method):
        self._message = message
        self._method = method


class CrudOperatorError(Exception):
    def __init__(self, message, method):
        self._message = message
        self._method = method


class CrudOperatorErrorSerializer(Exception):
    def __init__(self, message, method):
        self._message = message
        self._method = method
    
    def serialize(self, path):
        return {
            "path": path,
            "message": self._message,
            "method": self._method
        }
        
        
class ErrorSerializer:
    def __init__(self, message):
        self._message = message
        
    def serialize(self, path):
        return {
            "path": path,
            "message": self._message
            
        }        