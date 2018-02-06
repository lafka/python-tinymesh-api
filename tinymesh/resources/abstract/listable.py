from tinymesh.resources.abstract.resource import APIResource


class ListableResource(APIResource):
    @classmethod
    def list(cls, auth=None, **params):
        url = cls.class_url()
        httpreq, resp = APIResource._get(cls, url, auth=auth, **params)

        def reconstruct(_obj):
            return cls._construct(_obj)

        return list(map(reconstruct, resp._obj))
