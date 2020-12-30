"""
Various sample usages of the Alliance for Open Chatbot client utilities

Authors:
    - Amédée Potier (amedee.potier@konverso.ai) from Konverso

History:
    - 2020/11/02: Amédée: Initial version.

"""

if __name__ == '__main__':

    from openchatbotclient import Client


    # Create a client using its constructor  and query it
    bot_konverso = Client('https://callbot.konverso.ai', port=443, path='/api/ask')
    response = bot_konverso.ask("amedee", "hello", lang="fr")
    print(response)

    # Create a client using a URL pointing to its open chatbot API
    bot_konverso = Client.from_url('https://callbot.konverso.ai/api/ask')
    response = bot_konverso.ask("amedee", "hello you", lang="fr")
    print(response)

    #
    # Use the Repository to retrieve a Client or a Descriptor
    #
    from openchatbotclient import Repository
    repo = Repository()

    print("EDF Descriptor: ", str(repo.get_descriptor("kwalys.com")))

    bot_kwalys = repo.get_client("kwalys.com")
    response = bot_kwalys.ask("amedee", "hello", lang="fr")
    print("EDF replies: ", response.text)

    bot_descriptor = repo.get_descriptor("openchatbot.io")
    print("Descriptor: ", bot_descriptor)
    print("Host: ", bot_descriptor.host)

    bot_alliance = repo.get_client("openchatbot.io")
    print("Client: ", bot_alliance)


    print("Client API URL: ", bot_alliance.base_url)

    #
    # Send a chat message to a Client and get a JSON response
    #
    response = bot_alliance.ask("amedee", "hello", method='post')
    print(response)

    #
    # Now let's create more bots, doing explicit declarations
    #
    from openchatbotclient import Client

    bot_konverso = Client('https://callbot.konverso.ai', 443)

    bot_doungdoung = Client('https://doungdoung.com', 443, path='/api/doungdoung/v1.0/ask')


    #
    # Now let's create a second bot, doing an explicit declaration
    #
    from openchatbotclient import ClientGroup

    bots = ClientGroup()
    bots.append(bot_alliance)
    bots.append(bot_konverso)
    bots.append(bot_doungdoung)

    #
    # Now query the group of bots..
    #
    print("\n\n#### Sending 'hello' to a group of three bots")
    responses = bots.ask("amedee", "hello", lang="en")

    # Print the first available response...
    response = responses.get_first()
    if response:
        print("Got first response from: ", response.client, " : ", response.text)
    else:
        print("No response found !")

    # Or Print all the available responses:
    print("All reponses found:")
    print(responses.get_all_string(response_format=" - {client}: {text}", separator="\n"))

    # Or the one having the highest score
    # response = responses.get_with_max_score()
    # print("Got first response from: ", response)

    # You may also retrieve the descriptor of any client
    print("\n\n#### Generating a JSON descriptor for a bot")
    import json
    print(json.dumps(bot_konverso.descriptor, indent=4))

    #print("\n\n#### Testing wikipedia")
    #bot_doungdoung = Client.from_url('https://doungdoung.com/api/wikipedia/v1.0/ask')
    #response = bot_doungdoung.ask("amedee", "hello", lang="fr")
    #print("Wikipedia says: %s", response.text)

    bot_kwalys = repo.get_client("kwalys.com")
    response = bot_kwalys.ask("amedee", "hello", lang="fr")
    print("EDF replies: ", response.text)
