"""Client for Open Chat Bot.

       Example of usage:
            from openchatbotclient.client import client
            myclient = client('bot.domain.com', 8443, path='api')
            response = myclient.ask("my-userId", "hello")

       In this case next GET request will be invoked:
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
"""

import json
import requests

from .descriptor import descriptor, ENDPOINT_DEFAULT

from .exception import chatbot_server_error

class client:
    def __init__(self, host: str, port: int = 0, path: str = None, desc: descriptor = None):
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

        self.port = port
        self.__path = path or ENDPOINT_DEFAULT
        if not self.__path.startswith("/"):
            self.__path = "/" + self.__path

        self._headers = {'Content-Type': 'application/json; charset=utf-8'}

        if desc:
            self.descriptor = desc
        else:
            self.descriptor = descriptor({
                'openchatbot': {
                    'endpoint': self.__path,
                    'host': 'https://openchatbot.io',
                    'port': 443,
                    'methods': ['GET', 'POST']
                }
            })

    def __str__(self):
        # We extract the actual hostname.domain from the host
        # https://myhost.mydomain => myhost.mydomain
        #
        return "client('%s')" % self.host.rsplit("/", 1)[-1]

    @staticmethod
    def from_descriptor(desc):
        """Given a "descriptor" instance, returns a new "client" instance"""

        # Import it here to avoid any cyclic import
        #from openchatbotclient.descriptor import descriptor

        assert isinstance(desc, descriptor)

        return client(host=desc.get_host(),
                      port=desc.get_port(),
                      path=desc.get_endpoint(),
                      desc=desc)

    @property
    def base_url(self) -> str:
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
        raise chatbot_server_error(code, errorType)

    def get_descriptor(self):
        """Returns the related descriptor instance which may be posted for 
           registering this bot on a domain
        """
        return self.descriptor

    def ask(self, userId: str, query: str, lang: str = None, location: str = None, method: str = 'get'):
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

        params = {'userId': userId, 'query': query}
        if lang:
            params['lang'] = lang
        if location:
            params['location'] = location

        if method == 'get':
            r = requests.get("%s"%(self.base_url), params=params)
        elif method == 'post':
            r = requests.post("%s"%(self.base_url), data=json.dumps(params), headers=self._headers)
        else:
            raise RuntimeError("Unknown method '%s'"%(method))
        try:
            from . import response
            return response(self, self.__process_response(r.json()))
        except json.decoder.JSONDecodeError:
            raise RuntimeError("Invalid response : %s"%(r.text))
