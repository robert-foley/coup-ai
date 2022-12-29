import discord
import os
from typing import Union
from env.state import GameState
from enum import Enum
from dotenv import load_dotenv
load_dotenv()

GUILD_ID = 991853883020283944

class GamePhase(Enum):
	""" Enum representing different phases of a game of Coup """
	NONE = "none"  # No game is in progress
	LOBBY = "lobby"  # Players are joining the game
	PLAY = "play"  # Game is in progress
class CoupDiscordBot:
	_discord_client: discord.Client = None
	phase: GamePhase = GamePhase.NONE
	game: GameState = None
	game_creator: discord.Member = None
	players: list[discord.Member] = []

	def __init__(self) -> None:
		self._discord_client = discord.Client(
			intents=discord.Intents(messages=True, guilds=True)
		)

	def start(self, loop):
		loop.create_task(self._discord_client.start(os.environ.get('DISCORD_TOKEN')))
		tree = discord.app_commands.CommandTree(self._discord_client)

		@tree.command(name = "new_game", description = "Create new Coup game", guild=discord.Object(id=GUILD_ID)) #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
		async def join_game(interaction):
			await self.join_game(interaction)

		@self._discord_client.event
		async def on_ready():
			await tree.sync(guild=discord.Object(id=GUILD_ID))
			print(f'Logged in as {self._discord_client.user}!')

	async def new_game(self, interaction):
		self.game_creator = interaction.user
		self.phase = GamePhase.LOBBY
		self.players.append(interaction.user)
		await interaction.response.send_message("New game created by " + self.game_creator.name)

	async def join_game(self, interaction):
		self.players.append(interaction.user)
		# serialize list of players
		players_str = ', '.join([player.name for player in self.players])
		await interaction.response.send_message("Game joined with " + players_str)

	async def start_game(self, interaction):
		self.game = GameState(num_players=len(self.players))
		self.phase = GamePhase.PLAY
		await interaction.response.send_message("Game started")

	
		
	