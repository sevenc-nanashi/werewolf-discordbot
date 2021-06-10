import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

guild_ids = [840795339723767838, 810011469381894174]

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name = 'long',
        description = '会議時間を60秒延長します',
        guild_ids = guild_ids,
    )
    async def _long(self, ctx: SlashContext):
        self.bot.game.times += 60
        await ctx.send(f'{ctx.author.mention} 会議時間を60秒延長しました')

    @cog_ext.cog_slash(
        name = 'short',
        description = '会議時間を60秒短縮します',
        guild_ids = guild_ids,
    )
    async def _short(self, ctx: SlashContext):
        self.bot.game.times -= 60
        await ctx.send(f'{ctx.author.mention} 会議時間を60秒短縮しました')

def setup(bot):
    bot.add_cog(Commands(bot))