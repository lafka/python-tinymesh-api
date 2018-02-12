from tinymesh.resources.abstract.resource import APIResource


class CreateableResource(APIResource):
    @classmethod
    def create(cls, body, auth=None, **params):
        url = cls.resource_url(cls, params)
        httpreq, resp = APIResource._post(cls, url, body, auth=auth)

        return cls._construct(resp._obj)
