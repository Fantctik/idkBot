import economy
import disnake
from disnake.ext import commands
from disnake.ext.commands import has_permissions
import config
import time
from disnake.ext.commands import has_guild_permissions
import sqlite3

conn = sqlite3.connect('accounts.db')
cursor = conn.cursor()

client = commands.Bot(command_prefix='!', help_command=None, intents=disnake.Intents.all()) #первый аргумент - префикс

@client.event
async def on_ready():
    print("ready")

#Вход-выход

@client.event
async def on_member_join(member):
    role = member.guild.get_role(1065660265313607762) #начальная роль
    channel = member.guild.system_channel
    all_members = -8 #-8 потому что почему то бот при выводе показывает на 8 участников больше, причину не нашёл, если у вас всё хорошо с этим, то поставьте 0
    for i in client.get_all_members():
        all_members += 1
    embed = disnake.Embed(
        title="Добро пожаловать!",
        description=f"{member.name}#{member.discriminator}, теперь на сервере {all_members} участников!",
        color=0xffffff
    )
    await member.add_roles(role)
    await channel.send(embed=embed)

@client.event
async def on_member_remove(member):
    channel = member.guild.system_channel
    all_members = -8
    for i in client.get_all_members():
        all_members += 1
    embed = disnake.Embed(
        title="Сосать лошок",
        description=f"{member.name}#{member.discriminator} ливнул, теперь на сервере {all_members} участников!",
        color=0xff0000
    )
    await channel.send(embed=embed)

#Модерация

@client.command(name="kick")
@has_permissions(kick_members=True)
async def kick(ctx, member: disnake.Member, *, reason="Не указана"):
    await member.kick(reason=reason)
    embed = disnake.Embed(
        title="Кик",
        description=f"{ctx.author.mention} исключил {member.mention}",
        color=0xFFA500
    )
    await ctx.send(embed=embed)

@client.command(name="ban")
@has_permissions(ban_members=True)
async def ban(ctx, member: disnake.Member, *, reason="Не указана"):
    await member.ban(reason=reason)
    embed = disnake.Embed(
        title="Пизда кому то",
        description=f"{ctx.author.mention} забанил {member.mention}",
        color=0xFF0000
    )
    await ctx.send(embed=embed)

@client.command(name="mute")
@has_guild_permissions(mute_members=True)
async def mute(ctx, member: disnake.Member, time: float, reason="Не указана"):
    await member.guild.timeout(user=member,duration=time , reason=reason)
    embed = disnake.Embed(
        title="Мут/анмут",
        description=f"{ctx.author.mention} замутил/размутил {member.mention} на {time} секунд", #mute <user> 0 для размут
        color=0xFFFF00
    )
    await ctx.send(embed=embed)

#экономика

@client.command(name="create_wallet")
async def create_wallet(ctx):
    if economy.createUser(name=str(ctx.author.id)) == 1:
        await ctx.send("Данный пользователь уже зарегистрирован")
        return
    embed = disnake.Embed(
        title="Создание кошелька",
        description="Кошелёк создан",
        color=0x00FF00
    )
    await ctx.send(embed=embed)

@client.command(name="work")
async def work(ctx):
    cursor.execute(f"SELECT balanceBank FROM users WHERE name = {ctx.author.id}")
    timer = cursor.fetchone()[0]
    count = None
    if time.time() - timer >= 3600:
        count = economy.work(ctx.author.id)
    error_embed = disnake.Embed(
        title="Слишком рано!",
        description=f"Вы недавно поработали и устали, команда будет доступна через {round(60 - ((time.time() - timer) / 60))} минут!",
        color=0xFF0000
    )
    embed = disnake.Embed(
        title="Ворк",
        description=f"Вы поработали ртом и заработали {count} монет",
        color=0x00FF00
    )
    if time.time() - timer >= 3600:
        await ctx.send(embed=embed)
    else:
        await ctx.send(embed=error_embed)

@client.command(name="balance")
async def balance(ctx):
    money = economy.balance(ctx.author.id)
    embed = disnake.Embed(
        title="Баланс",
        description=f"У вас на счету {money} монет.",
        color=0x00FF00
    )
    await ctx.send(embed=embed)

@client.command(name="casino")
async def casino(ctx, count:int):
    match economy.casino(ctx.author.id, count):
        case 2:
            embed = disnake.Embed(
                title="Казино",
                description=f"Вы выиграли {count} монет!",
                color=0x00FF00
            )
            await ctx.send(embed=embed)
        case 0:
            embed = disnake.Embed(
                title="Казино",
                description=f"Вы проиграли {count} монет!",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
        case 3:
            await ctx.send("Ваша ставка меньше 100")
        case 4:
            await ctx.send("Вы поставили больше своего баланса.")

@client.command("sql_execute")
@has_permissions(administrator=True)
async def sql(ctx, args:str):
    cursor.execute(args)
    conn.commit()
    await ctx.send("Команда выполнена.")

@client.command("help")
async def help(ctx):
    embed = disnake.Embed(
        title="Команды",
        description="`Модерирование` \n !kick <user>, !ban <user>, !mute <user> <time> <reason> \n \n `Экономика` \n !create_wallet, !work, !balance, !casino <amount> \n \n `Для админа` \n !sql_execute <args>"
    )
    await ctx.send(embed=embed)

client.run(config.TOKEN) #вместо config.TOKEN нужно вписать ваш токен