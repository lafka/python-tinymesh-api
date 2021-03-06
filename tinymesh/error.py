class TinymeshHTTPError(Exception):

    def __init__(self,
                 message=None,
                 http_body=None,
                 http_status=None,
                 json_body=None, headers=None):

        super(TinymeshHTTPError, self).__init__(message)

        self._message = message
        self.http_body = http_body
        self.http_status = http_status
        self.json_body = json_body
        self.headers = headers
        self.request_id = self.headers.get('request-id', None)

    def __unicode__(self):
        if self.request_id is not None:
            msg = self._message or "(undefined message)"
            return u"Request {0}: {1}".format(self.request_id, msg)
        else:
            return self._message

    def __str(self):
        return self.__unicode__()


class APIError(TinymeshHTTPError):
    pass


class InvalidRequestError(TinymeshHTTPError):
    pass


class AuthenticationError(TinymeshHTTPError):
    pass


class PermissionError(TinymeshHTTPError):
    pass


class NotFoundError(TinymeshHTTPError):
    pass
