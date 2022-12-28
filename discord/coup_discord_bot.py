import discord
import os
from dotenv import load_dotenv
load_dotenv()

class CoupDiscordBot:
	_discord_client = None
	name = 'Coup'
	def __init__(self) -> None:
		self._discord_client = discord.Client(
			intents=discord.Intents(messages=True, guilds=True)
		)

	def run(self) -> None:
		pass

	def start(self, loop):
		@self._discord_client.event
		async def on_ready():
			print(f'Logged in as {self._discord_client.user}!')
		
		@self._discord_client.event
		async def on_message(message):
			await self.on_message_create(message)
		
		loop.create_task(self._discord_client.start(os.environ.get('DISCORD_TOKEN')))

	# This function will fire whenever there is a new message in Discord
	async def on_message_create(self, message):
		# Look for messages tagging this bot and respond
		did_mention_this_user = list(filter(lambda member: member.name == self.name, message.mentions))
		if did_mention_this_user:
			await self.reply(message)

	async def reply(self, message):
		try:
			await message.reply("Hi it's the coup bot! Thanks for mentioning me! Hello world & etc!")
		except Exception as e:
			print(f'{self.name} reply failed: {e}')
