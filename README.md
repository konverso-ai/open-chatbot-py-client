# Open Chat Bot Client package
This is package for Open Chat Bot client. Contains simple utility to access and use bots compliant with the Alliance for Open Chatbot standard.

## Authors
Initial implementation by Konverso in 2020
by  Alexander Danilov and Amedee Potier (<amedee.potier@konverso.ai>)

## License
This package is released under the MIT license. Consult the LICENSE file in this folder.

## Installation: 
This package may be installed using pip3 with the following commande:

## Usage notes: 

### Getting a response from a chatbot
Below is sample code to get a chat local stub, send a sentence to it and retrieve the bot response. 
	from openchatbotclient import OpenChatBotClient	
	client = OpenChatBotClient('dev02.konverso.ai', 8443, path='api')
	response = client.ask("OPENBOT", "hello", method='post')
	print(response)
The response you get is a JSON using the standard Alliance format.
