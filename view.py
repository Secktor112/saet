from models import Article
from models import Profiles
from models import Users
from flask import render_template
from flask import redirect
from flask import request
from app import app
from app import db


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/auth')
def auth():
    return render_template("auth.html")


@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)


@app.route('/posts/<int:id>')
def posts_detail(id):
    article = Article.query.get(id)
    return render_template("post_detail.html", article=article)


@app.route('/posts/<int:id>/del')
def posts_delete(id):
    article = Article.query.get_or_404(id)
    article.delete()
    if article.success:
        return redirect('/posts')
    return "При удалении статьи произошла ошибка"


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.update(
            request.form['title'],
            request.form['intro'],
            request.form['text']
        )

        if article.success:
            return redirect('/posts')
        return "При редактировании статьи произошла ошибка"

    else:
        return render_template("post-update.html", article=article)


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        article = Article(
            title=request.form['title'],
            intro=request.form['intro'],
            text=request.form['text']
        )

        article.create()

        if article.success:
            return redirect('/posts')
        return "При добавлении статьи произошла ошибка"

    else:
        return render_template("create-article.html")
