import discord
import os
from typing import Union
from enum import Enum
from dotenv import load_dotenv
load_dotenv()
from typing import Generator, Any

from env.state import GameState, TurnType
from env.action import ActionType

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
	game_generator: Generator[int, Any, None] = None
	game_creator: discord.Member = None
	players: list[discord.Member] = []
	current_player: int = 0
	turn_type: TurnType = TurnType.ACTION

	def __init__(self) -> None:
		self._discord_client = discord.Client(
			intents=discord.Intents(messages=True, guilds=True)
		)

	def start(self, loop):
		loop.create_task(self._discord_client.start(os.environ.get('DISCORD_TOKEN')))
		tree = discord.app_commands.CommandTree(self._discord_client)

		@tree.command(name = "new_game", description = "Create a new Coup game & enter lobby phase", guild=discord.Object(id=GUILD_ID)) #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
		async def new_game(interaction):
			await self.new_game(interaction)

		@tree.command(name = "join_game", description = "Join existing Coup game", guild=discord.Object(id=GUILD_ID))
		async def join_game(interaction):
			await self.join_game(interaction)

		@tree.command(name = "start_game", description = "Start Coup game with registerd players", guild=discord.Object(id=GUILD_ID))
		async def start_game(interaction):
			await self.start_game(interaction)

		@tree.command(name = "action", description = "Take a primary action as the player whose turn it is", guild=discord.Object(id=GUILD_ID))
		@discord.app_commands.choices(actions=[
				discord.app_commands.Choice(name="Income", value=str(ActionType.INCOME)),
				discord.app_commands.Choice(name="Foreign aid", value=str(ActionType.FOREIGN_AID)),
				discord.app_commands.Choice(name="Coup", value=str(ActionType.COUP)),
				discord.app_commands.Choice(name="Tax", value=str(ActionType.TAX)),
				discord.app_commands.Choice(name="Assassinate", value=str(ActionType.ASSASSINATE)),
				discord.app_commands.Choice(name="Exchange", value=str(ActionType.EXCHANGE)),
				discord.app_commands.Choice(name="Steal", value=str(ActionType.STEAL)),
				])
		async def action(interaction, actions: discord.app_commands.Choice[str]):
			await self.action(interaction, actions.value)


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
		self.game_generator = self.game.play_game()
		self.phase = GamePhase.PLAY
		await interaction.response.send_message("Game started")
		self.current_player = next(self.game_generator)

	async def action(self, interaction, action: ActionType):
		if interaction.user != self.players[self.current_player]:
			await interaction.response.send_message("It's not your turn")
			return
		if self.turn_type != TurnType.ACTION:
			await interaction.response.send_message("You can't take an action right now")
			return

		self.game_generator.send(action)
		await interaction.response.send_message("Action taken")
		self.turn_type = TurnType.CHALLENGE_OP

	


	
		
	