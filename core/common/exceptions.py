from fastapi_babel import _
from starlette import status


class MSBaseException(Exception):
    def __init__(self, status_code, message, **kwargs):
        self.code = status_code
        self.message = message
        self.kwargs = kwargs
        super().__init__(message, status_code)


class SystemException(MSBaseException):
    def __init__(
        self, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=None, **kwargs
    ):
        super().__init__(status_code, message or _("System error!"), **kwargs)


class ServiceException(MSBaseException):
    def __init__(
        self, status_code=status.HTTP_503_SERVICE_UNAVAILABLE, message=None, **kwargs
    ):
        super().__init__(status_code, message or _("Service error!"), **kwargs)


class NotFoundException(MSBaseException):
    def __init__(self, status_code=status.HTTP_404_NOT_FOUND, message=None, **kwargs):
        super().__init__(status_code, message or _("Not found!"), **kwargs)


class BadRequestException(MSBaseException):
    def __init__(self, status_code=status.HTTP_400_BAD_REQUEST, message=None, **kwargs):
        super().__init__(status_code, message or _("Bad request!"), **kwargs)

class UnAuthenticateException(MSBaseException):
    def __init__(
        self, status_code=status.HTTP_401_UNAUTHORIZED, message=None, **kwargs
    ):
        super().__init__(status_code, message or _("Un-Authentication!"), **kwargs)


class PermissionDeniedException(MSBaseException):
    def __init__(self, status_code=status.HTTP_403_FORBIDDEN, message=None, **kwargs):
        super().__init__(status_code, message or _("Permission Denied"), **kwargs)
