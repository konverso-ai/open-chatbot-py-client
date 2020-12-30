"""
Open Chat Bot Client package
============================

This Python package contains utilities that allow you to find, access, and use bots that are compliant with the Alliance for Open Chatbot standard. The package is designed for the Python 3 environments.

The Open Chatbot standard
-------------------------

The implementation is based on the standard defined by the Alliance.
 - The Alliance: https://www.alliance-open-chatbot.org/
 - The standard: https://github.com/alliance-for-openchatbot/standard

Authors
-------

The initial implementation is made by Konverso in 2020 by Alexander Danilov and Amedee Potier (amedee.potier@konverso.ai).

See also
--------

 - The API standard specifications:
       https://github.com/alliance-for-openchatbot/standard
 - The definition of the standard bot descriptor:
       https://openchatbot.io/domainbots
 - The easy-to-use web client that adds a widget connected to any chatbot to your website:
       https://github.com/ohoachuck/openchatbot-webclient

License
-------

This package is released under the MIT license. To learn more about it, view the LICENSE file in this folder.

Usage
-----

To get started, either view the test.py file in this module, or consult the help on the client module:

    from openchatbotclient import client
    help(client)

You may also find complete examples and tutorials in the related GitHub repository:
    https://github.com/konverso-ai/open-chatbot-py-client

"""

from .client import Client
from .descriptor import Descriptor
from .repository import Repository
from .response import Response
#from .response_group import ResponseGroup

from .client_group import ClientGroup
