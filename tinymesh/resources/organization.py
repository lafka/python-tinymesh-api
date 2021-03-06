from tinymesh.resources.abstract import CreateableResource
from tinymesh.resources.abstract import UpdateableResource
from tinymesh.resources.abstract import ListableResource


class Organization(CreateableResource, UpdateableResource, ListableResource):
    """
    API Resources related to networks
    """
