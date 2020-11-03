"""A descriptor is a definition of a chatbot, in a JSON format such as:

   {'openchatbot':
       {'endpoint': '/api/v1.0/ask',
        'host': 'https://openchatbot.io',
        'port': 443,
        'methods': ['GET', 'POST']
        }
   }

This descriptor class wraps this JSON into a class instance that is easy
to manipulate and will manage the default values.

This descriptor may be found in enterprise web site, typically under the path:
    /.well-known/openchatbot-configuration
See the module "repository" which has utility methods to retrieve descriptors

A descriptor may be created manually, with a JSON as input:
   my_descriptor = descriptor(my_json_dict)

Alternatively, this descriptor may be found in enterprise web site, typically under the path:
    /.well-known/openchatbot-configuration

See the module "repository" which has utility methods to retrieve descriptors

"""

from openchatbotclient.exception import invalid_chatbot_descriptor

OPENCHATBOT_LABEL = 'openchatbot'
HOST_LABEL = 'host'
ENDPOINT_LABEL = 'endpoint'
PORT_LABEL = 'port'
METHODS_LABEL = 'methods'

ENDPOINT_DEFAULT = '/api/ask'
PORT_DEFAULT = 'port'
METHODS_DEFAULT = ['GET', 'POST']

class descriptor(dict):
    def __init__(self, data=None):
        super().__init__()
        if data:
            self.update(data)

    def get_host(self):
        try:
            return self[OPENCHATBOT_LABEL].get(HOST_LABEL)
        except KeyError:
            raise invalid_chatbot_descriptor()

    def get_endpoint(self):
        return self[OPENCHATBOT_LABEL].get(ENDPOINT_LABEL, ENDPOINT_DEFAULT)

    def get_port(self):
        return self[OPENCHATBOT_LABEL].get(PORT_LABEL, PORT_DEFAULT)

    def get_methods(self):
        return self[OPENCHATBOT_LABEL].get(METHODS_LABEL, METHODS_DEFAULT)

    def get_url(self):
        return '%s:%d%s' % (self.get_host(), self.get_port(), self.get_endpoint())
