# my database classes"

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from app import db, login_manager, app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    favorites = db.relationship("Favorite", backref="user", lazy=True)
    shopping_list = db.relationship("ShoppingList", backref="user")

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def get_favorites(self):
        return Favorite.query.filter_by(user_id=self.id).all()
    
    def get_shopping_list(self):
       return ShoppingList.query.filter_by(user_id=self.id).all()

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    source = db.Column(db.String(255), nullable=True)
    url = db.Column(db.String(255), nullable=True)
    ingredients = db.Column(db.String(255), nullable=True)



class ShoppingList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.String(255), nullable=False) 
    ingredient = db.Column(db.String(255), nullable=False)
