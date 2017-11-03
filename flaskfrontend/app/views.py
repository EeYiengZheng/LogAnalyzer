from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm, models
from config import ALLOWED_EXTENSIONS
from .models import User
from .forms import LoginForm, RegistrationForm, EditForm
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
import os

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


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload')
@login_required
def upload():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        f = request.files['file']
        if f.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if f and allowed_file(f.filename):
            f_name = secure_filename(f.filename)
            f.save(os.path.join(app.root_path + app.config['UPLOAD_FOLDER'], f_name))
            flash('File upload succesful')
            return redirect(url_for('index'))
        return 'Invalid file. Only uploaded .log or .csv files!'
    return


@app.route('/usecase')
@login_required
def usecase():
    user = g.user
    return render_template('usecase.html',
                           title='Use Case',
                           user=user)


@app.route('/errorcase')
@login_required
def errorcase():
    user = g.user
    return render_template('usecase.html',
                           title='Error Case',
                           user=user)


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
        user.email = request.form.get('email')
        user.password_hash = generate_password_hash(request.form.get('password'))
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

"""
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))"""


@app.route('/logout')
def logout():
    logout_user()
    flash('Yoiu are logged out')
    return redirect(url_for('index'))


"""
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()

    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        form.file.data.save('uploads/' + filename)
        return redirect(url_for('index'))

    return render_template('index.html', form=form)


from logMetrics import errorPieChart, usagePieChart, errorRate


@app.route('/graph')
def show_graph():
    errpie = errorPieChart({{url_for('static', filename='syslog3.log')}},
                           {{url_for('static', filename='errorlog.csv')}})
    usepie = usagePieChart({{url_for('static', filename='syslog3.log')}},
                           {{url_for('static', filename='usagelog.csv')}})
    errrate = errorRate({{url_for('static', filename='errorlog.csv')}})
    return render_template('graph.html', epie=errpie, upie=usepie, err=errrate)
"""