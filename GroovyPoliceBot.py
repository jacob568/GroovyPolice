import os
import random

import discord
import constants

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
	for guild in client.guilds:
		if guild.name == GUILD:
			for voice_channel in guild.voice_channels:
				if voice_channel.name == "GroovyJail":
					print(
						f'{client.user} is connected to the following guild:\n'
						f'{guild.name}(id: {guild.id})'
					)

#{name: strikeInt}
user_strikes = {}

#Applies a strike to a user who commited an offense
#Returns true if the third strike is reached
def ApplyStrike(offender):
	if offender in user_strikes.keys():
		user_strikes[offender] += 1
		if user_strikes[offender] >= 3:
			#Move to groovy jail

			user_strikes[offender] = 0
			return True
	else:
		user_strikes[offender] = 1
		return False

@client.event
async def on_message(message):
	if message.author == client.user:
		return

    #the groovy bot command is (hopefully) always the first thing in a message, so need to split and
    #access only the first word
	splitMessage = message.content.split()
	channel = message.channel.name
	name = message.author.name
	printStrikeMessage = False
	response = ""

	#Checks the groovy commands channel for messages that aren't groovy commands
	if channel == constants.GROOVYCHANNEL and splitMessage:
		if splitMessage[0] not in constants.GROOVYBOTCOMMANDS:
			await message.delete()
			response = random.choice(constants.TELLINGOFFMESSAGES) + name
			printStrikeMessage = ApplyStrike(name)
		if printStrikeMessage:
			await message.channel.send("3 strikes " + name + "! Know what that means... nothing I haven't programmed a punishment yet")
		else:
			await message.channel.send(response)
	#Checks for groovy commands in non groovy channels
	if channel != constants.GROOVYCHANNEL and splitMessage:
		for command in constants.GROOVYBOTCOMMANDS:
			if splitMessage[0] == command:
				#Users have three strikes, stored in a dictionary.
				printStrikeMessage = ApplyStrike(name)
				response = random.choice(constants.TELLINGOFFMESSAGES) + name
				await message.delete()
				#prints the message depending on number of strikes
				if printStrikeMessage:
					#need to find the groovy jail channel
					for channel in message.guild.voice_channels:
						if channel.name == constants.GROOVYJAIL:
							await message.author.move_to(channel)
							break

					await message.channel.send("3 strikes " + name + "! You're going to GroovyJail, PUNK")
				else:
					await message.channel.send(response)

    
client.run(TOKEN)