import unittest
import sys
from app import db, app
from app.models import User, Favorite, ShoppingList
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from flask_testing import TestCase


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
      self.app_context = app.app_context()
      self.app_context.push()
      db.create_all()
      self.user = User(username='testuser', email='test@test.com', password='testpassword', image_file='default.jpg')
      db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@test.com')
        self.assertEqual(self.user.password, 'testpassword')

    def test_user_repr(self):
        self.assertEqual(str(self.user), "User('testuser', 'test@test.com', 'default.jpg')")

    


class FavoriteModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        self.favorite = Favorite(title='Test Favorite', user_id=1)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_favorite_creation(self):
        self.assertEqual(self.favorite.title, 'Test Favorite')
        self.assertEqual(self.favorite.user_id, 1)



class ShoppingListModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        self.shopping_list = ShoppingList(recipe_id='Test Recipe', user_id=1, ingredient='Test Ingredient')
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_shopping_list_creation(self):
        self.assertEqual(self.shopping_list.recipe_id, 'Test Recipe')
        self.assertEqual(self.shopping_list.user_id, 1)
        self.assertEqual(self.shopping_list.ingredient, 'Test Ingredient')


class TestForms(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_registration_form(self):
        form = RegistrationForm()
        self.assertFalse(form.validate())
        self.assertIn('This field is required.', form.username.errors)
        self.assertIn('This field is required.', form.email.errors)
        self.assertIn('This field is required.', form.password.errors)
        self.assertIn('This field is required.', form.confirm_password.errors)

    def test_registration_form(self):
       form = RegistrationForm()
       self.assertFalse(form.validate())
       self.assertIn('This field is required.', form.username.errors)
       self.assertIn('This field is required.', form.email.errors)
       self.assertIn('This field is required.', form.password.errors)
       self.assertIn('This field is required.', form.confirm_password.errors)

    def test_registration_form_valid(self):
        form = RegistrationForm(username='testuser', email='test@example.com',
                                password='testpassword', confirm_password='testpassword')
        self.assertTrue(form.validate())

    def test_login_form(self):
        form = LoginForm()
        self.assertFalse(form.validate())
        self.assertIn('This field is required.', form.email.errors)
        self.assertIn('This field is required.', form.password.errors)

    def test_login_form_valid(self):
        form = LoginForm(email='test@example.com', password='testpassword')
        self.assertTrue(form.validate())

    def test_update_account_form(self):
        form = UpdateAccountForm()
        self.assertFalse(form.validate())
        self.assertIn('This field is required.', form.username.errors)
        self.assertIn('This field is required.', form.email.errors)

    # def test_update_account_form_valid(self):
    #     form = UpdateAccountForm(username='testuser', email='test@example.com')
    #     self.assertTrue(form.validate())

    def test_request_reset_form(self):
        form = RequestResetForm()
        self.assertFalse(form.validate())
        self.assertIn('This field is required.', form.email.errors)

    # def test_request_reset_form_valid(self):
    #     form = RequestResetForm(email='test@example.com')
    #     self.assertTrue(form.validate())

    def test_reset_password_form(self):
        form = ResetPasswordForm()
        self.assertFalse(form.validate())
        self.assertIn('This field is required.', form.password.errors)
        self.assertIn('This field is required.', form.confirm_password.errors)

    def test_reset_password_form_valid(self):
        form = ResetPasswordForm(password='testpassword', confirm_password='testpassword')
        self.assertTrue(form.validate())

    def test_registration_form_valid(self):
        form = RegistrationForm(username='testuser', email='test@example.com',
                                password='testpassword', confirm_password='testpassword')
        self.assertTrue(form.validate())


if __name__ == '__main__':
    unittest.main()
