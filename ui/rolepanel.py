from discord.ext.ui import Component, Button, View, Message, async_interaction_partial
from discord import Embed, Colour, ButtonStyle
from random import shuffle

class Rolepanel(View):
    def __init__(self, bot, author_id):
        super().__init__(bot)
        self.bot = bot
        self.author_id = author_id
        self.close = False

    async def choice(self, interaction, choice):
        for p in self.bot.game.players:
            if interaction.user.id == p.id:
                p.role = choice

    async def end(self, interaction):
        if interaction.user.id != self.author_id:
            return
        game = self.bot.game
        if game.settings.custom_role_list == None:
            role_list = list(game.role_list(game.settings.max_player))
        else:
            role_list = list(game.settings.custom_role_list)

        for p in game.players:
            if p.role in role_list:
                role_list.remove(p.role)
            else:
                p.role = '乱'
        shuffle(role_list)
        for p in game.players:
            if p.role == '乱':
                p.role = role_list.pop(0)
        await interaction.channel.send('ゲーム参加者に役職を配布しました')
        await interaction.message.delete()

    async def body(self):
        return Message(
            embed=Embed(
                title='希望役職パネル', 
                description='希望する役職のボタンを選択してください\n人数が多い場合は抽選で選択されます',
                colour=Colour.green()
            ),
            component=Component(items=[
                [
                    Button('市民').on_click(async_interaction_partial(self.choice, '村')),
                    Button('占い').on_click(async_interaction_partial(self.choice, '占')),
                    Button('霊能').on_click(async_interaction_partial(self.choice, '霊')),
                    Button('狩人').on_click(async_interaction_partial(self.choice, '狩'))
                ],
                [
                    Button('人狼').on_click(async_interaction_partial(self.choice, '狼')).style(ButtonStyle.red),
                    Button('狂人').on_click(async_interaction_partial(self.choice, '狂')).style(ButtonStyle.red),
                    Button('ランダム').on_click(async_interaction_partial(self.choice, '乱')).style(ButtonStyle.grey),
                    Button('締切').on_click(self.end).style(ButtonStyle.grey)
                ]
            ])
        )