import enum
import peewee
from user_model import User
from all_models import BaseModel
import math

class PointType(enum.Enum):
    MESSAGE=2
    REACTION=1  

class LevelSystem:
    @staticmethod
    def get_rank(points):
        return math.floor((points*5/4)**(1.0/3))

    @staticmethod 
    def get_level_xp(level):
        return math.floor((4*(level**3))/5)


class UserActivity(BaseModel):

    MODE_ADD = "ADD"
    MODE_REDUCE = "REDUCE"
    MODE_CHOICES = (
        (MODE_ADD,MODE_ADD),
        (MODE_REDUCE,MODE_REDUCE),
    )

    user = peewee.ForeignKeyField(model=User)
    message_id = peewee.CharField(max_length=255)
    reaction = peewee.BooleanField(default=False)
    points = peewee.FloatField()
    mode = peewee.CharField(choices=MODE_CHOICES,default = MODE_ADD)

    def record_new_points(self,point_type,mode):
        
        points = point_type.value
        if point_type==PointType.REACTION:
            self.reaction = True
        
        current_total_points = UserActivity.get_points(self.user.user_id)
        if mode == UserActivity.MODE_ADD:
            new_total_points = current_total_points + points 
        else:
            new_total_points = current_total_points - points
        
        self.user.total_points = new_total_points
        self.user.save()

        self.points = points
        self.mode = mode 

        self.save()

    @staticmethod 
    def get_points(user_id):
        added_points_sum = UserActivity.select(
            UserActivity.points, peewee.fn.SUM(UserActivity.points).alias("total")
        ).join(User).where(User.user_id == user_id, UserActivity.mode == UserActivity.MODE_ADD)

        reduced_points_sum = UserActivity.select(
            UserActivity.points, peewee.fn.SUM(UserActivity.points).alias("total")
        ).join(User).where(User.user_id == user_id, UserActivity.mode == UserActivity.MODE_REDUCE)

        added_total = 0
        if reduced_points_sum[0].total:
            added_total = reduced_points_sum[0].total 

        reduced_total = 0
        if reduced_points_sum[0].total:
            reduced_total = reduced_points_sum[0].total

        return added_total - reduced_total
    
    @staticmethod 
    def count_messages(user_id):
        return UserActivity.select(UserActivity,User).join(User).where(User.user_id==user_id,UserActivity.reaction == False).count()
    
    @staticmethod 
    def count_reactions(user_id):
        added_reactions =  (UserActivity.select(UserActivity,User).join(User).where(User.user_id==user_id,UserActivity.reaction == True, UserActivity.mode == UserActivity.MODE_ADD).count())

        reduced_reactions = (UserActivity.select(UserActivity,User).join(User).where(User.user_id==user_id,UserActivity.reaction == True, UserActivity.mode == UserActivity.MODE_REDUCE).count())

        return (added_reactions - reduced_reactions)