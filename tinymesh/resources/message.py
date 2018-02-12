from tinymesh.resources.abstract import CreateableResource


class Message(CreateableResource):
    """
    API Resources related to networks
    """

    def resource_url(self, source):
        if 'network' not in source:
            pass

        network = source['network']
        baseurl = self.class_url()

        """
        If device is not present, remote API will resolve based on content (ie,
        for broadcast messages or raw message containing address info).
        """
        if 'device' not in source:
            return "%s/%s" % (baseurl, network)
        else:
            device = source['device']
            return "%s/%s/%s" % (baseurl, network, device)
