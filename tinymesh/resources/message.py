import tinymesh
from tinymesh.resources.abstract import APIResource, CreateableResource


class Message(CreateableResource):
    """
    API Resources related to messages
    """

    class Query(APIResource):
        """
        Class to query message store"
        """
        def __init__(self, **params):
            # @todo raise some kind of exception InvalidRequest??
            self['network'] = params['network']
            self['device'] = params.get('device', None)
            self._isOpen = False

        def query(self, auth,
                  apibase=None,
                  stream=False,
                  continuous=False,
                  data_encoding='hex',
                  date_from=None,
                  date_to=None,
                  sort_by='datetime',
                  sort_order='descending',
                  **kwargs):
            """
            Perform a streaming query
            """

            stream = kwargs.get('stream', True)

            query = {
                'data.encoding': data_encoding,
                'stream': "true" if stream else "false",
                'continuous': "true" if continuous else "false",
                'sort.by': sort_by,
                'sort.order': sort_order
            }

            if date_from is not None:
                query['date.from'] = date_from

            if date_to is not None:
                query['date.to'] = date_to

            url = self.resource_url(self, apibase=apibase)
            httpreq, resp = APIResource._get(self, url, auth=auth,
                                             stream=stream, params=query,
                                             **kwargs)

            self._isOpen = True
            self._resp = resp
            self._req = httpreq

            return (httpreq, resp)

        def iter(self, **params):
            return self._req.iter_lines(chunk_size=None, **params)

        @classmethod
        def class_url(cls, apibase=None):
            if apibase is None:
                apibase = tinymesh.apibase

            return "%s/%s" % (apibase, "messages")

        def resource_url(self, source=None, apibase=None, **kwargs):
            """
            Build the query URL
            """
            if 'network' in source and source['network'] is not None:
                baseurl = self.class_url(apibase=apibase)
                network = source['network']

                if 'device' in source and source['device'] is not None:
                    device = source['device']
                    return "%s/%s/%s" % (baseurl, network, device)
                else:
                    return "%s/%s" % (baseurl, network)
            else:
                pass

    def resource_url(self, source=None, apibase=None):
        if 'network' not in source:
            pass

        network = source['network']
        baseurl = self.class_url(apibase=apibase)

        """
        If device is not present, remote API will resolve based on content (ie,
        for broadcast messages or raw message containing address info).
        """
        if 'device' not in source:
            return "%s/%s" % (baseurl, network)
        else:
            device = source['device']
            return "%s/%s/%s" % (baseurl, network, device)
