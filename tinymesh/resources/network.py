from tinymesh.resources.abstract import APIResource
from tinymesh.resources.abstract import CreateableResource
from tinymesh.resources.abstract import UpdateableResource
from tinymesh.resources.abstract import ListableResource


class Network(CreateableResource, UpdateableResource, ListableResource):
    """
    API Resources related to networks
    """
