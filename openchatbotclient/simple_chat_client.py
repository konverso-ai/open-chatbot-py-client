"""
Various sample usages of the Alliance for Open Chatbot client utilities

Authors:
    - Amédée Potier (amedee.potier@konverso.ai) from Konverso

History:
    - 2020/11/02: Amédée: Initial version.

"""

import sys

if __name__ == '__main__':

    user_name = sys.argv[-1]

    from openchatbotclient import Client

    # Create a client using its constructor  and query it
    bot_konverso = Client('https://myhost.konverso.ai',
                          port=443,
                          path='/api/ask')

    print("Starting conversation with %s" % str(bot_konverso))
    print("Use 'Ctrl D' to stop")
    while True:
        try:
            user_input = input("You> ")
        except EOFError:
            print()
            break

        if not user_input:
            continue
        response = bot_konverso.ask(user_name, user_input, lang="en")
        print("Bot> %s" % response.text)
