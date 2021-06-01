from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from models import Article, User, Instruments, Type, Family, Cart
from flask import render_template, flash, url_for
from flask import redirect
from flask import request
from app import app
from app import db
from flask import session
from utility import get_template, get_role, Inst_type, Inst_family


@app.route('/')
def index():
    return get_template("index.html")


@app.route('/catalog')
def catalog():
    return get_template("catalog.html")


@app.route('/instrument')
def catalog_route():
    type_id = request.args.get("type_id")
    types_id = Instruments.query.filter_by(type_id=type_id).all()

    return get_template("instrument.html", types_id=types_id)


@app.route('/instrument_family')
def catalog_route_fam():
    family_id = request.args.get("family_id")
    families_id = Instruments.query.filter_by(family_id=family_id).all()

    return get_template("instrument_family.html", families_id=families_id)


@app.route('/instrument/<int:id>')
def inst_detail(id):
    inst = Instruments.query.filter_by(id=id).first()
    return get_template("inst_detail.html", inst=inst)


@app.route('/service')
def service():
    return get_template("service.html")


@app.route('/auth', methods=['POST', 'GET'])
def auth():
    login = request.form.get('login')
    password = request.form.get('psw')

    if login and password:
        user = User.query.filter_by(login=login).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            session['userid'] = user.id
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect('/')
        else:
            flash('Login or password is not correct')
    else:
        flash('Please fill login and password fields')

    return render_template('auth.html')


@app.route('/get')
def get():
    print(session['userid'])
    return ''


@app.route('/register', methods=['POST', 'GET'])
def register():
    login = request.form.get('login')
    password = request.form.get('psw')
    password2 = request.form.get('psw2')
    name = request.form.get('name')
    email = request.form.get('email')

    # print(name.encode())

    if request.method == 'POST':
        if not (login or password or password2 or name or email):
            flash('Please, fill all fields!')
        elif password != password2:
            flash('Passwords are not equal!')
        elif not (password or password2):
            flash('Please, fill all fields!')
        elif not name or not email:
            flash('Please, fill all fields!')
        else:
            hash_pwd = generate_password_hash(password)

            try:
                new_user = User(
                    login=login,
                    password=hash_pwd,
                    name=name,
                    email=email
                )
                db.session.add(new_user)
                db.session.commit()
                return redirect('/auth')
            except:
                flash('username or email is incorrect')
            # try:
            #     new_profile =

            return redirect('/register')

    return render_template('register.html')


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    logout_user()
    session['userid'] = None
    return render_template("index.html")


@app.route('/about')
def about():
    return get_template("about.html")


@app.route('/posts')
def posts():
    if get_role(session['userid']) == 1:
        is_admin = True
    else:
        is_admin = False
    articles = Article.query.order_by(Article.date.desc()).all()
    return get_template("posts.html", articles=articles, admin=is_admin)


@app.route('/posts/<int:id>')
def posts_detail(id):
    if get_role(session['userid']) == 1:
        is_admin = True
    else:
        is_admin = False
    article = Article.query.get(id)
    return get_template("post_detail.html", article=article, admin=is_admin)


@app.route('/posts/<int:id>/del')
def posts_delete(id):
    if get_role(session['userid']) != 1:
        return redirect('/')

    article = Article.query.get_or_404(id)
    article.delete()
    if article.success:
        return redirect('/posts')
    return "При удалении статьи произошла ошибка"


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    if get_role(session['userid']) != 1:
        return redirect('/')

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
        return get_template("post-update.html", article=article)


@app.route('/create-article', methods=['POST', 'GET'])
@login_required
def create_article():
    if get_role(session['userid']) != 1:
        return redirect('/')

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
        return get_template("create-article.html")


@app.route('/profile', methods=['GET'])
@login_required
def profile():
    return get_template("profile.html")


@app.route('/add_inst', methods=['POST', 'GET'])
@login_required
def add_inst():
    types = Type.query.all()

    families = Family.query.all()

    name = request.form.get('name')
    type = request.form.get('type')
    family = request.form.get('family')
    photo = request.form.get('photo')
    price = request.form.get('price')
    options = request.form.get('options')
    vendor = request.form.get('vendor')
    disc = request.form.get('disc')

    sel_type = Type.query.filter_by(name_ru=type).first()
    sel_family = Family.query.filter_by(name_ru=family).first()



    try:
        new_inst = Instruments(
            name=name,
            type_id=sel_type.id,
            family_id=sel_family.id,
            photo=photo,
            price=price,
            options=options,
            vendor=vendor,
            disc=disc
        )
        db.session.add(new_inst)
        db.session.commit()
        return redirect('/add_inst')
    except Exception as e:
        print(e)
    # try:
    #     new_profile =

    return get_template("add_inst.html", types=types, families=families)


@app.route('/cart', methods=['GET'])
@login_required
def cart():
    carts = Cart.query.filter_by(user_id=session['userid']).all()
    for cart in carts:
        cart.inst = Instruments.query.filter_by(id=cart.inst_id).first()

    return get_template("cart.html", carts=carts)


@app.route('/cart/<int:id>/del')
@login_required
def cart_delete(id):
    cart = Cart.query.get_or_404(id)
    cart.delete()
    if cart.success:
        return redirect('/cart')
    return "При удалении статьи произошла ошибка"


@app.route('/add_cart/<int:id>', methods=['GET'])
@login_required
def add_cart(id):
    try:
        new_cart = Cart(
            user_id = session['userid'],
            inst_id = id
        )
        db.session.add(new_cart)
        db.session.commit()
        return redirect('/cart')
    except:
        print('Не удалось')



@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('auth') + '?next=' + request.url)
    return response
