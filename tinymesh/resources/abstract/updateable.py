from tinymesh.resources.abstract.resource import APIResource


class UpdateableResource(APIResource):
    @classmethod
    def update(self):
        return self
