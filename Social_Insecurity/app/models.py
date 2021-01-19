from flask_login import UserMixin
from app import login, query_db, get_db, app

@login.user_loader
def load_user(id):
    return User(id)
    
class User(UserMixin):
    def __init__(self, id):
        user = query_db('SELECT * FROM Users WHERE id =?;', [id], one=True)
        self.id = id
        self.first_name = user['first_name']
        self.last_name = user['last_name']
        self.username = user['username']
        self.password = user['password']


