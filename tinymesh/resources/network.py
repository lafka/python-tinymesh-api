from tinymesh.resources.abstract import ReadableResource
from tinymesh.resources.abstract import CreateableResource
from tinymesh.resources.abstract import UpdateableResource
from tinymesh.resources.abstract import ListableResource


class Network(ReadableResource,
              CreateableResource,
              UpdateableResource,
              ListableResource):
    """
    API Resources related to networks
    """
