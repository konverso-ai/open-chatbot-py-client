"""Client for Open Chat Bot.

A Response represents a bot answer. It is typically obtained from:
    - client.ask

Or the extraction of one Response from a Response Group (obtained through client_group.ask).
The Response Group methods that would return a Response:
    - response_group.get_first()
    - response_group.get_with_max_score()

The response is effectively a JSON in a format such as:
{'response': {
    'query': 'hello',
    'userId': 'amedee',
    'timestamp': 1604337762.158837,
    'text': 'Hello Amedee, how can I help you?',
    'tts': ['Hello Amedee, how can I help you?'],
    'infoURL': '',
    'medias': [{'required_actions': [],
                 'suggested_actions': [{'format': 'button',
                                        'value': {'title': 'Help',
                                                  'onClick': '#do Help',
                                                  'displayedMessage': 'Kbot, show me help !'}},
                                       {'format': 'button',
                                        'value': {'title': 'Talk with an operator',
                                        'onClick': '#do Operator Talk',
                                        'displayedMessage': 'Kbot, I want to talk with an operator!'}},
                                       {'format': 'button',
                                        'value': {'title': 'View Display Capabilities',
                                                  'onClick': '#do Demo Components'
                                                  }
                                        }
                                       ]
                }],
    'context': [],
    'suggestions': []
    },
    'meta': {
        'version': '2020.15',
        'botIcon': 'https://callbot.konverso.ai/images/kbot_avatar.png\n',
        'botName': 'Kbot',
        'copyright': 'Copyright 2018 Konverso.',
        'authors': []
    },
    'status': {
        'code': 200,
        'status': 'success'
    }
}

The response object encapsulte a Client information, with a Response JSON, and
provides various utilities method to easily retrieve content out of the the JSON.

    resp = my_client.ask("my name", "my question", lang="en")

    # (cl is going to be the same object as my_client)²
    cl = resp.get_client()

    # Get a boolean indicating if a response was received.
    resp.is_success()

    # Easily get the actual response text:
    resp.get_text()

Authors:
    - Amédée Potier (amedee.potier@konverso.ai) from Konverso

History:
    - 2020/11/02: Amédée: Initial class implementation
"""

from . import client

class response:

    def __init__(self, cli: client, data: dict):
        """client is a client instance
           data is a json
        """
        self.cli = cli
        self.jso = data

    def __str__(self):
        return 'response(%s => %s)' % (self.cli, self.get_text())

    def get_client(self):
        """Returns an instance of 'client' class"""
        return self.cli

    def is_success(self):
        return self.jso.get('status', {}).get('status') == 'success'

    def get_text(self):
        return self.jso.get('response', {}).get('text', '')

    #
    # Set of utility properties to grab the most typical data
    # from the json
    #

    #
    # Related to the query:
    #
    @property
    def query(self) -> str:
        return self.jso.get('response', {}).get('query', '')

    @property
    def userId(self) -> str:
        return self.jso.get('response', {}).get('userId', '')

    #
    # Response data
    #
    @property
    def code(self) -> int:
        """The HTTP response code, such as 200"""
        return self.jso.get('status', {}).get('code', 0)

    @property
    def status(self) -> str:
        """The string 'success' if success"""
        return self.jso.get('status', {}).get('status', '')

    @property
    def text(self) -> str:
        """The textual response received"""
        return self.jso.get('response', {}).get('text', '')

    @property
    def botName(self) -> str:
        """The name of the remote bot"""
        return self.jso.get('meta', {}).get('botName', '')

    @property
    def botIcon(self) -> str:
        """The avatar of the remote bot, as a URL"""
        return self.jso.get('meta', {}).get('botIcon', '')


    #
    # Other useful metadata
    #
    @property
    def version(self) -> str:
        """The software version of the bot returning the response"""
        return self.jso.get('meta', {}).get('version', '')

    @property
    def copyright(self) -> str:
        """The copyright information of the bot returning the response"""
        return self.jso.get('meta', {}).get('copyright', '')

    @property
    def authors(self) -> list:
        """The authors of the bot returning the response"""
        return self.jso.get('meta', {}).get('authors', [])
