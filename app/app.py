from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

posts = [
    {
        "author": "Lavender",
        "title": "Chapo Beans",
        "ingredients": ["flour", "beans"],
        "method": ["Make chapos", "cook beans", "serve while hot"],
        "date_posted": "Nov 20, 2023",
        "date_updated": "Nov 22, 2023",
    },
    {
        "author": "Jane Doe",
        "title": "Ugali Beef",
        "ingredients": ["flour", "water", "beef", "onions", "tomatoes", "oil", "salt", "dhania"],
        "method": ["Make ugali", "cook beef", "serve while hot"],
        "date_posted": "Oct 20, 2023",
        "date_updated": "Oct 22, 2023",
    },
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)