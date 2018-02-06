from tinymesh.resources.abstract import APIResource
from tinymesh.resources.abstract import CreateableResource
from tinymesh.resources.abstract import UpdateableResource
from tinymesh.resources.abstract import ListableResource


class Channel(CreateableResource,
              UpdateableResource,
              ListableResource):
    """
    API Resources related to channel operations
    """
