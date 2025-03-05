from t_flask import app, db, mail, bcrypt
from flask import render_template, url_for, redirect, flash, session, request
from t_flask.forms import RegistrationForm, LoginForm, ResetRequestForm, ResetPaswordForm, UpdateAccountForm
from t_flask.models import User, UserDetails
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import os
import uuid


@app.route('/')
@app.route('/home')
def homepage():
    return render_template('homepage.html', title='Home' )

@app.route('/about')
def about():
    return render_template('about.html', title='About' )

def save_image(picture_file):
    if not picture_file:
        return None

    picture_name = picture_file.filename
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_name)
    picture_file.save(picture_path)
    return picture_name

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form=UpdateAccountForm()
    user_details = UserDetails.query.filter_by(firstname=form.firstname.data,lastname=form.lastname.data,user_id=current_user.id).first()

    user_details_list = UserDetails.query.filter_by(user_id=current_user.id).all()

    if len(user_details_list) > 1:
        for extra_details in user_details_list[1:]:
            db.session.delete(extra_details)
        db.session.commit() 


    user_details = user_details_list[0] if user_details_list else None

    if form.validate_on_submit():
        if form.picture.data:
            image_file = save_image(form.picture.data)
            current_user.image_file = image_file

        current_user.username = form.username.data
        current_user.email = form.email.data


        if user_details:
            user_details.firstname = form.firstname.data
            user_details.lastname = form.lastname.data
        else:
            user_details = UserDetails(
                firstname=form.firstname.data,
                lastname=form.lastname.data,
                user_id=current_user.id
            )
            db.session.add(user_details)

        db.session.commit()

        flash('Your account has been updated!','success')
        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.firstname.data = current_user.details[-1].firstname
        form.lastname.data = current_user.details[-1].lastname
        if user_details:
            form.firstname.data = user_details.firstname
            form.lastname.data = user_details.lastname
    image_url=url_for('static', filename='profile_pics/' + current_user.image_file) if current_user.image_file else url_for('static', filename='default.jpg')

    return render_template('account.html', title='Account', legend= 'Account details', form=form, image_url=image_url)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = RegistrationForm()
    if form.validate_on_submit():
        encrypted_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username= form.username.data, email=form.email.data, password=encrypted_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created! You can now log in successfully as {form.username.data}!', 'success')

        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Loging successful for {form.email.data} !', category='success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('account'))
        else:
             flash(f'Loging unsuccessful for {form.email.data}!', category='danger')

    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out!', category='info')
    return redirect(url_for('login'))

def send_mail(user):
    token = user.get_token()
    msg = Message('Password Reset Request', sender='noreply@tttsh.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:

{url_for('reset_token', token=token, _external=True)}

If you did not make this request, please ignore this email.
'''
    mail.send(msg)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    form = ResetRequestForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user:
            send_mail(user)
            flash(f'Password reset request has been sent to {form.email.data}', category='success')
            return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form, legend='Reset Password')



@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    user=User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', category='warning')
        return redirect(url_for('reset_request'))

    form = ResetPaswordForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password=hashed_password
        db.session.commit()
        flash(f'Password reset for {user.email} has been successful!', category='success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title="Change Password", form=form, legend="Change Password")