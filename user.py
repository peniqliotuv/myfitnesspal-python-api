from flask.ext.login import UserMixin

class User(UserMixin):

  user_database = {}

  def __init__(self, username, client):
    self.id = username
    self.client = client

  @classmethod
  def get(cls, id):
    return cls.user_database.get(id)
  
