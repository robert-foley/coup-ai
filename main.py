import asyncio
from discord.coup_discord_bot import CoupDiscordBot

print("HI!!! Let's play Coup on Discord")
loop = asyncio.new_event_loop()
bot = CoupDiscordBot()
bot.start(loop)
loop.run_forever()
