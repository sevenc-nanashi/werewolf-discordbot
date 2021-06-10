from discord.ext.ui import Component, Button, View, Message, async_interaction_partial
from discord import Embed, Colour

class Vote(View):
    def __init__(self, bot):
        super().__init__(bot)
        self.bot = bot

    async def choice(self, interaction, p):
        p.voted += 1
        embed = Embed(description=f'{p.mention} に投票しました', colour=Colour.green())
        await interaction.channel.send(embed=embed)
        await self.bot.game.channels.alive.send(f'{interaction.user.display_name} が投票しました')

        await self.bot.game.decrease_task()
        await interaction.message.delete()

    async def body(self):
        items = []
        for p in self.bot.game.players:
            items.append(
                Button(p.name)
                    .on_click(async_interaction_partial(self.choice, p))
                    .disabled(p.is_dead)
            )
        items = [items[x:x+3] for x in range(0, len(items), 3)]
        return Message(
            embed=Embed(
                title='投票する対象を選択してください',
                description='最も投票されたプレイヤーが処刑されます',
                colour=Colour.blue()
            ),
            component=Component(items=items)
        ).on_appear(self.bot.game.increase_task)
        