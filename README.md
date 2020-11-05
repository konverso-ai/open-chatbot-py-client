# Open Chat Bot Client package
This Python package contains utilities that allow you to find, access, and use the bots that are compliant with the Alliance for Open Chatbot standard. The package is designed for the Python 3 environments.  

The implementation is based on the standard defined by the Alliance.  
- The Alliance: <https://www.alliance-open-chatbot.org/>  
- The standard: <https://github.com/alliance-for-openchatbot/standard>  

## Authors
The initial implementation is made by Konverso in 2020 by Alexander Danilov and Amedee Potier (amedee.potier@konverso.ai).

## See also
- The API standard specifications: <https://github.com/alliance-for-openchatbot/standard>
- The definition of the standard bot descriptor: <https://openchatbot.io/domainbots>
- The easy-to-use web client that adds a widget connected to any chatbot to your website: <https://github.com/ohoachuck/openchatbot-webclient>

## License
This package is released under the MIT license. To learn more about it, view the `LICENSE` file in this folder.

## Installation 
You can install this package using pip3. To do so, run the following command:

    pip3 install -e git+https://github.com/konverso-ai/open-chatbot-py-client.git#egg=AllianceForOpenChatBot

## Usage notes 

### Getting a response from a chatbot
The sample below demonstrates how to get a chat local stub, send a sentence to it, and retrieve the bot response. 

	from openchatbotclient import client 
	bot = client('https://callbot.konverso.ai', 443) 
	response = bot.ask("john", "hello", lang="en") 
	print(response) 

The response you get is a JSON file using the standard Alliance format.

### Looking up an enterprise bot
The standard includes the concept of bot registration. Companies can register their bot with the help of a standard JSON descriptor that is available at the following link: `/.well-known/openchatbot-configuration`.   

Use the "repository" class to retrieve a descriptor instance:

    from openchatbotclient import repository
    repo = repository()

    bot_descriptor = repo.get_descriptor("openchatbot.io")
    print("Host: ", bot_descriptor.get_host())

Alternatively, you can use the "client" instance, where you can invoke multiple chat requests:

    bot = repo.get_client("openchatbot.io")
    print("Client: ", bot)

Then you can send chat text to these bots:

    response = bot.ask("john", "hello", lang="en")
    print(response)

### Querying multiple bots

You can interact with multiple remote bots and manage multiple responses. This use case is demonstrated in the sample below. 

1. Create a second bot. This time it is done by an explicit declaration:

```
from openchatbotclient import client
bot_konverso = client('https://callbot.konverso.ai', 443)
```

2. Create a group with these two bots:

``` 
from openchatbotclient import client_group

bots = client_group()
bots.append(bot_konverso)
bots.append(bot_alliance)
```

3. Send user input to all the bots in this group:

```
responses = bots.ask("amedee", "hello", lang="en")
print("Found response of size:", len(responses))
```

4. You get the `response_group` object. Now you can use utilities to extract the content of interest from this object.

Get one response:

```
response = responses.get_first()
   if response:
      print("Got first response from: ", response.get_client(), " : ", response.get_text())
   else:
      print("No response found !")
```

Print all available responses:
```
print("All reponses found:")
print(responses.get_all_string(response_format=" - {client}: {text}", separator="\n"))
```
