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

    def resource_url(self, source=None):
        # @todo should check if call is coming from ListableResource before
        #       assuming anything about keys
        if source is not None and 'network' in source:
            baseurl = self.class_url()

            if 'key' in source:
                return "%s/%s/%s" % (baseurl, source['network'], source['key'])
            else:
                return "%s/%s" % (baseurl, source['network'])
        else:
            return self.class_url()
