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

    def resource_url(self, source=None):
        # @todo should check if call is coming from ListableResource before
        #       assuming anything about keys
        baseurl = self.class_url()

        if 'network' in source:
            return "%s/%s" % (baseurl, source['network'])
        else:
            return baseurl
