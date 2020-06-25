import os
import random

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

user_strikes = {}

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    #The commands to search for
    GroovyBotCommands = [
        "-play",
        "-skip",
        "-seek",
        "-join",
        "-next",
        "-back",
        "-clear",
        "-pause",
        "-resume"
    ]

    #Responses to offenders
    TellingOffMessages = [
    	"PLACE COMMANDS IN THE RIGHT CHANNEL YOU FOOL ",
    	"are you serious right now ",
    	"NEE NAW NEE NAW POST IN THE RIGHT CHANNEL ",
    	"Hey! I'm a groovy police recruit! Please post in the right channel ",
    	"why don't you listen to me... im just trying to keep the peace ",
    	"RESPECT MY AUTHORITAH ",
    	"I'm 2 weeks away from retirement and I have to deal with your s**t ",
    	"-play police siren"
    ]

    #command is (hopefully) always the first thing in the message, so need to split and
    #access only the first word
    splitMessage = message.content.split()
    channel = message.channel.name

    
    if channel != "place-groovy-commands-here" and splitMessage:
	    name = message.author.name
	    printStrikeMessage = False

	    for command in GroovyBotCommands:
	    	if splitMessage[0] == command:
	    		#Users have three strikes, stored in a dictionary.
	    		if name in user_strikes.keys():
	    			user_strikes[name] += 1
	    			if user_strikes[name] >= 3:
	    				user_strikes[name] = 0
	    				printStrikeMessage = True
	    		#If a first offender, they are added to the dictionary
	    		else:
	    			user_strikes[name] = 1

	    		response = random.choice(TellingOffMessages) + name
    			await message.channel.purge(limit=1)

    			#prints the message depending on number of strikes
    			if printStrikeMessage:
	    			await message.channel.send("3 strikes " + name + "! Know what that means... nothing I haven't programmed a punishment yet")
	    		else:
    				await message.channel.send(response)

client.run(TOKEN)