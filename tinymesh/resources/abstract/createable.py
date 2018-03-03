from tinymesh.resources.abstract.resource import APIResource


class CreateableResource(APIResource):
    @classmethod
    def create(cls, body, auth=None, apibase=None, **params):
        url = cls.resource_url(cls, params, apibase=apibase)
        httpreq, resp = APIResource._post(cls, url, body, auth=auth)

        return cls._construct(resp._obj)
