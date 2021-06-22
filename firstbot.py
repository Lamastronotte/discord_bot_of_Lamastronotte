import json
import os
import youtube_dl
import discord
from discord.ext import commands
import asyncio
import cog_1

bot = commands.Bot(command_prefix="%")
musics = {}
ytdl = youtube_dl.YoutubeDL()

@bot.event
async def on_ready():
    print("le bot est pret")

class Video:
    def __init__(self, link):
        video = ytdl.extract_info(link, download=False)
        video_format = video["formats"] [0]
        self.url = video["webpage_url"]
        self.stream_url = video_format["url"]

@bot.command(name='del')
async def delete(ctx, number_of_messages: int):
    messages = await ctx.channel.history(limit=number_of_messages + 1).flatten()
    for each_message in messages:
        await each_message.delete()

@bot.command(name='ezkick')
async def kick(ctx, user: discord.User, *reason):
    reason = " ".join(reason)
    await ctx.guild.kick(user, reason=reason)
    await ctx.send(f"{user} was kiked")

def play_song(client, queue, song, ctx):
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(song.stream_url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))
    def next(_):
        if len(queue) > 0:
            new_song = queue[0]
            del queue[0]
            play_song(client, queue, new_song)
        else:
            asyncio.run_coroutine_threadsafe(client.disconnect(), bot.loop)

    client.play(source, after=next)

@bot.command(name='skip')
async def skip(ctx):
    client = ctx.guild.voice_client
    client.stop()

@bot.command(name='ezplay')
async def play(ctx, url):
    print("play")
    client = ctx.guild.voice_client
    if client and client.channel:
        video = Video(url)
        musics[ctx.guild].append(video)
    else:
        channel = ctx.author.voice.channel
        video = Video(url)
        musics[ctx.guild] = []
        client = await channel.connect()
        await ctx.send(f"i go play {video.url}")
        play_song(client, video)

if os.path.exists(os.getcwd() + "/config.json"):
    with open("./config.json") as f:
        configData = json.load(f)
else:
    configTemplate = {"Token": "", "Prefix": "!"}
    with open(os.getcwd() + "/config.json", "w+") as f: json.dump(configTemplate, f)

bot.add_cog(cog_1.Cogmute(bot))
bot.add_cog(cog_1.Cogban(bot))
token = configData["Token"]
prefix = configData["Prefix"]
bot.run(token)