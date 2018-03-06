from tinymesh.resources.abstract.resource import APIResource


class ReadableResource(APIResource):
    @classmethod
    def read(cls, key, auth=None, apibase=None, source={}, **kwargs):
        url = cls.resource_url(cls, apibase=apibase, source=source)
        httpreq, resp = APIResource._get(cls, url, auth=auth)
        return cls._construct(resp._obj)
