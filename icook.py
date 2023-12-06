""" customizing the app_context"""

from app import app, db
from app.models import Favorite, ShoppingList, User

@app.shell_context_processor
def provide_shell_context():
   """
   This function provides the shell context for the Flask application.
   It returns a dictionary that includes the database object and the User, Favorite, and ShoppingList classes.
   """
   return {'db': db, 'User': User, 'Favorite': Favorite, 'ShoppingList': ShoppingList}
