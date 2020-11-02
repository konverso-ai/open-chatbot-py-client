"""
Various sample usages of the Alliance for Open Chatbot client utilities

Authors:
    - Amédée Potier (amedee.potier@konverso.ai) from Konverso

History:
    - 2020/11/02: Amédée: Initial version.

"""

if __name__ == '__main__':

    from openchatbotclient import repository
    repo = repository()

    bot_descriptor = repo.get_descriptor("openchatbot.io")
    print("Host: ", bot_descriptor.get_host())

    bot = repo.get_client("openchatbot.io")
    print("Client: ", bot)


    print("Client API URL: ", bot.base_url)

    response = bot.ask("OPENBOT", "hello", method='post') 
    print(response)
