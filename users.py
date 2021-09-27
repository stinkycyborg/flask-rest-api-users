from collections import UserList
import json
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from flask_cors import CORS, cross_origin


# Create Flask app and RESTful API
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
marsh = Marshmallow(app)
api = Api(app)
cors = CORS(app)


# 
# Create 'User' schema
# 

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50))
  phone = db.Column(db.String(50))

  def __repr__(self):
    return '<User %s>' % self.name

class UserSchema(marsh.Schema):
  class Meta:
    fields = ('id', 'name', 'phone')
    model = User

user_schema = UserSchema()
users_schema = UserSchema(many=True)


#
# Create 'User' RESTful resource
#

class UserListResource(Resource):
  def get(self):
    users = User.query.all()
    return users_schema.dump(users)

  def post(self):
    new_user = User(
      name = request.json['name'],
      phone = request.json['phone']
    )
    db.session.add(new_user)
    db.session.commit()
    return user_schema.dump(new_user)

class UserResource(Resource):
  def get(self, user_id):
    user = User.query.get_or_404(user_id)
    return user_schema.dump(user)
  
  def patch(self, user_id):
    user = User.query.get_or_404(user_id)
    if 'name' in request.json:
      user.name = request.json['name'] 
    if 'phone' in request.json:
      user.phone = request.json['phone']
    db.session.commit()
    return user_schema.dump(user)

  def delete(self, user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return '', 204


#
# Add 'User' resource to API.
#

api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/users/<int:user_id>')


#
# Dummy response for root path.
#

@app.route('/')
@cross_origin()
def hello():
  hello_dict = {
    'message': 'Hello!'
  }
  return json.dumps(hello_dict)


#
# Run the Flask app when executing `python3 main.py`
#

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)