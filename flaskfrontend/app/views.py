from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm, models
from .models import User, Log
from .forms import LoginForm, RegistrationForm, UploadForm
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash


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
    from .utils import allowed_file
    from os import path, remove, makedirs
    from config import UPLOAD_FOLDER
    import hashlib
    if request.method == 'POST':
        if 'new_file' not in request.files:
            flash('No file part')
            return redirect(url_for('upload'))
        f = request.files['new_file']
        if f.filename == '':
            flash('No selected file')
            return redirect(url_for('upload'))
        if f and allowed_file(f.filename):
            hasher = hashlib.sha256()
            BLOCKSIZE = 65536
            tmp_path = path.join('tmp', f.filename)
            f.save(tmp_path)
            with open(tmp_path, 'rb') as afile:
                buf = afile.read(BLOCKSIZE)
                while len(buf) > 0:
                    hasher.update(buf)
                    buf = afile.read(BLOCKSIZE)
            remove(tmp_path)
            hash = hasher.hexdigest()
            log_hash = models.Log.query.filter_by(file_hash=hash).first()
            f_name = secure_filename(f.filename)
            i_f_name = f_name.rsplit('.', 1)[0] + '_'
            i = 0
            tmp_path = path.join(app.root_path, UPLOAD_FOLDER, str(current_user.id))
            if not path.exists(tmp_path):
                makedirs(tmp_path)
            while path.isfile(path.join(app.root_path, UPLOAD_FOLDER, str(current_user.id),
                                        i_f_name + str(i) + '.' + f_name.rsplit('.', 1)[1])):
                i += 1
            i_f_name = i_f_name + str(i) + '.' + f_name.rsplit('.', 1)[1]
            if log_hash is not None:
                flash('Upload unsuccessful: file already exist')
                return redirect(url_for('upload'))
            else:
                new_log = Log(owner=current_user)
                new_log.file_hash = hash
                new_log.filename = f_name
                new_log.internal_f_name = i_f_name
                db.session.add(new_log)
                db.session.commit()

                f.save(path.join(app.root_path, UPLOAD_FOLDER, str(current_user.id), i_f_name))
                flash('File uploaded: ' + f_name)
                return redirect(url_for('index'))
        return redirect(url_for('upload'))
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


@app.route('/logout')
def logout():
    logout_user()
    flash('You are logged out')
    return redirect(url_for('index'))
