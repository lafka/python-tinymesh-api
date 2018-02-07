from tinymesh.resources.abstract import ReadableResource
from tinymesh.resources.abstract import CreateableResource
from tinymesh.resources.abstract import UpdateableResource
from tinymesh.resources.abstract import ListableResource


class Device(ReadableResource,
             CreateableResource,
             UpdateableResource,
             ListableResource):
    """
    API Resources related to devices
    """
