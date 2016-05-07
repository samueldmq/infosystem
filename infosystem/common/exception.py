
class InfoSystemException(Exception):

    status = 500
    message = ''    


class NotFound(InfoSystemException):

    status = 404
    message = 'Entity not found'

