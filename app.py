"""
Flask web application for fun
"""

from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from data import get_articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt


app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Initialize MySQL
mysql = MySQL(app)

Articles = get_articles()


@app.route('/')
def home():
    """
    home page
    """
    return render_template('home.html')


@app.route('/about')
def about():
    """
    about page
    """
    return render_template('about.html')


@app.route('/articles')
def articles():
    """
    articles page
    """
    return render_template('articles.html', articles=Articles)


@app.route('/article/<string:id>/')
def article(id):
    """
    single article page
    """
    return render_template('article.html', id=id)


class RegisterForm(Form):
    """
    Register Form/model
    """
    name = StringField('Name', [validators.Length(min=1, max=50)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    username = StringField('Username', [validators.Length(min=5, max=25)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match.')
    ])
    confirm = PasswordField('Confirm Password')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    register route
    """
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)",
                    (name, email, username, password))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can log in.', 'success')
        return redirect(url_for('home'))

    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.secret_key = 'secret666'
    app.run(debug=True)
