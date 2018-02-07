import tinymesh
import json
import requests
import cgi


class APIObject(dict):
    def __init__(self, key=None, last_response=None, **params):
        super(APIObject, self).__init__()

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
    def _construct(cls, source):
        _obj = cls(source['key'])

        for k in source:
            _obj[k] = source[k]

        return _obj


class APIResource(APIObject):

    def _get(self, url, *arg, **args):
        self._req = requests.get(url, *arg, **args)

        mimetype, _opts = cgi.parse_header(self._req.headers['content-type'])

        if 'text/json' == mimetype or 'application/json' == mimetype:
            self._obj = json.loads(self._req.text)

        return self._req, self

    @classmethod
    def class_name(cls):
        if cls == APIResource:
            raise NotImplementedError('Can\'t use abstract class. APIResource')

        return str(cls.__name__.lower())

    @classmethod
    def class_url(cls):
        cls_name = cls.class_name()
        return tinymesh.apibase + "/v2/%s" % (cls_name,)

    def resource_url(self, key=None):
        base = self.class_url()

        if key is not None:
            return "%s/%s" % (base, key)
        else:
            return base
