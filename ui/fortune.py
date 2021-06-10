from discord.ext.ui import Component, Button, View, Message, async_interaction_partial
from discord import Embed, Colour

class Fortune(View):
    def __init__(self, bot):
        super().__init__(bot)
        self.bot = bot

    async def choice(self, interaction, p):
        embed = Embed(description=f'{p.mention} は {p.color} です', colour=Colour.green())
        await interaction.channel.send(embed=embed)

        await self.bot.game.decrease_task()        
        await interaction.message.delete()

    async def body(self):
        items = []
        for p in self.bot.game.players:
            items.append(
                Button(p.name)
                    .on_click(async_interaction_partial(self.choice, p))
                    .disabled(p.is_dead or p.role == '占')
            )
        items = [items[x:x+3] for x in range(0, len(items), 3)]
        return Message(
            embed=Embed(
                title='占う対象を選択してください',
                description='対象が人狼だった場合は黒、\nそれ以外は白と占われます',
                colour=Colour.blue()
            ),
            component=Component(items=items)
        ).on_appear(self.bot.game.increase_task)