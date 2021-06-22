import discord
from discord.ext import commands
bot = commands.Bot(command_prefix="%")

class Cogban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name=f'ezban')
    async def ban(ctx, user: discord.User, *reason):
        reason = " ".join(reason)
        await ctx.guild.ban(user, reason=reason)
        await ctx.send(f"{user} was deleted")

    @commands.command(name='ezunban')
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

class Cogmute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def createMutedRole(ctx):
        mute = await ctx.guild.create_role(name="Mutted",
                                           permissions=discord.permissions(send_messages=False, speak=False),
                                           reason="Mutted role was create")
        for channel in ctx.guild.channels:
            await channel.set_permissions(mutedRole, send_messages=False)
            return mutedRole

    async def getMutedRole(ctx):
        roles = ctx.guild.roles
        for role in roles:
            if role.name == "Mutted":
                return role
        await createMutedRole()

    @commands.command(name='mute')
    async def mute(ctx, member: discord.Member, *, reason="flood"):
        mutedRole = await getMutedRole(ctx)
        await member.add_roles(mutedRole, reason=reason)
        await ctx.send(f"{member.mention}: muted")

    @commands.command(name='unmute')
    async def unmute(ctx, member: discord.Member, *, reason="no enought information"):
        mutedRole = await getMutedRole(ctx)
        await member.remove_roles(mutedRole, reason=reason)
        await ctx.send(f"{member.mention}: unmuted")


