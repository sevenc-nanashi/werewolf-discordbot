from discord.ext.ui import Component, Button, View, Message
from discord import Embed, Colour, ButtonStyle
from random import shuffle

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
        shuffle(self.members)
        l = list('ABCDEFGHI')
        for member in self.members[:9]:
            p = Player(member)
            p.name = f'市民{l.pop(0)}'
            self.bot.game.players.append(p)
        embed = Embed(
            title='ゲーム参加者が決定しました',
            description='\n'.join([m.mention for m in self.members[:9]]),
            colour=Colour.green()
        )
        await interaction.channel.send(embed=embed)
        
        await interaction.message.delete()

    async def body(self):
        return Message(
            embed=Embed(
                title=f'参加者募集パネル｜{len(self.members)}/9',
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