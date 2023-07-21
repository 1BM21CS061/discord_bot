import discord
from models import UserActivity,PointType
from user_model import User

class Ranks:
    async def process_message(self,message: discord.Message):
        await self.add_points(message.id, message.author.id,PointType.MESSAGE) #arguments: id of message, id of discord user who messaged, specifies the type of points type


    async def process_reaction(self,payload:discord.RawReactionActionEvent):
        if payload.event_type=="REACTION_ADD":
            await self.add_points(payload.message_id, payload.user_id,PointType.REACTION)
        else:
            self.reduce_points(payload.message_id, payload.user_id,PointType.REACTION,UserActivity.MODE_REDUCE)
    
    def save_to_db(self,message_id,user_id,point_type,mode=UserActivity.MODE_ADD):
        user = User.fetch_by_user_id(user_id) #gets the user object corresponding to the user_id from the user table  
        user_activity = UserActivity(message_id=message_id,user=user)
        user_activity.record_new_points(point_type,mode)

    async def add_points(self,message_id,user_id,point_type):
        self.save_to_db(message_id,user_id,point_type)

    async def reduce_points(self,message_id,user_id,point_type,mode):
        self.save_to_db(message_id,user_id,point_type,mode)