import os
import secrets
from PIL import Image
from flask import jsonify, render_template, url_for, flash, redirect, request
from app.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                             RequestResetForm, ResetPasswordForm)
from app import app, db, bcrypt
from app.models import User, Favorite
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message, Mail
import requests
from app.models import Favorite, User, ShoppingList

with app.app_context():
   db.create_all()

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route("/home")
def home():
    """Render the home page."""
    return render_template('index.html')

@app.route("/recipe/<recipe_id>")
def recipe(recipe_id):
  """Render the recipe page for a given recipe ID."""
  print(recipe_id)
  url = f"https://api.edamam.com/api/recipes/v2/{recipe_id}?type=public&app_id=5f8d15e8&app_key=7e4f94d1f57158c014144b6f0864dc56"

  response = requests.get(url).json()

  recipe_dict = {}

  recipe_dict["title"] = response.get("recipe").get("label")
  recipe_dict["image"] = response.get("recipe").get("image") 
  recipe_dict["source"] = response.get("recipe").get("source")
  recipe_dict["url"] = response.get("recipe").get("url")
  recipe_dict["ingredients_list"] = response.get("recipe").get("ingredientLines")

  return render_template('recipe.html', recipe=recipe_dict,id=recipe_id)

   
@app.route("/add-to-favorites", methods=["POST"])
@login_required
def add_to_favorites():
    """Add a recipe to the user's favorites."""
    if request.method == "POST":
        recipe_id = request.form.get("recipe_id")
        print(recipe_id)

        # Fetch recipe details using the recipe_id (similar to your /recipe/<recipe_id> route)
        url = f"https://api.edamam.com/api/recipes/v2/{recipe_id}"
        params = {
            "type": "public",
            "app_id": "5f8d15e8",
            "app_key": "7e4f94d1f57158c014144b6f0864dc56",
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            recipe_details = response.json().get("recipe")
            if recipe_details:
                # Create a Favorite object and save it to the database
                favorite = Favorite(
                    user_id=current_user.id,  # Assuming you're using Flask-Login for authentication
                    title=recipe_details.get("label"),
                    image=recipe_details.get("image"),
                    source=recipe_details.get("source"),
                    url=recipe_details.get("url"),

                )

                db.session.add(favorite)
                db.session.commit()

                flash("Recipe added to favorites", "success")
            else:
                flash("Error fetching recipe details from the API", "error")
        else:
            flash("Error in API request. Status Code: {}".format(response.status_code), "error")

    # Redirect the user back to the recipe page
    return redirect(url_for("recipe", recipe_id=recipe_id))

@app.route("/about")
def about():
    """Render the about page."""
    return render_template('landing.html', title='About')

@app.route('/recipe/<id>', methods=['GET', ])
def recipe_detail(id):
     """Print the detailed view of a recipe."""
     recipe = get_recipe_details(id)
     return render_template('recipe_details.html', recipe=recipe)

@app.route("/register", methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    """Handle user logout."""
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    """Renders user's account details"""
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

def send_reset_email(user):
    """Send a password reset email to the user."""
    mail = Mail(app)
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    """Handle the request to reset the user's password."""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_password.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    """Handle the password reset token."""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

@app.route('/favorites')
def favorites():
   # Get the favorites of the current user
   favorites = current_user.get_favorites() if current_user.is_authenticated else []

   # Pass the favorites to the template
   return render_template('favourites.html', favorites=favorites)

@app.route('/delete-favorite/<int:favorite_id>', methods=['POST'])
@login_required
def delete_favorite(favorite_id):
    """Delete a recipe from the user's favorites."""
    favorite = Favorite.query.get_or_404(favorite_id)

    # Ensure that the current user owns the favorite before deleting
    if favorite.user_id == current_user.id:
        db.session.delete(favorite)
        db.session.commit()
        flash('Recipe deleted from favorites', 'success')
    else:
        flash('You are not authorized to delete this recipe', 'danger')

    return redirect(url_for('favorites'))


@app.route('/delete-shopping-list/<int:id>', methods=['POST'])
@login_required
def delete_shopping(id):
    """Delete an item from the user's shopping list."""
    del_shopping = ShoppingList.query.get_or_404(id)

    # Ensure that the current user owns the favorite before deleting
    if  del_shopping.user_id == current_user.id:
        db.session.delete(del_shopping)
        db.session.commit()
        flash('Ingredient deleted from shopping list', 'success')
    else:
        flash('You are not authorized to delete this recipe', 'danger')

    return redirect(url_for('favorites'))


# Example route for adding to shopping list

@app.route('/add-to-shopping-list', methods=['POST'])
@login_required
def add_to_shopping_list():
    """Add selected ingredients to the user's shopping list."""
    user_id = current_user.id
    recipe_id = request.form.get('recipe_id')
    selected_ingredients = request.form.getlist('ingredients[]')
    print(user_id)
    print(recipe_id)
    print(selected_ingredients)

    # Create ShoppingList entries for each selected ingredient
    for ingredient in selected_ingredients:
        shopping_list_item = ShoppingList(user_id=user_id, recipe_id=recipe_id, ingredient=ingredient)
        db.session.add(shopping_list_item)

    db.session.commit()

    flash("Ingredients added to your shopping list", "success")

    return redirect(url_for("recipe", recipe_id=recipe_id))

