"""
Flask web application for fun
"""

from flask import Flask, render_template
from data import get_articles

app = Flask(__name__)
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


if __name__ == '__main__':
    app.run(debug=True)
