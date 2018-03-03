from tinymesh.resources.abstract.resource import APIResource


class ListableResource(APIResource):
    @classmethod
    def list(cls, auth=None, apibase=None, **params):
        url = cls.resource_url(cls, params, apibase=apibase)
        httpreq, resp = APIResource._get(cls, url, auth=auth)

        def reconstruct(_obj):
            return cls._construct(_obj, apibase=apibase)

        return list(map(reconstruct, resp._obj))
