import discord
from discord.ext import commands

from lib.player import Player

class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def debug(self, ctx):
        ids = [
            823890048088932383, 
            805479870376968202, 
            830778350929838100,
            735722422866542632, 
            823857190849871872, 
            836979174018514995,
            793214782349115432, 
            809760929264828446, 
            826152382139203634
        ]
        l = list('ABCDEFGHI')
        for i in ids:
            member = ctx.guild.get_member(i)
            player = Player(member)
            player.name = f'市民{l.pop(0)}'
            self.bot.game.players.append(player)

def setup(bot):
    bot.add_cog(Debug(bot))