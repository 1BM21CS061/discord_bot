import discord
from discord.ext import commands
from controller import Ranks

#creating a subclass of the commands.Bot main class
#commands.Bot class consists of several attributes and methods:
#attributes:description, owner_id, intents, command_prefix
#methods:run(token), close(), get_user_info(user_id)

class RankingBot(commands.Bot):
    ranks:Ranks 

    def initialize(self):
        self.ranks = Ranks()

    async def process_message(self,message: discord.Message):
        await self.ranks.process_message(message)


    async def process_reaction(self,payload:discord.RawReactionActionEvent):
        await self.ranks.process_reaction(payload)