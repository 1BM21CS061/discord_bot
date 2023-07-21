from all_models import BaseModel
import peewee

class User(BaseModel):
    user_id = peewee.CharField(max_length=100) #defining a field called user_id in the table User
    total_points = peewee.FloatField(default=0) #defining a field called total_points in the table User

    @staticmethod   #can be called without using a class instance since the method now only belongs to User class
    def fetch_by_user_id(user_id):
        try:
            user = User.get(User.user_id==user_id) #searches the User table to find a tuple matching the user_id specified in the argument  
        except:
            user = User.create(user_id = user_id) #creates a tuple with the specified user_id if it can't find one
        return user
    
    @staticmethod 
    def get_leaderboard():
        """
    Retrieves the leaderboard users based on their total points.

    Returns:
    - list: A list of User objects representing the leaderboard users.
    """
        return User.select().order_by(User.total_points.desc())[:10]