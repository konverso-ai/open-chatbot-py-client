# Open Chat Bot Client package


#Authors
Initial implementation by Konverso in 2020
with Alexander Danilov and Amedee Potier (<amedee.potier@konverso.ai>)

This is package for Open Chat Bot client.

#Installation: 

#Usage notes: 
Below is sample code to get a chat local stub, send a sentence to it and retrieve the bot response. 
	from openchatbotclient import OpenChatBotClient
	
	client = OpenChatBotClient('dev02.konverso.ai', 8443, path='api')
	response = client.ask("OPENBOT", "hello", method='post')
	print(response)
The response you get is a JSON using the standard Alliance format.
