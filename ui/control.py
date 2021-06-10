# from discord.ext.ui import Component, Button, View, Message, async_interaction_partial
# from discord import Embed, Colour, ButtonStyle

# class Control(View):
#     def __init__(self, bot):
#         super().__init__(bot)
#         self.bot = bot

#     async def countdown(self, interaction):
#         await interaction.channel.send(f'{interaction.user.mention} 時間短縮')
#         self.bot.game.times -= 60
#         await self.update()

#     async def body(self):
#         return Message(
#             embed=Embed(
#                 description=f'討論の残り時間 {self.bot.game.countdown}秒',
#                 colour=Colour.green()
#             ),
#             component=Component(items=[
#                 [
#                     Button('60秒 時間短縮')
#                         .on_click(self.countdown)
#                         .style(ButtonStyle.danger)
#                 ]
#             ])
#         )