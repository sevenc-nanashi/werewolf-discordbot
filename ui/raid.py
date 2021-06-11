from discord.ext.ui import Component, Button, View, Message, async_interaction_partial
from discord import Embed, Colour

class Raid(View):
    def __init__(self, bot):
        super().__init__(bot)
        self.bot = bot

    async def choice(self, interaction, p):
        self.bot.game.raid_target = p
        embed = Embed(description=f'{p.mention} を襲撃しました', colour=Colour.green())
        await interaction.channel.send(embed=embed)
        
        self.bot.game.decrease_task()
        await interaction.message.delete()
        await self.stop()

    async def body(self):
        items = []
        for p in self.bot.game.players:
            items.append(
                Button(p.name)
                    .on_click(async_interaction_partial(self.choice, p))
                    .disabled(p.is_dead or p.role == '狼')
            )
        items = [items[x:x+3] for x in range(0, len(items), 3)]
        return Message(
            embed=Embed(
                title='襲撃する対象を選択してください',
                description='対象を殺害することができます',
                colour=Colour.blue()
            ),
            component=Component(items=items)
        ).on_appear(self.bot.game.increase_task)