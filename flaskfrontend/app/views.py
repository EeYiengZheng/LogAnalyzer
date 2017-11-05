from flask import render_template, flash, redirect, session, url_for, request, g, send_from_directory, Markup
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm, models
from .models import User, Log
from .forms import LoginForm, RegistrationForm, UploadForm
from werkzeug.security import generate_password_hash
from .utils import allowed_file, findUserFiles, file_save_seq


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
@app.route('/index')
def index():
    user = g.user
    return render_template('index.html',
                           title='Home',
                           user=user)


@app.route('/upload')
@login_required
def upload():
    form = UploadForm(request.form)
    return render_template('upload.html',
                           form=form,
                           title='Upload')


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'new_file' not in request.files:
            flash('No file part')
            return redirect(url_for('upload'))
        f = request.files['new_file']
        return file_save_seq(f)
    return



@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    from config import UPLOAD_FOLDER
    from os import path
    userFolder = path.join(app.root_path, UPLOAD_FOLDER, str(current_user.id))
    return send_from_directory(directory=userFolder, filename=filename)
    


@app.route('/usecase')
@login_required
def usecase():
    fileArray = findUserFiles(current_user)
    return render_template(['usecase.html'],
                           title='Use Case',
                           files=fileArray)


@app.route('/errorcase')
@login_required
def errorcase():
    fileArray = findUserFiles(current_user)
    return render_template('errorcase.html',
                           title='Error Case',
                           files=fileArray)


@app.route('/graphs', methods=['GET', 'POST'])
def graphs():
    import matplotlib.pyplot as plt, mpld3
    #random data to test matplot
    dictionary = {}
    dictionary['someError'] = 55
    dictionary['anotherOne'] = 5
    dictionary['alot'] = 123
    errors = list(dictionary.keys())
    counts = list(dictionary.values())
    fig, ax = plt.subplots()
    ax.plot(errors, counts)
    htmlOutput = mpld3.fig_to_html(fig)
    matplotHtml = Markup(htmlOutput)
    return matplotHtml


@app.route('/login', methods=['GET', 'POST'])
def login():
    # if g.user is not None and g.user.is_authenticated:
    #    return redirect(url_for('upload'))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid username or password.')
        session['remember_me'] = form.remember_me.data
    return render_template('login.html',
                           title='Sign In',
                           form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User()
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        user.password_hash = generate_password_hash(request.form.get('password'))
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You are logged out')
    return redirect(url_for('index'))
