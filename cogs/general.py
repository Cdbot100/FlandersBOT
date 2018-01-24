import botInfo
import settings.config
import discord
import json
import prefixes

from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

class General():
    def __init__(self, bot):
        self.bot = bot

    # Whispers a description of the bot with author, framework, guild count etc.
    # If user has DMs disabled, send the message in the channel
    @commands.command()
    @commands.cooldown(1, 3, BucketType.user)
    async def info(self, ctx):
        try:
            await ctx.author.send(botInfo.botInfo + '\n***Currently active in '
                              + str(len(self.bot.guilds)) + ' servers***')

        except discord.Forbidden:
            await ctx.send(botInfo.botInfo + '\n***Currently active in '
                              + str(len(self.bot.guilds)) + ' servers***')

    # Whispers a list of the bot commands, If the user has DMs disabled,
    # sends the message in the channel
    @commands.command()
    @commands.cooldown(1, 3, BucketType.user)
    async def help(self, ctx):
        try:
            await ctx.author.send(botInfo.commandsList)

        except:
            await ctx.send(botInfo.commandList)

    # Sends the feedback to the feedback channel of support server
    @commands.command()
    @commands.cooldown(2, 600, BucketType.user)
    async def feedback(self, ctx, *, message : str):
        feedbackChannel = self.bot.get_channel(403688189627465730)
        embed = discord.Embed(title='📫 Feedback from: ' + str(ctx.author) +
                              ' (' + str(ctx.author.id) + ')',
                              colour=discord.Colour(0x44981e),
                              description='```' + message + '```')

        embed.set_author(name=ctx.message.author.name,
                         icon_url=ctx.message.author.avatar_url)

        await feedbackChannel.send(embed=embed)

    # Display the prefixes used on the current guild
    @commands.command()
    @commands.cooldown(1, 3, BucketType.channel)
    async def prefix(self, ctx):
        guildPrefixes = await prefixes.prefixesFor(ctx.message.guild)
        if len(guildPrefixes) > 5:
            await ctx.send('This servers prefixes are: `ned`, `diddly`,' +
                               ' `doodly`,' + ' `diddly-`, `doodly-` and `' +
                               guildPrefixes[-1] + '`.' )

        else:
            await ctx.send('This servers prefixes are `ned`, `diddly`, ' +
                               '`doodly`,' + ' `diddly-` and `doodly-`.')

    # Allows for a single custom prefix per-guild
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    @commands.cooldown(3, 60, BucketType.guild)
    async def setprefix(self, ctx, *, message : str=None):
        guildIndex = prefixes.findGuild(ctx.message.guild)

        # Only allow custom prefixes in guilds
        if ctx.message.guild is None:
            await ctx.send('Custom prefixes are for servers only.')

        # Require entering a prefix
        if message is None:
            await ctx.send('You did not provide a new prefix.')

        # Limit prefix to 10 characters, may increase
        elif len(message) > 10:
            await ctx.send('Custom server prefix too long (Max 10 chars).')

        else:
            # Write the new custom prefix
            with open('prefixes.json', 'r') as guildList:
                data = json.load(guildList)
                guildList.close()

            # Declare if it is already that prefix
            if data[guildIndex]['prefix'] == message:
                await ctx.send('This server custom prefix is already `' +
                                   message + '`.')

            else:
                # Add a new custom guild prefix if one doesn't already exist
                if guildIndex == -1:
                    data.append({'guildID':ctx.message.guild.id,
                                'prefix':message})

                # Otherwise, modify the current prefix to the new one
                else:
                    data[guildIndex]['prefix'] = message

                # Write the new prefix to the file
                with open('prefixes.json', 'w') as guildList:
                    json.dump(data, guildList, indent=4)
                    guildList.close()
                    await ctx.send('This servers custom prefix changed to `'
                                       + message + '`.')

    # Display statistics for the bot
    @commands.command()
    @commands.cooldown(1, 3, BucketType.channel)
    async def stats(self, ctx):

        # Get guild count
        guildCount = len(self.bot.guilds)

        # Count users online in guilds
        totalMembers = 0
        onlineUsers = 0
        for guild in self.bot.guilds:
            totalMembers += len(guild.members)
            for member in guild.members:
                if member.status == discord.Status.online:
                    onlineUsers += 1

        averageOnline = round((onlineUsers / guildCount), 2)

        # Embed statistics output
        embed = discord.Embed(colour=discord.Colour(0x44981e))
        embed.set_thumbnail(url='https://images.discordapp.net/avatars/221609683562135553/afc35c7bcaf6dcb1c86a1c715ac955a3.png')
        embed.set_author(name='FlandersBOT Statistics', url='https://github.com/FlandersBOT', icon_url='https://images.discordapp.net/avatars/221609683562135553/afc35c7bcaf6dcb1c86a1c715ac955a3.png')
        embed.add_field(name='Bot Name', value='FlandersBOT#0680', inline=True)
        embed.add_field(name='Bot Owner', value='Mitch#8293', inline=True)
        embed.add_field(name='Total Members', value=str(totalMembers), inline=True)
        embed.add_field(name='Server Count', value=str(guildCount), inline=True)
        embed.add_field(name='Online Users', value=str(onlineUsers), inline=True)
        embed.add_field(name='Online Users Per Server', value=str(averageOnline), inline=True)

        # Post statistics
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(General(bot))
