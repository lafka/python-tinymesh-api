import tinymesh

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

    class IO(APIResource):
        def __init__(self, **params):
            # @todo raise some kind of exception InvalidRequest??
            self['network'] = params['network']
            self['channel'] = params['channel']
            self._isOpen = False

        def open(self, auth, **params):

            url = self.resource_url(self)
            httpreq, resp = APIResource._get(self, url, auth=auth,
                                             stream=True, **params)

            self._isOpen = True
            self._resp = resp
            self._req = httpreq

            return (httpreq, resp)

        def iter(self, **params):
            return self._req.iter_lines(chunk_size=None, **params)

        @classmethod
        def class_url(cls, apibase=None):
            apibase = apibase if apibase is not None else tinymesh.apibase
            return "%s/%s" % (tinymesh.apibase, "_channels/io")

        def resource_url(self, source):
            # @todo should check if call is coming from ListableResource before
            #       assuming anything about keys
            if 'network' not in source:
                pass
            elif 'channel' not in source:
                pass
            else:
                baseurl = self.class_url()
                network = source['network']
                channel = source['channel']

                return "%s/%s/%s" % (baseurl, network, channel)
