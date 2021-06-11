from discord.ext.ui import Component, Button, View, Message
from discord import Embed, Colour, ButtonStyle
from random import shuffle
from string import ascii_uppercase

from lib.player import Player

class Invite(View):
    def __init__(self, bot, author_id):
        super().__init__(bot)
        self.bot = bot
        self.author_id = author_id
        self.members = []
        self.close = False

    async def join(self, interaction):
        if not interaction.user in self.members:
            self.members.append(interaction.user)
        await self.update()
    
    async def leave(self, interaction):
        if interaction.user in self.members:
            self.members.remove(interaction.user)
        await self.update()

    async def end(self, interaction):
        if interaction.user.id != self.author_id:
            return
        max_player = self.bot.game.settings.max_player
        shuffle(self.members)
        l = list(ascii_uppercase)
        for member in self.members[:max_player]:
            player = Player(member)
            player.symbol = l.pop(0)
            player.name = f'市民{player.symbol}'
            self.bot.game.players.append(player)
        embed = Embed(
            title='ゲーム参加者が決定しました',
            description='\n'.join([m.mention for m in self.members[:max_player]]),
            colour=Colour.green()
        )
        await interaction.channel.send(embed=embed)
        
        await interaction.message.delete()
        await self.stop()

    async def body(self):
        return Message(
            embed=Embed(
                title=f'参加者募集パネル｜{len(self.members)}/{self.bot.game.settings.max_player}',
                description='\n'.join([m.mention for m in self.members]),
                colour=Colour.blue()
            ),
            component=Component(items=[
                [
                    Button('参加希望').on_click(self.join).style(ButtonStyle.primary),
                    Button('参加取り止め').on_click(self.leave).style(ButtonStyle.danger),
                    Button('締切').on_click(self.end).style(ButtonStyle.secondary)
                ]
            ])
        )