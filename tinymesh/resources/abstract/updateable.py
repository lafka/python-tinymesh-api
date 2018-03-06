from tinymesh.resources.abstract.resource import APIResource


class UpdateableResource(APIResource):
    @classmethod
    def update(cls, body, auth=None, apibase=None, filterkeys=[], **params):
        url = cls.resource_url(cls, apibase=apibase, source=body)

        for k in filterkeys:
            body.__delitem__(k)

        print("url: ", url, body)

        httpreq, resp = APIResource._put(cls, url, body, auth=auth)

        return cls._construct(resp._obj)
