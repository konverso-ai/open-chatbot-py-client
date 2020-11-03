# Open Chat Bot Client package
This package is designed to help you interface with any chatbot compliant on the 
Aliance for Open Chatbot standard. This package is designed for Python 3 environments.

This python package contains a number of small utilities to find, access and use these bots.

This implementation is based on the standard defined  by the Alliance in: 
<https://github.com/alliance-for-openchatbot/standard>

The Alliance web site is found at:
<https://www.alliance-open-chatbot.org/>

## Authors
Initial implementation made by Konverso in 2020
by  Alexander Danilov and Amedee Potier (<amedee.potier@konverso.ai>)

## License
This package is released under the MIT license. Consult the LICENSE file in this folder.

## Installation: 
This package may be installed using pip3 with the following commande:

    pip3 install -e git+https://bitbucket.org/konversoai/openchatbotclient.git#egg=AllianceForOpenChatBot

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

### Querying multiple bots

You can also work with multiple remotes bots, and collected group of responses. 
Let's demonstrate such usage. We first create a second bot, this time
doing an explicit declaration

    from openchatbotclient import client
    bot_konverso = client('https://callbot.konverso.ai', 443)

And then we can create a group with these two bots:

    from openchatbotclient import client_group

    bots = client_group()
    bots.append(bot_konverso)
    bots.append(bot_alliance)

We can easily send a user input to all bots in this group:

    responses = bots.ask("amedee", "hello", lang="en")
    print("Found response of size:", len(responses))

And then on the response_group object we get, we have various utilities to 
extract the content of interest from it:

Get one response:

    response = responses.get_first()
    if response:
        print("Got first response from: ", response.get_client(), " : ", response.get_text())
    else:
        print("No response found !")

Or Print all the available responses:

    print("All reponses found:")
    print(responses.get_all_string(response_format=" - {client}: {text}", separator="\n"))
