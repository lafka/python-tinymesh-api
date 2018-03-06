import tinymesh
import json
import requests
import cgi
import logging
from tinymesh import error


class APIObject(dict):
    def __init__(self, key=None, last_response=None, apibase=None, **params):
        super(APIObject, self).__init__()

        self._apibase = apibase if apibase is not None else tinymesh.apibase

        self._unsaved_values = set()
        self._transient_values = set()
        self._last_response = last_response

        self._retrieve_params = params
        self._previous = None

        if key:
            self['key'] = key

    @property
    def last_response(self):
        return self._last_response

    def __setattr__(self, k, v):
        if k[0] == '_' or k in self.__dict__:
            return super(APIObject, self).__setattr__(k, v)

        self[k] = v
        return None

    def __getattr__(self, k):
        if k[0] == '_':
            raise AttributeError(k)

        try:
            return self[k]
        except KeyError as err:
            raise AttributeError(*err.args)

    def __delattr__(self, k):
        if k[0] == '_' or k in self.__dict__:
            return super(APIObject, self).__delattr__(k)
        else:
            del self[k]

    def __setitem__(self, k, v):
        # Allows for unpickling in Python 3.x
        if not hasattr(self, '_unsaved_values'):
            self._unsaved_values = set()

        self._unsaved_values.add(k)

        super(APIObject, self).__setitem__(k, v)

    def __getitem__(self, k):
        try:
            return super(APIObject, self).__getitem__(k)
        except KeyError as err:
            if k in self._transient_values:
                raise KeyError(
                    "%r.  HINT: The %r attribute was set in the past."
                    "It was then wiped when refreshing the object with "
                    "the result returned by Tiny Mesh's API, probably as a "
                    "result of a save().  The attributes currently "
                    "available on this object are: %s" %
                    (k, k, ', '.join(list(self.keys()))))
            else:
                raise err

    def __delitem__(self, k):
        super(APIObject, self).__delitem__(k)

        if hasattr(self, '_unsaved_values'):
            self._unsaved_values.remove(k)

    def __setstate__(self, state):
        self.update(state)

    @classmethod
    def _construct(cls, source, **kwargs):
        _obj = cls(source['key'], **kwargs)

        for k in source:
            _obj[k] = source[k]

        return _obj


class APIResource(APIObject):
    def _put(self, url, body, *arg, **kwargs):

        stream = kwargs.get('stream', False)

        headers = kwargs.get('headers', {})

        if body is not None:
            if not isinstance(body, str):
                body = json.dumps(body)
                headers['content-type'] = 'application/json'

        self._req = requests.put(url,
                                 *arg,
                                 data=body,
                                 headers=headers,
                                 **kwargs)

        if self._req.encoding is None:
            self._req.encoding = 'utf-8'

        mimetype, _opts = cgi.parse_header(self._req.headers['content-type'])

        if not stream and ('text/json' == mimetype
                           or 'application/json' == mimetype):
            self._obj = json.loads(self._req.text)

        if 200 == self._req.status_code:
            return self._req, self
        if 201 == self._req.status_code:
            return self._req, self
        elif 401 == self._req.status_code:
            raise error.AuthenticationError("Failed to authenticate request",
                                            self._req.text,
                                            self._req.status_code,
                                            self._obj,
                                            self._req.headers)
        else:
            raise error.APIError("POST: Unhandeled API Error\n\n%s"
                                 % (self._req.text),
                                 self._req.text,
                                 self._req.status_code,
                                 self._obj,
                                 self._req.headers)

    def _post(self, url, body, *arg, **kwargs):

        stream = kwargs.get('stream', False)

        headers = kwargs.get('headers', {})

        if body is not None:
            if not isinstance(body, str):
                body = json.dumps(body)
                headers['content-type'] = 'application/json'

        self._req = requests.post(url,
                                  *arg,
                                  data=body,
                                  headers=headers,
                                  **kwargs)

        if self._req.encoding is None:
            self._req.encoding = 'utf-8'

        mimetype, _opts = cgi.parse_header(self._req.headers['content-type'])

        if not stream and ('text/json' == mimetype
                           or 'application/json' == mimetype):
            self._obj = json.loads(self._req.text)

        if 200 == self._req.status_code:
            return self._req, self
        if 201 == self._req.status_code:
            return self._req, self
        elif 401 == self._req.status_code:
            raise error.AuthenticationError("Failed to authenticate request",
                                            self._req.text,
                                            self._req.status_code,
                                            self._obj,
                                            self._req.headers)
        else:
            raise error.APIError("POST: Unhandeled API Error\n\n%s"
                                 % (self._req.text),
                                 self._req.text,
                                 self._req.status_code,
                                 self._obj,
                                 self._req.headers)

    def _get(self, url, *arg, **args):
        self._req = requests.get(url, *arg, **args)

        if self._req.encoding is None:
            self._req.encoding = 'utf-8'

        headers = {}
        for k in self._req.headers:
            # Normalize headers
            headers[k.lower()] = self._req.headers[k]

        self._req.headers = headers

        contenttype = self._req.headers.get('content-type', "text/json")
        mimetype, _opts = cgi.parse_header(contenttype)
        transfer_encoding = self._req.headers.get('transfer-encoding', '')
        chunked = transfer_encoding.startswith('chunked')

        if not chunked and ('text/json' == mimetype
                            or 'application/json' == mimetype):
            self._obj = json.loads(self._req.text)
        else:
            self._obj = None

        if 200 == self._req.status_code:
            return self._req, self

        elif 400 == self._req.status_code:
            raise error.InvalidRequestError("Bad API Request: %s"
                                            % (self._obj['error'], ),
                                            self._req.text,
                                            self._req.status_code,
                                            self._obj,
                                            self._req.headers)

        elif 401 == self._req.status_code:
            raise error.AuthenticationError("Failed to authenticate request",
                                            self._req.text,
                                            self._req.status_code,
                                            self._obj,
                                            self._req.headers)

        elif 403 == self._req.status_code:
            raise error.PermissionError("Permission denied",
                                        self._req.text,
                                        self._req.status_code,
                                        self._obj,
                                        self._req.headers)

        else:
            raise error.APIError("GET: Unhandeled API Error\n\n%s"
                                 % (self._req.text),
                                 self._req.text,
                                 self._req.status_code,
                                 None,
                                 self._req.headers)

    @classmethod
    def class_name(cls):
        if cls == APIResource:
            raise NotImplementedError('Can\'t use abstract class. APIResource')

        return str(cls.__name__.lower())

    @classmethod
    def class_url(cls, apibase=None):
        cls_name = cls.class_name()

        return "%s/%s" % (apibase, cls_name,)

    def resource_url(self, key=None, apibase=None):
        """
        Build the URL to a Tiny Mesh Cloud Resource
        """
        if apibase is None:
            apibase = self._apibase

        base = self.class_url(apibase=apibase)

        if key is not None:
            return "%s/%s" % (base, key)
        else:
            return base
