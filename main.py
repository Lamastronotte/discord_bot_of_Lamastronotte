import json
import os
import discord
from discord.ext import commands
bot = commands.Bot(command_prefix="%")

@bot.event
async def on_ready():
    print("le bot est pret")

@bot.command(name='del')
async def delete(ctx, number_of_messages: int):
    messages = await ctx.channel.history(limit=number_of_messages + 1).flatten()
    for each_message in messages:
        await each_message.delete()

@bot.command(name='ezkick')
async def kick(ctx, user : discord.User, *reason):
    reason = " ".join(reason)
    await ctx.guild.kick(user, reason = reason)
    await ctx.send(f"{user} was kiked")

@bot.command(name=f'ezban')
async def ban(ctx, user : discord.User, *reason):
    reason = " ".join(reason)
    await ctx.guild.ban(user, reason = reason)
    await ctx.send(f"{user} was deleted")

@bot.command(name='ezunban')
async def unban(ctx, user, *reason):
    reason = " ".join(reason)
    userName, userID = user.split("#")
    bannedUsers = await ctx.guild.bans()
    for i in bannedUsers:
        if i.user.name == userName and i.user.discriminator == userID:
            await ctx.guild.unban(i.user, reason=reason)
            await ctx.send(f"{user} was unban")
            await ctx.send("note: maybe he doesn't want to come back")
            return
    await ctx.send(f"{user} was not banned")

if os.path.exists(os.getcwd() + "/config.json"):
    with open("./config.json") as f:
        configData = json.load(f)
else:
    configTemplate = {"Token": "", "Prefix": "!"}
    with open(os.getcwd() + "/config.json", "w+") as f: json.dump(configTemplate, f)

token = configData["Token"]
prefix = configData["Prefix"]
bot.run(token)