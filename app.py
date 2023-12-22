from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, Blueprint, render_template, request, make_response, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from Db import db
from Db.models import users, books
from flask_login import login_user, login_required, current_user, logout_user
app = Flask(__name__)

app.secret_key = "123"
user_db = "Tychinskiy_rgz_orm"
host_ip = "localhost"
host_port = "5432"
database_name = "Tychinskiy_base_rgz_orm"
password = "123"

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{user_db}:{password}@{host_ip}:{host_port}/{database_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

@login_manager.user_loader
def load_users(user_id):
    return users.query.get(int(user_id))


@app.route('/')
@app.route('/index')
def start():
    return redirect('/mainpage', code=302)


@app.route('/main', methods=['POST', 'GET'])
def mainpage():
    if current_user.is_authenticated:
        username = current_user.username
    else:
        username = "Кто Вы?"
    
    if request.method == 'POST':
        book_title = request.form.get('book')
        author = request.form.get('author')
        min_pages = request.form.get('min_pages')
        max_pages = request.form.get('max_pages')
        publisher = request.form.get('publisher')
        
        # Выполнить фильтрацию на основе введенных пользователем параметров
        filtered_books_list = filter_books_logic(book_title, author, min_pages, max_pages, publisher)
        return render_template('mainpage.html', all_books=filtered_books_list, username=username)

    else:
        # Раздел для отображения всех книг без фильтрации
        offset = request.args.get('offset', default=0, type=int)
        books_list = books.query.limit(20).offset(offset).all()
        return render_template('mainpage.html', all_books=books_list, username=username)

@app.route('/login', methods=['POST', 'GET'])
def login():
    error=''
    if request.method=='GET':
        return render_template('login.html')
        
    username_form=request.form.get('username')
    password_form=request.form.get('password')

    my_user=users.query.filter_by(username=username_form).first()
    
    if my_user=='' or password_form=='':
        error='не заполнены поля'
        return render_template('login.html', error=error)
    
    if my_user is not None:
        if check_password_hash(my_user.password, password_form):
            login_user(my_user, remember=False)
            return redirect('/main')
        else:
            error='неверный пароль'
            return render_template('login.html', error=error) 
    else:
        error='такого пользователя не существует'
        return render_template('login.html', error=error) 

    
@app.route('/register', methods=['post', 'get'])
def registerr():
    if request.method == 'GET':
        return render_template("register.html")

    username_form = request.form.get("username")
    password_form = request.form.get("password")

    if not username_form or not password_form:
        return render_template("register.html", errors='Заполните все поля')
    
    if not re.match("^[a-zA-Z0-9!@#$%^&*]+$", username_form) or not re.match("^[a-zA-Z0-9!@#$%^&*]+$", password_form):
        return render_template("register.html", errors='Логин и пароль должны состоять только из латинских букв, цифр и знаков препинания')
    
    if users.query.filter_by(username=username_form).first():
        return render_template("register.html", errors='Пользователь с таким логином уже существует')

    hashed_password = generate_password_hash(password_form, method="pbkdf2")
    new_user = users(username=username_form, password=hashed_password, is_admin=False)

    db.session.add(new_user)
    db.session.commit()
    return redirect("/login")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')