"""
Various sample usages of the Alliance for Open Chatbot client utilities

Authors:
    - Amédée Potier (amedee.potier@konverso.ai) from Konverso

History:
    - 2020/11/02: Amédée: Initial version.

"""

if __name__ == '__main__':

    from openchatbotclient import client

    bot_konverso = client('https://callbot.konverso.ai', port=443, path='/api/ask')

    print(bot_konverso.base_url)

    response = bot_konverso.ask("amedee", "hello", lang="fr")
    print(response)

    #import sys
    #sys.exit(0)

    #
    # Use the Repository to retrieve a Client or a Descriptor
    #
    from openchatbotclient import repository
    repo = repository()

    bot_descriptor = repo.get_descriptor("openchatbot.io")
    print("Host: ", bot_descriptor.get_host())

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
    from openchatbotclient import client

    bot_konverso = client('https://callbot.konverso.ai', 443)

    bot_doungdoung = client('https://doungdoung.com', 443, path='/api/doungdoung/v1.0/ask')


    #
    # Now let's create a second bot, doing an explicit declaration
    #
    from openchatbotclient import client_group

    bots = client_group()
    bots.append(bot_alliance)
    bots.append(bot_konverso)
    bots.append(bot_doungdoung)

    #
    # Now query the group of bots..
    #
    responses = bots.ask("amedee", "hello", lang="en")
    print("Found response of size:", len(responses))

    # Print the first available response...
    response = responses.get_first()
    if response:
        print("Got first response from: ", response.get_client(), " : ", response.get_text())
    else:
        print("No response found !")

    # Or Print all the available responses:
    print("All reponses found:")
    print(responses.get_all_string(response_format=" - {client}: {text}", separator="\n"))

    # Or the one having the highest score
    # response = responses.get_with_max_score()
    # print("Got first response from: ", response)

    # You may also retrieve the descriptor of any client
    import json
    print(json.dumps(bot_konverso.get_descriptor(), indent=4))


