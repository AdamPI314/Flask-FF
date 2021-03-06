"""
Flask web application for fun
"""
from flask import Flask, render_template, flash, redirect, url_for, session, request
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from functools import wraps
from models import *


app = Flask(__name__)
app.secret_key = 'secret666'

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Initialize MySQL
mysql = MySQL(app)


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
    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM articles")

    articles = cur.fetchall()

    if result > 0:
        return render_template('articles.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('articles.html', msg=msg)
    cur.close()


@app.route('/get_article/<string:id>/')
def get_article(id):
    """
    single article page
    """
    cur = mysql.connection.cursor()

    _ = cur.execute("SELECT * FROM articles WHERE id = %s", [id])

    article = cur.fetchone()

    return render_template('get_article.html', article=article)


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

# user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    login route
    """
    if request.method == 'POST':
        # get form fields
        username = request.form['username']
        password_candidate = request.form['password']

        # create cursor
        cur = mysql.connection.cursor()

        # get user by username
        result = cur.execute(
            "SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            # get stored hash
            data = cur.fetchone()
            password = data['password']

            # compare passwords
            if sha256_crypt.verify(password_candidate, password):
                app.logger.info('PASSWORD MATCHED')
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)

        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

        cur.close()
    return render_template('login.html')


# check if user logged in
def is_logged_in(f):
    """
    is logged in decorator
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        """
        wrap from template
        """
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap


@app.route('/logout')
@is_logged_in
def logout():
    """
    logout
    """
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('home'))


@app.route('/dashboard')
@is_logged_in
def dashboard():
    """
    dash board
    """
    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM articles")

    articles = cur.fetchall()

    if result > 0:
        return render_template('dashboard.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('dashboard.html', msg=msg)
    cur.close()


@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_article():
    """
    add article
    """
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data

        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO articles(title, body, author) VALUES(%s, %s, %s)",
                    (title, body, session['username']))

        mysql.connection.commit()

        cur.close()

        flash('Article Created', 'success')

        return redirect(url_for('dashboard'))

    return render_template('add_article.html', form=form)


@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_article(id):
    """
    edit article 
    """
    cur = mysql.connection.cursor()

    _ = cur.execute("SELECT * FROM articles where id = %s", [id])

    article = cur.fetchone()

    form = ArticleForm(request.form)
    form.title.data = article['title']
    form.body.data = article['body']

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']

        cur.execute(
            "UPDATE articles SET title=%s, body=%s WHERE id = %s", (title, body, id))

        mysql.connection.commit()

        cur.close()

        flash('Article Updated', 'success')

        return redirect(url_for('dashboard'))

    return render_template('edit_article.html', form=form)


@app.route('/delete_article/<string:id>', methods=['POST'])
@is_logged_in
def delete_article(id):
    """
    delete article
    """
    cur = mysql.connection.cursor()

    cur.execute("DELETE FROM articles WHERE ID = %s", [id])

    mysql.connection.commit()

    cur.close()

    flash('Article Deleted', 'success')

    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True)
