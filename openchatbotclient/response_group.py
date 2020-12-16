"""Client for Open Chat Bot.

A response group represents a set of responses received from a number of bots
for a given sentence. It is typically created as a result of the invokation of:
    client_group.ask

Depending on your objectives, the Response Group may provide useful utilities to get
a random, or top score response, or some kind of fallback mechanism.

Authors:
    - Amédée Potier (amedee.potier@konverso.ai) from Konverso

History:
    - 2020/11/02: Amédée: Initial class implementation
"""

from .response import Response

class ResponseGroup(list):

    def append(self, response: Response):
        assert isinstance(response, Response)
        super().append(response)

    def get_first(self):
        """returns the first non empty Response or None of no Response was found

           Useful method to get results based on priorities. Get a priority ordered
           list of clients, get your responses using the client_group.ask

           Call this get_first to get the first response available...
        """

        for r in self:
            return r

    def get_all_string(self, response_format="{client}: {text}", separator="\n"):
        """returns a unique string representing the overall result

           format is an option text formatting that will be used to render each Response
           The following format variables are allowed:
           - client: the client name
           - text: the textual response
        """
        content_list = []
        for response in self:
            content = response_format.format(client=str(response.client),
                                             text=str(response.text))
            content_list.append(content)

        return separator.join(content_list)

    # Add when we have score
    #
    #def get_with_max_score(self):
    #    if not self:
    #        return None
    #    s = sorted(self, lambda x: x.get("score", 0))
    #    return s[-1]
