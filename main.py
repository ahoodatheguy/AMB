import music
import nextcord
from nextcord import client
from nextcord.ext import commands

client = commands.Bot(command_prefix='!')

cogs = [music]
for cog in cogs:
	cog.setup(client)




client.run('YOUR TOKEN HERE')