from tinymesh.resources.abstract import APIResource
from tinymesh.resources.abstract import CreateableResource
from tinymesh.resources.abstract import UpdateableResource


class User(CreateableResource, UpdateableResource):
    """
    API Resources related to users
    """
