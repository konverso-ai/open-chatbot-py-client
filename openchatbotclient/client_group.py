"""Client for Open Chat Bot.

A client group is a list of clients. This may be used to send a given
user query to a number of bots and retrieve all results, typically
to get the higher rank answer, or to compare the various performances, etc.

Authors:
    - Amédée Potier (amedee.potier@konverso.ai) from Konverso

History:
    - 2020/11/02: Amédée: Initial class implementation
"""

from .client import Client
from .response_group import ResponseGroup

class ClientGroup(list):

    def append(self, client):
        assert isinstance(client, Client)
        super().append(client)

    def ask(self, userId: str, query: str, lang: str = None, location: str = None, method: str = 'get'):
        """Invoke request to each of the bots in the group
           and returns an aggregated answer. Not that errors are ignored...
           The result is a simple list of the valid JSON received.

           Returns an instance of response_group
        """

        json_result_list = ResponseGroup()

        for client in self:
            try:
                json_result = client.ask(userId=userId, query=query, lang=lang, location=location, method=method)
            except Exception as e:
                print("Got error sending request to %s (API '%s'): %s" % (client, client.base_url, e))
            else:
                json_result_list.append(json_result)

        return json_result_list
