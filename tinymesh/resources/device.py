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

    def resource_url(self, source=None, apibase=None, **kwargs):
        """
        Get the full url for resource
        """
        # @todo should check if call is coming from ListableResource before
        #       assuming anything about keys
        if apibase is None:
            apibase = self._apibase

        baseurl = self.class_url(apibase=apibase, **kwargs)

        network = source.get('network')

        if 'key' in source:
            key = source['key']
            return "%s/%s/%s" % (baseurl, network, key)
        else:
            return "%s/%s" % (baseurl, network)
