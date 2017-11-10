from flask import render_template, flash, redirect, session, url_for, request, g, send_from_directory, Markup
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, models
from .models import User
from .forms import LoginForm, RegistrationForm, UploadForm
from werkzeug.security import generate_password_hash
from .utils import findUserFiles, file_save_seq
from config import UPLOAD_FOLDER, ANALYZED_CSV_FOLDER
from os import path
from .analyzer import usagePieChart, errorPieChart

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
    userFolder = path.join(app.root_path, UPLOAD_FOLDER, str(current_user.id))
    return send_from_directory(directory=userFolder, filename=filename)


@app.route('/usecase')
@login_required
def usecase():
    fileArray = findUserFiles(current_user)
    '''
    usage analysis statistics 
    '''
    return render_template(['usecase.html'],
                           title='Use Case',
                           files=fileArray)  # stats=statistics


@app.route('/errorcase')
@login_required
def errorcase():
    fileArray = findUserFiles(current_user)
    '''
    error analysis statistics 
    '''
    return render_template('errorcase.html',
                           title='Error Case',
                           files=fileArray)  # stats=statistics


@app.route('/graphs_err', methods=['GET', 'POST'])
def graphs_error():
    import matplotlib.pyplot as plt, mpld3

    filename = path.join(app.root_path, UPLOAD_FOLDER, str(current_user.id), request.args['filename'])
    # src/--.py functions should be called here to return matplot html
    dictionary = errorPieChart(filename, path.join(app.root_path, ANALYZED_CSV_FOLDER, "errorlog.csv"))

    errors = list(dictionary.keys())
    counts = list(dictionary.values())
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'red',
              'salmon', 'peru']
    patches, texts = plt.pie(counts, colors=colors, startangle=90)
    plt.legend(patches, errors, loc='upper right', )
    plt.axis('equal')
    plt.tight_layout()
    fig = plt.gcf()

    return mpld3.fig_to_html(fig, template_type='simple')


@app.route('/graphs_use', methods=['GET', 'POST'])
def graphs_usage():
    import matplotlib.pyplot as plt, mpld3

    filename = path.join(app.root_path, UPLOAD_FOLDER, str(current_user.id), request.args['filename'])
    # src/--.py functions should be called here to return matplot html
    dictionary = usagePieChart(filename, path.join(app.root_path, ANALYZED_CSV_FOLDER, "usagelog.csv"))

    usage = list(dictionary.keys())
    counts = list(dictionary.values())
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'red',
              'salmon', 'peru']
    patches, texts = plt.pie(counts, colors=colors, startangle=90)
    plt.legend(patches, usage, loc='upper right', )
    plt.axis('equal')
    plt.tight_layout()
    fig = plt.gcf()

    return mpld3.fig_to_html(fig, template_type='simple')


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
