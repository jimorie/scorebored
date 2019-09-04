from aioli.exceptions import AioliException


class ConflictException(AioliException):
    def __init__(self, message="Conflict"):
        super(ConflictException, self).__init__(status=409, message=message)
