from tinymesh.resources.abstract.resource import APIResource


class ReadableResource(APIResource):
    @classmethod
    def read(cls, key, auth=None, **params):
        url = cls.resource_url(cls, key)
        httpreq, resp = APIResource._get(cls, url, auth=auth, **params)
        return cls._construct(resp._obj)
