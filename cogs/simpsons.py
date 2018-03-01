from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

from api.compuglobal import Frinkiac
from api.compuglobal import FrinkiHams
from cogs.tvshows import TVShowCog


class Simpsons(TVShowCog):
    def __init__(self, bot):
        super().__init__(bot, Frinkiac())
        self.frinkihams = FrinkiHams()

    # Messages a random Simpsons quote with gif if no search terms are given,
    # Otherwise, search for Simpsons quote using search terms and post gif
    @commands.command(aliases=['simpsonsgif', 'sgif'])
    @commands.cooldown(1, 3, BucketType.channel)
    @commands.guild_only()
    async def simpsons(self, ctx, *, search_terms: str=None):
        await self.post_gif(ctx, search_terms)

    # Allows for custom captions to go with the gif that's searched for
    @commands.command(aliases=['smeme'])
    @commands.cooldown(1, 3, BucketType.channel)
    @commands.guild_only()
    async def simpsonsmeme(self, ctx, *, search_terms: str):
        await self.post_custom_gif(ctx, search_terms)

    # Generate a random Steamed Hams quote with gif if no search terms are
    # given, otherwise search for quote using search terms and post gif
    @commands.command(aliases=['steamed', 'aurora', 'borealis'])
    async def steamedhams(self, ctx, *, search_terms: str=None):
        if search_terms is None:
            screencap = await self.frinkihams.get_random_screencap()

        else:
            screencap = await self.frinkihams.search_for_screencap(search_terms)

        gif_url = await screencap.get_gif_url(before=2000, after=2000)
        sent = await ctx.send('Steaming your hams...'
                              + '<a:loading:410316176510418955>')

        generated_url = await self.api.generate_gif(gif_url)
        await sent.edit(content=generated_url)


def setup(bot):
    bot.add_cog(Simpsons(bot))
