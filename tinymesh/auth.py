import hmac
from hashlib import sha256 as sha256
from base64 import b64encode
from requests.auth import HTTPBasicAuth, AuthBase

class APIAuth(AuthBase):
    @classmethod
    def authenticate(cls):
        if cls == APIAuth:
            raise NotImplementedError(
                """
                Can't use abstract class. APIAuth for request authentication.
                Use BasicAuth or TokenV1Auth classes instead.
                """)


class BasicAuth(APIAuth):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def authenticate(self, req):
        return HTTPBasicAuth(self.username, self.password)


class TokenV1Auth(APIAuth, AuthBase):
    def __init__(self, token):
        self.secret = token
        self.fingerprint = None

        if token is not None:
            self.fingerprint = sha256(token).hexdigest()

    def authenticate(self, req):
        return self

    def __call__(self, req):
        if self.secret is not None:
            payload = u"\n".join([req.method, req.url, req.body or u""])
            signature = hmac.new(self.secret, payload.encode('utf-8'), sha256)
            encoded = b64encode(signature.digest()).decode()

            req.headers['Authorization'] = self.fingerprint + " " + encoded

        return req
