from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, query_db
from app.models import User
from app.forms import IndexForm, PostForm, FriendsForm, ProfileForm, CommentsForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():    
    form = IndexForm()
    wrong_pass = False
    
    if form.login.is_submitted() and form.login.submit.data:
        user = query_db('SELECT * FROM Users WHERE username= ?;',[form.login.username.data], one=True)
        if form.login.validate(form) and request.method == 'POST':
            if user == None:
                flash('Sorry, this user does not exist!')
            elif check_password_hash(user['password'],form.login.password.data):
            # elif user['password'] == form.login.password.data:
                login_user(User(user['id']), remember=form.login.remember_me.data)
                return redirect(url_for('stream'))
            else:
                flash('Sorry, wrong password! ')
                wrong_pass = True

    elif form.register.is_submitted() and form.register.submit.data:
        user= query_db('SELECT * FROM Users WHERE USERNAME = ?;',[form.register.username.data],one=True)
        if request.method == 'POST' and form.register.validate(form):
            query_db('INSERT INTO Users (username, first_name, last_name, password, secret_question) VALUES(?, ?, ?, ?, ?);', 
            [form.register.username.data, form.register.first_name.data, form.register.last_name.data,
            generate_password_hash(form.register.password.data), generate_password_hash(form.register.secret_question.data)])
            flash("User created.")
            return redirect(url_for('index'))
            

    if form.change_pass.is_submitted() and form.change_pass.submit.data:
        user = query_db('SELECT * FROM Users WHERE username=?;',[form.change_pass.username.data], one=True)
        if form.change_pass.validate(form):
            if user == None:
                flash("Sorry, this user does not exist!")
            elif user['secret_question'] == form.change_pass.secret_question.data:
                query_db('UPDATE Users SET password=? WHERE username=? ;',[generate_password_hash(form.change_pass.password.data), form.change_pass.username.data])
                flash("Password changed! Use your new password now")
            else:
                flash("That's not the right answer to the secret question")
        else:
            flash("Password and Confirm Password fields must contain the same data")
    return render_template('index.html', title='Welcome', form=form, wrong_pass=wrong_pass)

@app.route('/stream', methods=['GET', 'POST'])
@login_required
def stream():
    username = current_user.username
    form = PostForm()

    user = query_db('SELECT * FROM Users WHERE username= ?;',[username], one=True)
    if form.validate_on_submit() and request.method == 'POST':
        if form.image.data:
            path = os.path.join(app.config['UPLOAD_PATH'], form.image.data.filename)
            form.image.data.save(path)

        query_db('INSERT INTO Posts (u_id, content, image, creation_time) VALUES(?, ?, ?, ?);', [user['id'], form.content.data, form.image.data.filename, datetime.now()])
        return redirect(url_for('stream', username=username))

    
    posts = query_db('SELECT p.*, u.*, (SELECT COUNT(*) FROM Comments WHERE p_id=p.id) AS cc FROM Posts AS p JOIN Users AS u ON u.id=p.u_id WHERE p.u_id IN (SELECT u_id FROM Friends WHERE f_id=?) OR p.u_id IN (SELECT f_id FROM Friends WHERE u_id=?) OR p.u_id=? ORDER BY p.creation_time DESC;',[user['id'],user['id'],user['id'] ])
    return render_template('stream.html', title='Stream', username=username, form=form, posts=posts)


@app.route('/comments/<username>/<int:p_id>', methods=['GET', 'POST'])
@login_required
def comments(username, p_id):
    username = current_user.username
    form = CommentsForm()
    
    if form.validate_on_submit() and request.method == 'POST':

        user = query_db('SELECT * FROM Users WHERE username= ?;',[username], one=True)

        query_db('INSERT INTO Comments (p_id, u_id, comment, creation_time) VALUES(?, ?, ?, ?);',[p_id, user['id'], form.comment.data, datetime.now()])

    post = query_db('SELECT * FROM Posts WHERE id=?;',[p_id], one=True)
    
    all_comments = query_db('SELECT DISTINCT * FROM Comments AS c JOIN Users AS u ON c.u_id=u.id WHERE c.p_id=? ORDER BY c.creation_time DESC;',[p_id])
    return render_template('comments.html', title='Comments', username=username, form=form, post=post, comments=all_comments)


@app.route('/friends/<username>', methods=['GET', 'POST'])
@login_required
def friends(username):
    form = FriendsForm()
    
    user = query_db('SELECT * FROM Users WHERE username= ?;',[username], one=True)
    
    if form.validate_on_submit() and request.method == 'POST':
        
        friend = query_db('SELECT * FROM Users WHERE username= ?;',[form.username.data], one=True)
        if friend is None:
            flash('User does not exist')
        else:
            
            if current_user.username == form.username.data:
                flash('You kan not add your self as a friend')
            else:
                query_db('INSERT INTO Friends (u_id, f_id) VALUES(?, ?);',[user['id'], friend['id']])
    
    
    all_friends = query_db('SELECT * FROM Friends AS f JOIN Users as u ON f.f_id=u.id WHERE f.u_id=? AND f.f_id!=? ;',[user['id'], user['id']])
    return render_template('friends.html', title='Friends', username=username, friends=all_friends, form=form, current_username = current_user.username)


@app.route('/profile/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    form = ProfileForm()

    if form.validate_on_submit():
        
        query_db('UPDATE Users SET education=?, employment=?, music=?, movie=?, nationality=?, birthday= ? WHERE username=? ;',[
            form.education.data, form.employment.data, form.music.data, form.movie.data, form.nationality.data, form.birthday.data, username
        ])
        return redirect(url_for('profile', username=username))

    user = query_db('SELECT * FROM Users WHERE username= ?;',[username], one=True)
    if user is None:
        flash("This user does not exist")
        return redirect(url_for('profile', username=current_user.username))

    return render_template('profile.html', title='profile', username=username, user=user, form=form, current_username = current_user.username)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
