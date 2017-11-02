from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from .models import User
from datetime import datetime
from .forms import LoginForm, RegistrationForm, EditForm
from werkzeug.utils import secure_filename

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
@app.route('/index')
def index():
    user = g.user
    posts = [
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html',
                           title='Home',
                           user=user)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


ALLOWED_EXTENSIONS = ['log', 'csv']  # <-- don't know where to put this

@app.route('/upload')
@login_required
def upload():
    return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
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
            f.save('/uploads_' + f_name)
            return redirect(url_for('index'))
        f.save(f.filename)
        return 'file uploaded successfully'
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
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User()
        user.email = request.form.get('email')
        user.password_hash = request.form.get('password') #will hash later
        db.session.add(user)
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


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
    return redirect(request.args.get('next') or url_for('index'))



@app.route('/logout')
def logout():
    logout_user()
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

"""