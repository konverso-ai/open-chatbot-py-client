"""
    Companies running bots compliants with the Alliance for Open Chatbot specifications
    may advertise their bots by posting details about them using a file
    descriptor located in a well know path:

        https://domain/.well-known/openchatbot-configuration

Authors:
    - Amédée Potier (amedee.potier@konverso.ai) from Konverso

History:
    - 2020/11/02: Amédée: Initial version.

"""

import json
import requests


from .exception import NoChatbotDescriptorError, InvalidChatbotDescriptorError

from .descriptor import Descriptor


DESCRIPTOR_PATH = "/.well-known/openchatbot-configuration"

class Repository:
    def __init__(self):
        pass

    def get_descriptor_url(self, domain):
        return "https://%s%s" % (domain, DESCRIPTOR_PATH)

    def get_descriptor(self, domain, headers=None, data=None, auth=None):
        """Given a particular domain, attempts to retrieve the related
           descriptor
        """

        url = self.get_descriptor_url(domain)
        r = requests.get(url, headers=headers, data=data, auth=auth, verify=False)

        if r is None:
            raise NoChatbotDescriptorError()

        if r.status_code in (200, 201, 202, 204, 206):
            # We have a response.. let's validate this is a valid JSON
            try:
                j = json.loads(r.content)
                return Descriptor(j)
            except:
                # Invalid content
                raise InvalidChatbotDescriptorError()

        raise NoChatbotDescriptorError()

    def get_client(self, domain, headers=None, data=None, auth=None):
        """Given a particular domain, attempts to retrieve the related
           descriptor
        """

        # Retrieve the descriptor for this domain
        desc = self.get_descriptor(domain, headers=headers, data=data, auth=auth)

        # And build the client stub for it
        # Inner include to avoid any risk of cyclic imports
        from .client import Client
        return Client.from_descriptor(desc)

#
# Sample code, validating the bots of the members of the Alliance for Open Chatbot.
#
if __name__ == '__main__':
    repo = Repository()

    for d in ("www.konverso.ai", "www.proxem.com", "www.kwalys.com", "phebe.io", "synapse-developpement.fr", "openchatbot.io"):

        print("================================")
        print("Testing domain %s" % d)
        print(repo.get_descriptor_url(d))
        print("================================")

        try:
            response = repo.get_descriptor(d)
        except Exception as e:
            print("Failed due to: %s" % e)
        else:
            print(response)
