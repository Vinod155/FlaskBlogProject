
from flask import render_template,url_for , flash, redirect ,request
from flaskblog.forms import RegisterationForm,LoginForm
from flaskblog.models import User, Post
from flaskblog import app, db, bcrypt
from flask_login import login_user , current_user ,logout_user ,login_required

posts=[
    {
        'author':'vinod',
        'title':'Blog Post Content',
        'content':'First Post Content',
        'date_posted':'20 April, 2018'       
    },
     {
        'author':'cory schafer',
        'title':'Blog Post Content 2',
        'content':'second Post Content',
        'date_posted':'20 April, 2019'       
    }
    
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title="About")

@app.route("/register" , methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=RegisterationForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Your account is now created !, you can now login",'success')
        return redirect(url_for('home')) #home page function 
    return render_template('register.html',title='Register',form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page=request.args.get('next')  #get returns none if there is no next parameter
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Log in Un-successful ! please check your username and password ","danger")
    return render_template('login.html',title='Login',form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account')
@login_required # this route will work only when we are logged in,this decorator will make sure we  are logged in then this route will work
def account():
    return render_template('account.html' ,title='Account')

