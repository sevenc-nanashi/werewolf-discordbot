import discord
from discord.ext import commands
from discord_slash import SlashCommand
import settings

from lib.game import Game

token = settings.TOKEN
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='w/', intents=intents)
slash = SlashCommand(bot, sync_commands=True)

bot.game = Game()

cogs = [
    'cogs.setting',
    'cogs.main',
    'cogs.commands',
    'cogs.debug',
]

for cog in cogs:
    bot.load_extension(cog)

bot.run(token)