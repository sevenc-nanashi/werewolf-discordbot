from discord import Embed, Colour, PermissionOverwrite
from discord.ext import commands
from asyncio import sleep
from random import choice

from ui.fortune import Fortune
from ui.escort import Escort
from ui.raid import Raid
from ui.vote import Vote

class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot        

    @commands.command()
    async def gamestart(self, ctx):

        guild = ctx.guild
        category = ctx.channel.category
        everyone = guild.default_role

        game = self.bot.game
        players = game.players
        channels = game.channels
        roles = game.roles

        channels.alive = await category.create_text_channel(name='生存者')
        channels.dead = await category.create_text_channel(name='死亡者')
        channels.audience = await category.create_text_channel(name='観戦者')
        channels.wolfs = await category.create_text_channel(name='人狼部屋')

        roles.alive = await guild.create_role(name='生存者', colour=Colour.blue())
        roles.dead = await guild.create_role(name='死亡者', colour=Colour.red())

        await channels.alive.set_permissions(everyone, send_messages=False)
        await channels.alive.send(f'{roles.alive.mention}\nここは生存者が集まって討論する場所です\nこのチャンネルは全員が見ることができますが、生存者しか書き込むことはできません')
        
        await channels.dead.set_permissions(roles.alive, read_messages=False)
        await channels.dead.set_permissions(everyone, send_messages=False)
        await channels.dead.set_permissions(roles.dead, send_messages=True)
        await channels.dead.send('ここは死亡者が集まって雑談する場所です\nこのチャンネルは死亡者・観戦者が見ることができますが、死亡者しか書き込むことはできません')

        await channels.audience.set_permissions(roles.alive, read_messages=False)
        await channels.audience.send('ここは観戦者が集まって雑談する場所です\nこのチャンネルは死亡者・観戦者が見る・書き込むことができます')

        await channels.wolfs.set_permissions(everyone, read_messages=False)
        await channels.wolfs.send('ここは人狼が集まって会議する場所です\nこのチャンネルは人狼にしか見えません')

        for player in players:
            member = guild.get_member(player.id)
            await member.edit(nick=f'{player.name}｜{player.status}')
            await member.add_roles(roles.alive)
            player.channel = await category.create_text_channel(
                name=f'{player.side}｜{player.role_name}',
                overwrites={
                    everyone: PermissionOverwrite(read_messages=False),
                    member: PermissionOverwrite(read_messages=True)
                }
            )
            await player.channel.send(f'{player.mention} {player.side}｜{player.role_name}\nこのチャンネルはあなたにしか見えません')
            if player.role == '狼':
                await channels.wolfs.set_permissions(member, overwrite=PermissionOverwrite(read_messages=True))

        while True:
            embed = Embed(description=f'{game.days}日目夜｜{roles.alive.mention} {len(players.alives)}人', colour=Colour.blue())
            await channels.alive.send(embed=embed)
            await channels.alive.send('個人のチャンネルに移動してください')
            await channels.alive.set_permissions(roles.alive, send_messages=False)

            for player in players.alives:
                if game.days == 1:
                    if player.role == '占':
                        p = choice([p for p in players if p.color == '白' and p != player])
                        await player.channel.send(f'{p.mention} は {p.color} でした')
                if game.days != 1:
                    if player.role == '占':
                        await Fortune(self.bot).start(player.channel)
                    if player.role == '霊':
                        await player.channel.send(f'{game.vote_target.mention} は {game.vote_target.color} でした')
                    if player.role == '狩':
                        await Escort(self.bot).start(player.channel)
            if game.days != 1:
                await Raid(self.bot).start(channels.wolfs)
                        
            while game.tasks > 0:
                await sleep(1)

            if game.raid_target != game.escort_target:
                player = game.raid_target
                player.die()
                embed = Embed(description=f'{player.mention} が殺害されました', colour=Colour.red())
                await channels.alive.send(embed=embed)
                member = guild.get_member(player.id)
                await member.edit(nick=f'{player.name}｜{player.status}')
                await member.remove_roles(roles.alive)
                await member.add_roles(roles.dead)
            else:
                embed = Embed(description='誰も殺害されませんでした', colour=Colour.green())
                await channels.alive.send(embed=embed)

            if game.is_werewolf_win():
                await channels.alive.send('ゲーム終了｜人狼陣営の勝利です')
                await ctx.channel.send(game.role_list)
                break

            embed = Embed(description=f'{game.days}日目朝｜{roles.alive.mention} {len(players.alives)}人', colour=Colour.blue())
            await channels.alive.send(embed=embed)
            await channels.alive.send('処刑する人を話し合ってください')
            await channels.alive.set_permissions(roles.alive, send_messages=True)
            
            game.times = 600
            while game.times > 0:
                game.times -= 1
                if game.times % 60 == 0:
                    await channels.alive.send(f'会議時間残り{game.times}秒です')
                await sleep(1)

            embed = Embed(description=f'{game.days}日目夕｜{roles.alive.mention} {len(players.alives)}人', colour=Colour.blue())
            await channels.alive.send(embed=embed)
            await channels.alive.send('個人チャンネルで投票をしてください')

            for player in players.alives:
                await Vote(self.bot).start(player.channel)

            while game.tasks > 0:
                await sleep(1)

            maximum = max([p.voted for p in players.alives])
            for player in players.alives:
                if player.voted == maximum:
                    player.die()
                    member = guild.get_member(player.id)
                    if player.role == '狼':
                        await channels.wolfs.set_permissions(member, overwrite=PermissionOverwrite(read_messages=False))
                    embed = Embed(description=f'{player.mention} が処刑されました', colour=Colour.red())
                    await channels.alive.send(embed=embed)
                    await member.edit(nick=f'{player.name}｜{player.status}')
                    await member.remove_roles(roles.alive)
                    await member.add_roles(roles.dead)
                    game.vote_target = player
                    break
                
            for player in players.alives:
                player.voted = 0

            if game.is_werewolf_win():
                await channels.alive.send('ゲーム終了｜人狼陣営の勝利です')
                await ctx.channel.send(game.role_list)
                break
            if game.is_village_win():
                await channels.alive.send('ゲーム終了｜市民陣営の勝利です')
                await ctx.channel.send(game.role_list)
                break

            game.days += 1

def setup(bot):
    bot.add_cog(Main(bot))