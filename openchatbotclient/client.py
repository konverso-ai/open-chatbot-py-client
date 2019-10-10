import json
import requests

class OpenChatBotError(Exception):
    """Exception for error response"""
    def __init__(self, status: int, description: str):
        self.status = status
        self.description = description

class OpenChatBotClient:
    """Client for Open Chat Bot.

       Example of usage:
            client = OpenChatBotClient('bot.domain.com', 8443, path='api')
            response = client.ask("my-userId", "hello")

       In this case next GET request will be invoked:
            https://bot.domain.com:8443/api/ask
        with params:
            {'userId': 'my-userId', 'query': 'hello'}

    """
    def __init__(self, host: str, port: int = 80, schema='https', path: str = None):
        self.host = host
        self.port = port
        self.schema = schema
        self.__path = path
        self._headers = {'Content-Type': 'application/json; charset=utf-8'}

    @property
    def base_url(self) -> str:
        url = "%s://%s:%d"%(self.schema, self.host, self.port)
        if self.__path:
            url += "/%s"%(self.__path)
        return url

    @staticmethod
    def __process_response(json_data: dict):
        status = json_data.get('status', {})
        code = status.get('code', 0)
        if code == 200:
            return json_data
        errorType = status.get('errorType', 'Unknown error')
        raise OpenChatBotError(code, errorType)

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
            response = requests.get("%s/ask"%(self.base_url), params=params)
        elif method == 'post':
            response = requests.post("%s/ask"%(self.base_url), data=json.dumps(params), headers=self._headers)
        else:
            raise RuntimeError("Unknown method '%s'"%(method))
        try:
            return self.__process_response(response.json())
        except json.decoder.JSONDecodeError:
            raise RuntimeError("Invalid response : %s"%(response.text))
