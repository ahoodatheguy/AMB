import nextcord
from nextcord.ext import commands

import youtube_dl


class music(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command()
	async def join(self, ctx):
		if ctx.author.voice is None:  # If the user is not in a voice channel.
			await ctx.reply('You are not in a voice channel!')
		else:
			channel = ctx.author.voice.channel  # Get the channel of the user

			if ctx.voice_client is None:  # If the bot is not already in a voice channel
				await channel.connect()   # Join it
				await ctx.send(f'Joined {channel}.')

			elif ctx.voice_client.channel is channel:          # If the bot is in the same channel as the user
				await ctx.reply(f'Already in {channel}')       # Tell the user there is no need for the join command.

			else:                                              # If the bot is in a different channel.
				await ctx.voice_client.move_to(channel)        # Move to it.
				await ctx.send(f'Moved to {channel}.')
	
	@commands.command()
	async def stop(self, ctx):
		await ctx.send(f'Leaving {ctx.voice_client.channel}.')
		await ctx.voice_client.disconnect()

	@commands.command()
	async def play(self, ctx, url):
		ctx.voice_client.stop()
		
		FFMPEG_OP = {
			'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
			'options': '-vn'
			}
		YDL_OP = {'format':'bestaudio'}

		vc = ctx.voice_client

		with youtube_dl.YoutubeDL(YDL_OP) as ydl:
			info = ydl.extract_info(url, download=False)
			url2 = info['formats'][0]['url']
			source = await nextcord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OP)
			vc.play(source)

	@commands.command()
	async def pause(self, ctx):
		await ctx.voice_client.pause()
		await ctx.reply('Paused!')
	@commands.command()
	async def resume(self, ctx):
		await ctx.voice_client.resume()
		await ctx.reply('Resuming!')

def setup(client):
	client.add_cog(music(client))
