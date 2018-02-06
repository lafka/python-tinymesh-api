from tinymesh.resources.abstract.resource import APIResource

class CreateableResource(APIResource):
    @classmethod
    def create(cls, auth=None, **params):
        pass
