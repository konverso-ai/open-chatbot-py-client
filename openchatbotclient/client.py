"""Client for Open Chat Bot.

   Example of usage:

        from openchatbotclient.client import Client

        # You may create a Client using the native constructor
        client = Client('bot.domain.com', 8443, path='api')
        response = client.ask("my-userId", "hello")

        # Or using a URL to the API
        client = Client.from_url("https://mybot.mydomain.com/api/v1/ask")
        response = client.ask("john.doe", "what is the weather today?")

   The 'ask' method will cause a GET request to be invoked, such as: 
        https://bot.domain.com:8443/api/ask
    with params:
        {'userId': 'my-userId', 'query': 'hello'}

Authors:
    - Alexander Danilov from Konverso
    - Amédée Potier (amedee.potier@konverso.ai) from Konverso

History:
    - 2019/11/01: Alexander: Initial class implementation
    - 2020/11/02: Amédée: Renaming class to "client"
    - 2020/11/02: Amédée: Adding the "from_descriptor" static method
    - 2020/12/15: Amédée: Adding the "from_url" static method
                          Adjusting names to be PEP8 compliants

"""

import json
import requests

from .descriptor import Descriptor, ENDPOINT_DEFAULT

from .exception import ChatbotServerError

class Client:
    def __init__(self, host: str, port: int = 0, path: str = None, descriptor: Descriptor = None, headers=None):
        """Create a client that may be queried. The constructor parameters are:
           - host: a host in the format protocol://domain, such as:
              https://konverso.ai
           - port: optional, only required if using none standard ports (i.e 8443 for example)
           - path: the endpoint, defaults to /api/ask
           - descriptor: optional, a descriptor instance

        See also the fromDescriptor method to get a client.
        """

        # Host is in format:
        # https://domain
        self.host = host

        self.hostname = self.host.rsplit("/", 1)[-1]

        if port:
            self.port = port
        elif self.host.startswith("https"):
            self.port = 443
        else:
            self.port = 80

        self.__path = path or ENDPOINT_DEFAULT
        if not self.__path.startswith("/"):
            self.__path = "/" + self.__path

        self._headers = {'Content-Type': 'application/json; charset=utf-8'}
        if headers:
            self._headers.update(headers)

        if descriptor:
            self.descriptor = descriptor
        else:
            self.descriptor = Descriptor({
                'openchatbot': {
                    'endpoint': self.__path,
                    'host': 'https://openchatbot.io',
                    'port': 443,
                    'methods': ['GET', 'POST']
                }
            })

        # The avatar may be used as a place holder for storing
        # the image associated with the bot. (REVIEW. Should be added to the alliance standard ?
        #
        self.avatar = None

    def __str__(self):
        # We extract the actual hostname.domain from the host
        # https://myhost.mydomain => myhost.mydomain
        #
        return "client('%s')" % self.hostname

    @staticmethod
    def from_descriptor(descriptor):
        """Given a "descriptor" instance, returns a new "client" instance"""

        # Import it here to avoid any cyclic import
        #from openchatbotclient.descriptor import descriptor

        assert isinstance(descriptor, Descriptor)

        return Client(host=descriptor.host,
                      port=descriptor.port,
                      path=descriptor.endpoint,
                      descriptor=descriptor)

    @staticmethod
    def from_url(url):
        """Given a URL pointing to the "ask" API, returns a new "client" instance"""

        # Extracting from the URL the protocol, the domain, the path
        # token0://token2/token3
        # protocol://domain/path
        #
        tokens = url.split("/", 3)

        protocol = tokens[0]
        domainport = tokens[2]

        # domain may potentially be in the form
        # domain:port
        #
        domainport_tokens = domainport.split(":")
        if len(domainport_tokens) == 1:
            domain = domainport_tokens[0]
            port = None
        else:
            domain, port = domainport_tokens

        path = tokens[3]

        return Client(host='%s//%s' % (protocol, domain),
                      port=port,
                      path=path)

    @property
    def base_url(self) -> str:
        """Returns the URL of the remote bot "ask" API web service,
            that is something like:
            http[s]://host.domain[:port]/path/to/api/ask
        """
        url = self.host

        if self.port:
            url += ":%d" % self.port

        if self.__path:
            url += "%s"%(self.__path)

        return url

    @staticmethod
    def __process_response(json_data: dict):
        status = json_data.get('status', {})
        code = status.get('code', 0)
        if code == 200:
            return json_data
        errorType = status.get('errorType', 'Unknown error')
        errorMsg = "%s: %s" % (errorType, str(json_data))
        raise ChatbotServerError(code, errorMsg)

    def get_descriptor(self):
        """Returns the related descriptor instance which may be posted for
           registering this bot on a domain
        """
        return self.descriptor

    @property
    def api_path(self):
        return self.__path

    def ask(self, userId: str, query: str, lang: str = None, location: str = None, method: str = 'get', timeout=None, headers=None, params = None):
        """Invoke request to bot and receive answer
           Input parameters:
            - userId : user's identifier
            - query : message to send to bot
            - lang : queries language
            - location : user's location
            - method : which method to user for processing (get or post).
                       'get' is default
          Output:
            - json with response data or exception
        """
        if not userId:
            raise RuntimeError("userId is empty")

        if not query:
            raise RuntimeError("Query is empty")

        # Params is the combination of mandatory params and extra ones optionally
        params = params or {}
        params.update({'userId': userId, 'query': query})

        # Headers may be updated for the request
        aggregated_headers = self._headers.copy()
        if headers:
            aggregated_headers.update(headers)
        
        if lang:
            params['lang'] = lang
        if location:
            params['location'] = location

        if method == 'get':
            #print(self.base_url)
            #print(params)
            r = requests.get("%s"%(self.base_url), params=params, headers=aggregated_headers, timeout=timeout, verify=False)
        elif method == 'post':
            r = requests.post("%s"%(self.base_url), data=json.dumps(params), headers=aggregated_headers, timeout=timeout, verify=False)
        else:
            raise RuntimeError("Unknown method '%s'"%(method))

        if r.status_code != 200:
            #print("Failed with headers: %s" % json.dumps(self._headers))
            #print("Failed with params: %s" % json.dumps(params))
            raise RuntimeError("Invalid response : code %s : %s" % (r.status_code, r.text))

        # Inner import to avoid cyclic include
        from . import Response
        #print(r)
        return Response(self, self.__process_response(r.json()))
