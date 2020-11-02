# Open Chat Bot Client package
This is package to help you interface with any chatbot compliant on the 
Aliance for Open Chatbot standard. 

This python package contains a number of small utilities to find, access and use these bots.


This implementation is based on the standard defined  by the Alliance in: 
<https://github.com/alliance-for-openchatbot/standard>

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

	from openchatbotclient import client 
	bot = client('https://callbot.konverso.ai', 443) 
	response = bot.ask("OPENBOT", "hello", method='post') 
	print(response) 

The response you get is a JSON using the standard Alliance format.

### Looking up an enterprise bot
The standard also includes the concept of bot registration. Companies may 
register their bot using a standard JSON descriptor under a well known URL path:

You may use the "repository" class to retrieve either a descriptor instance

    from openchatbotclient import repository
    repo = repository()

    bot_descriptor = repo.get_descriptor("openchatbot.io")
    print("Host: ", bot_descriptor.get_host())

Or directly a "client" instance on which you may then invoke numerous chat requests.

    bot = repo.get_client("openchatbot.io")
    print("Client: ", bot)

And you may then send chat text to these bots easily:

    response = bot.ask("OPENBOT", "hello", method='post')
    print(response)

