from flask import Flask,render_template, request, redirect, url_for, abort, flash, session
import sqlalchemy
from werkzeug.security import generate_password_hash
from flask_login import login_manager, login_user, login_required,logout_user,current_user,LoginManager
from flask_user import roles_required
from datetime import datetime
from models.post_model import Posts
from models.user_model import UserModel
from models.comment_model import Comments
from models.category_model import Category
from models.tag_model import Tags
from models.roles import Role
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine,desc


# class ConfigClass(object):
#     """ Flask application config """
#     # Flask-Mail SMTP server settings
#     MAIL_SERVER = 'smtp.gmail.com'
#     MAIL_PORT = 465
#     MAIL_USE_SSL = True
#     MAIL_USE_TLS = False
#     MAIL_USERNAME = 'email@example.com'
#     MAIL_PASSWORD = 'password'
#     MAIL_DEFAULT_SENDER = '"MyApp" <noreply@example.com>'
#     # Flask-User settings
#     USER_APP_NAME = "Flask-User Basic App"      # Shown in and email templates and page footers
#     USER_ENABLE_EMAIL = True        # Enable email authentication
#     USER_ENABLE_USERNAME = False    # Disable username authentication
#     USER_EMAIL_SENDER_NAME = USER_APP_NAME
#     USER_EMAIL_SENDER_EMAIL = "noreply@example.com"

app = Flask(__name__)


# app.config.from_object(__name__+'.ConfigClass')
app.config['SECRET_KEY'] = "Thisshouldbesecret!"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/flaskapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

engine = create_engine('mysql+pymysql://root:@localhost/flaskapp')
Session = sessionmaker(bind = engine)
sess = Session()

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))

# APP ROUTES

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # remember = True if request.form.get('remember') else False

        user = UserModel.query.filter_by(email=email).first()
        # if user:
        #     print('User found')
        #     if user.check_password(password):
        #         return redirect(url_for('home'))
        #     flash('Email or Password Incorrect. Check and Try Again!')
        # flash('Email or Password Incorrect. Check and Try Again!')
        # return redirect(url_for('login'))
        

        if not user and user.check_password(password):
            flash('Email or Password Incorrect. Check and Try Again!')
            return redirect(url_for('login'))  
        login_user(user)    
        return redirect(url_for('home'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    session.clear()
    return redirect(url_for('index'))

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        registeredAt = datetime.now()
        firstName = request.form['firstName']
        lastName = request.form['lastName'] 
        email = request.form['email']
        passwordHash = generate_password_hash(request.form['passwordHash'],method='sha256')
        is_admin=False

        user = UserModel.query.filter_by(email=email).first()

        if user:
            flash('User with that email already exists.')
            return redirect(url_for('signup'))
        
        new_user=UserModel(firstName,lastName,email,passwordHash,registeredAt,is_admin)
        new_user.save_to_db()
        return redirect(url_for('login'))
    
    return render_template('sign_up.html')

@app.route('/')
def index():
    if not UserModel.query.filter(UserModel.email == 'zekah54@gmail.com').first():
        passwordHash = generate_password_hash('Admin',method='sha256')
        user = UserModel(
            firstName='Admin',
            lastName='Chamakuvangu',
            email='zekah54@gmail.com',
            passwordHash=passwordHash,
            registeredAt=datetime.now(),
            is_admin=True
        )
        user.roles.append(Role(name='Admin'))
        user.roles.append(Role(name='Agent'))
        db.session.add(user)
        db.session.commit()

    posts = Posts.query.order_by(desc(Posts.publishedAt)).all()
    categories = Category.query.all()
    # users = UserModel.query.all()
    if current_user.is_authenticated and current_user.is_admin==False:
        return redirect(url_for('home'))
    return render_template('index.html', posts = posts,categories = categories)

@app.route('/home')
@login_required
def home():
    posts = Posts.query.order_by(desc(Posts.publishedAt)).all()
    categories = Category.query.all()
    return render_template('home.html', posts = posts,categories = categories, user = current_user)

@app.route('/category/<string:category>')
def category(category):
    try:
        cat = Category.query.filter_by(category=category).one()
        posts = Posts.query.filter_by(category_id = cat.id).all()
        return render_template('category.html', posts = posts, user = current_user)
    except sqlalchemy.orm.exc.NoResultFound:
        abort(404)    

@app.route('/tags/<string:tag>')
def tag(tag):
    try:
        tag = Tags.query.filter_by(tag=tag).one()
        posts = Posts.query.filter_by(tag_id = tag.id).all()
        return render_template('category.html', posts = posts, user = current_user)
    except sqlalchemy.orm.exc.NoResultFound:
        abort(404)    

@app.route('/contact')
def contact():
    user = current_user
    return render_template('contact.html',user = user)

@app.route('/post/<string:slug>')
def post(slug):
    try:
        # users = sess.query(UserModel, Comments).filter(UserModel.id == Comments.user_id).all()
        post = Posts.query.filter_by(slug=slug).one()
        tags = Tags.query.filter_by(id=post.tag_id).all()
        comments = Comments.query.filter_by(post_id=post.id).order_by(desc(Comments.publishedOn)).all()
        # tags = 
        users = UserModel.query.all()
        if comments:
            return render_template('post.html', post=post,comments =comments, users = users,tags=tags)
        return render_template('post.html', post=post,users = users,tags=tags)
    except sqlalchemy.orm.exc.NoResultFound:
        abort(404)

@app.route('/posts/<string:slug>',methods=['GET','POST'])
@login_required
def posts(slug):
    if request.method == 'POST':
        publishedOn = datetime.now()
        content = request.form['comment']
        post = Posts.query.filter_by(slug=slug).one()
        post_id = post.id
        user_id = current_user.id
        new_comment = Comments(content,publishedOn,post_id,user_id)
        new_comment.save_to_db()

    try:
        # users = sess.query(UserModel, Comments).filter(UserModel.id == Comments.user_id).all()
        post = Posts.query.filter_by(slug=slug).one()
        tags = Tags.query.filter_by(id=post.tag_id).all()
        comments = Comments.query.filter_by(post_id=post.id).all()
        users = UserModel.query.all()
        if comments:
            return render_template('posts.html', post=post,comments =comments,tags=tags, users = users)
        return render_template('posts.html', post=post,users = users,tags=tags)
    except sqlalchemy.orm.exc.NoResultFound:
        abort(404)

@app.route('/admin')
@roles_required('Admin')
def admin_page():
    return redirect('admin')


@app.route('/about')
def about():
    return render_template('about.html',user = current_user)

if __name__ == "__main__":
    from flask_admin import Admin
    from flask_admin.contrib.sqla import ModelView
    from db import db
    db.init_app(app)

    class Controller(ModelView):
        def is_accessible(self):
            if current_user.is_authenticated:
                if current_user.is_admin == True:
                    return current_user.is_authenticated
            else:
                return abort(404)
            

        def not_auth(self):
            return redirect(url_for('login'))

    admin = Admin(app,name='Control Panel')
    admin.add_view(Controller(Posts, db.session))
    admin.add_view(Controller(Category, db.session))
    admin.add_view(Controller(Comments, db.session))
    admin.add_view(Controller(Tags,db.session))
    admin.add_view(Controller(UserModel, db.session))

    app.run(debug=True, port='5000') #host='0.0.0.0'