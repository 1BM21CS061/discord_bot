import discord
from discord.ext import commands

from models import UserActivity 
from user_model import User
import database
from baseClasses import RankingBot
 

def setup_tables():
    database.db.create_tables([User, UserActivity])

def run():
    setup_tables()
    intents = discord.Intents.all() #intents are a feature to control which events the bots receives
    bot = RankingBot(command_prefix="!", intents=intents)
    bot.initialize()

    @bot.event   #event handlers(capture events)
    async def on_ready():
        print("We have logged in as {}".format(bot.user))
        await bot.load_extension("cog") #loading Ranks cog class in cog.py
 
    #on_message event is triggered whenever a message is sent in a text channel the bot has access to
    #discord.Message provides access to message content, author, channel, guild, mentions etc.
    #discord.Message.content => accesses text of the message
    #channel.send(Message) => to send messages to the channel where message was received 
    @bot.event
    async def on_message(message: discord.Message):
        ctx = await bot.get_context(message)  #contains information about the command
        channel = ctx.channel
        if not ctx.valid:
          if not message.author.bot:    #basically handling only member messages and not bot messages
              await bot.process_message(message)
        await bot.process_commands(message)

    #on_raw_reaction event is triggered when a user adds or removes a reaction to a message
    #discord.RawReactionActionEvent provides information about reaction event
    #attributes: member, event_type(add or remove), message_id of message which was reacted to, user_id etc.
    @bot.event
    async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
        await bot.process_reaction(payload)

    @bot.event
    async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
        await bot.process_reaction(payload)

    bot.run('MTEwMzM3MTIxMzEwOTIxOTM3OA.G-2g-U.ahkgEtSa2wV4OVlVttcocq1IzoLox5H1JWX9_k')
             

if __name__ == "__main__":
    run()
