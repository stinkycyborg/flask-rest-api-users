from users import app, db, api
from users import UserResource
from flask_restful import Api, Resource
 
# Test getting a user
def test_get():
  userResource = UserResource()
  user = userResource.get(1)
  assert 'name' in user
  assert 'phone' in user
