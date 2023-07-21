from discord.ext import commands
from user_model import User 
import discord 
from models import LevelSystem,UserActivity

class Ranks(commands.Cog):
    """
    A Discord.py cog for managing ranks and leaderboards.
    """

    def __init__(self, bot):
        #Initializes the Ranks cog
        self.bot = bot 

    @commands.group()
    async def rs(self, ctx):
        ...

    @rs.command()
    async def leaderboard(self, ctx):
        leaderboard_users = User.get_leaderboard()
        embed = discord.Embed(title="Leaderboard")
        output = "``"
        for user in leaderboard_users:
            discord_member = await ctx.message.guild.fetch_member(user.user_id)
            output += f"{discord_member.display_name:25}{user.total_points} Pts."
        output += "``"
        embed.add_field(name="Users", value=output, inline=False)
        await ctx.send(embed=embed)

    @rs.command()
    async def rank(self,ctx,member:discord.Member = None):
        if not member:
            member = ctx.message.author

        total_points = UserActivity.get_points(member.id)
        current_rank = LevelSystem.get_rank(total_points)
        next_level_xp = LevelSystem.get_level_xp(current_rank+1)
        current_xp_level = LevelSystem.get_level_xp(current_rank)

        next_level_xp_diff = next_level_xp - current_xp_level
        level_progress = total_points - current_xp_level

        count_messages = UserActivity.count_messages(member.id)
        count_reactions = UserActivity.count_reactions(member.id)


async def setup(bot):
    #Function to set up and add the Ranks cog to the bot
    await bot.add_cog(Ranks(bot))
