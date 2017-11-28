import datetime
from os import path, makedirs

import matplotlib.pyplot as plt
import mpld3
import zipfile
from dateutil import parser
from flask import render_template, flash, redirect, session, url_for, request, g, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash

from app import app, db, models
from config import UPLOAD_FOLDER, ANALYZED_CSV_FOLDER
from .analyzer import errorSearch, usageSearch, usagelog, errorlog, usageRate, errorRate
from .forms import LoginForm, RegistrationForm, UploadForm
from .models import User
from .utils import findUserFiles, file_save_seq


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
    print("upload")
    return render_template('upload.html',
                           form=form,
                           title='Upload')
"""@app.route('/upload_file', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        if 'new_file' not in request.files:
            flash('No file part')
            return redirect(url_for('upload'))
        f = request.files['new_file']
        return file_save_seq(f)
    return"""

@app.route('/upload_file', methods=['GET', 'POST'])
@login_required
def upload_file():
    print("at upload_file")
    f = request.files
    print("got file")
    if request.method == 'POST':
        if len(f) == 0:
            print("no files")
            flash('No file part')
            return redirect(url_for('upload'))
        return file_save_seq(f['zip'])
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

    return render_template('errorcase.html',
                           title='Error Case',
                           files=fileArray)  # stats=statistics


@app.route('/graphs_err', methods=['GET', 'POST'])
def graphs_error():
    if request.args['filename'] == 'Choose a file':
        return ''
    start = request.args['start']
    end = request.args['end']
    term = request.args['term']
    filename = path.join(app.root_path, UPLOAD_FOLDER, str(current_user.id), request.args['filename'])
    # src/--.py functions should be called here to return matplot html
    if not path.exists(path.join(app.root_path, ANALYZED_CSV_FOLDER, str(current_user.id))):
        makedirs(path.join(app.root_path, ANALYZED_CSV_FOLDER, str(current_user.id)))
    loginfo = errorlog(filename, path.join(app.root_path, ANALYZED_CSV_FOLDER, str(current_user.id),
                                           request.args['filename'].rsplit('.', 1)[0] + "_errorlog.csv"))
    log = loginfo[1]
    if start != '' and end != '':
        s = parser.parse(start, parserinfo=None, default=datetime.datetime(loginfo[2].year, 1, 1))
        e = parser.parse(end, parserinfo=None, default=datetime.datetime(loginfo[3].year, 12, 31))
    else:
        s = loginfo[2]
        e = loginfo[3]
    print(s)
    print(e)
    dictionary = sorted(errorSearch(log, path.join(app.root_path, ANALYZED_CSV_FOLDER, str(current_user.id),
                                                   request.args['filename'].rsplit('.', 1)[0] + "_searchlog.csv"), s, e,
                                    term)[0].items())
    print(dictionary)
    errors = list()
    counts = list()
    for key, val in dictionary:
        errors.append(key)
        counts.append(val)
    plt.close()
    x = range(len(errors))
    plt.bar(x, counts, width=0.4)
    plt.xticks(x, errors)
    plt.grid(True, alpha=0.3)
    for i in range(len(x)):
        if counts[i] != 0:
            plt.text(x[i] - .05, counts[i] + .7, s=counts[i], fontsize=14)

    fig = plt.gcf()
    fig.set_figheight(5)
    fig.set_figwidth(12)
    stats = '<table class="table table-striped">'
    with open(path.join(app.root_path, ANALYZED_CSV_FOLDER, str(current_user.id),
                        request.args['filename'].rsplit('.', 1)[0] + "_errorlog.csv"), mode='r',
              encoding="utf-8") as csv:
        headers = csv.readline().split(',')
        stats += '<thead><tr><th>#</th><th>{}</th><th>{}</th><th>{}</th></tr></thead><tbody>'.format(
            headers[1], headers[2] + headers[3], headers[4])
        contents = csv.readlines()
        l = 1
        for line in contents:
            tokens = line.split(',', 4)
            stats += '<tr><th scope="row">{}</th><td>{}</td><td>{}</td><td>{}</td></tr>'.format(
                l, tokens[1], tokens[2] + ' ' + tokens[3], tokens[4].replace('"', ''))
            l += 1
        stats += '</tbody></table>'
    summarized = '<table class="table table-striped"><tr scope="row"><th>Error Cases</th><th>Count</th></tr>'
    for e in range(0, len(errors)):
        summarized += '<tr scope="row"><td>' + errors[e] + '</td>' + '<td>' + str(counts[e]) + '</td></tr>'
    summarized += '</table>'
    html = '<div class="container container-fluid"><div class="row justify-content-center"' \
           + mpld3.fig_to_html(fig, template_type='simple') + '</div><div class="row justify-content-center">' \
           + summarized + '</div><div class="row justify-content-center"><details title="Detailed Statistics">' \
           + stats + '</details>' + '</div></div>'

    return html


@app.route('/graphs_use', methods=['GET', 'POST'])
def graphs_usage():
    if request.args['filename'] == 'Choose a file':
        return ''
    start = request.args['start']
    end = request.args['end']
    term = request.args['term']
    filename = path.join(app.root_path, UPLOAD_FOLDER, str(current_user.id), request.args['filename'])
    # src/--.py functions should be called here to return matplot html
    if not path.exists(path.join(app.root_path, ANALYZED_CSV_FOLDER, str(current_user.id))):
        makedirs(path.join(app.root_path, ANALYZED_CSV_FOLDER, str(current_user.id)))
    loginfo = usagelog(filename, path.join(app.root_path, ANALYZED_CSV_FOLDER, str(current_user.id),
                                           request.args['filename'].rsplit('.', 1)[0] + "_usagelog.csv"))
    log = loginfo[1]
    if start != '' and end != '':
        s = parser.parse(start, parserinfo=None, default=datetime.datetime(loginfo[2].year, 1, 1))
        e = parser.parse(end, parserinfo=None, default=datetime.datetime(loginfo[3].year, 12, 31))
    else:
        s = loginfo[2]
        e = loginfo[3]
    print(s)
    print(e)
    dictionary = sorted(usageSearch(log, path.join(app.root_path, ANALYZED_CSV_FOLDER, str(current_user.id),
                                                   request.args['filename'].rsplit('.', 1)[0] + "_searchlog.csv"), s, e,
                                    term)[0].items())
    print(dictionary)
    entries = list()
    counts = list()
    for key, val in dictionary:
        entries.append(key)
        counts.append(val)
    plt.close()
    x = range(len(entries))
    plt.bar(x, counts, width=0.3)
    plt.xticks(x, entries)
    plt.grid(True, alpha=0.3)
    for i in range(len(x)):
        if counts[i] != 0:
            plt.text(x[i] - .05, counts[i] + .7, s=counts[i], fontsize=14)

    fig = plt.gcf()
    fig.set_figheight(5)
    fig.set_figwidth(8)

    stats = '<table class="table table-striped">'
    with open(path.join(app.root_path, ANALYZED_CSV_FOLDER, str(current_user.id),
                        request.args['filename'].rsplit('.', 1)[0] + "_usagelog.csv"), 'r') as csv:
        headers = csv.readline().split(',')
        stats += '<thead><tr><th>#</th><th>{}</th><th>{}</th><th>{}</th></tr></thead><tbody>'.format(
            headers[1], headers[2] + headers[3], headers[4])
        contents = csv.readlines()
        l = 1
        for line in contents:
            tokens = line.split(',', 4)
            stats += '<tr><th scope="row">{}</th><td>{}</td><td>{}</td><td>{}</td></tr>'.format(
                l, tokens[1], tokens[2] + ' ' + tokens[3], tokens[4])
            l += 1
        stats += '</tbody></table>'
    summarized = '<table class="table table-striped"><tr scope="row"><th>Usage Cases</th><th>Count</th></tr>'
    for e in range(0, len(entries)):
        summarized += '<tr scope="row"><td>' + entries[e] + '</td>' + '<td>' + str(counts[e]) + '</td></tr>'
    summarized += '</table>'
    html = '<div class="container container-fluid"><div class="row justify-content-center"' \
           + mpld3.fig_to_html(fig, template_type='simple') + '</div><div class="row justify-content-center">' \
           + summarized + '</div><div class="row justify-content-center"><details title="Detailed Statistics">' \
           + stats + '</details>' + '</div></div>'

    return html


@app.route('/rate_use', methods=['GET', 'POST'])
def rate_usage():
    if request.args['filename'] == 'Choose a file':
        return ''
    start = request.args['start']
    end = request.args['end']
    term = request.args['term']
    filename = path.join(app.root_path, UPLOAD_FOLDER, str(current_user.id), request.args['filename'])
    # src/--.py functions should be called here to return matplot html
    if not path.exists(path.join(app.root_path, ANALYZED_CSV_FOLDER, str(current_user.id))):
        makedirs(path.join(app.root_path, ANALYZED_CSV_FOLDER, str(current_user.id)))
    loginfo = usagelog(filename, path.join(app.root_path, ANALYZED_CSV_FOLDER, str(current_user.id),
                                           request.args['filename'].rsplit('.', 1)[0] + "_usagelog.csv"))
    log = loginfo[1]
    if start != '' and end != '':
        s = parser.parse(start, parserinfo=None, default=datetime.datetime(loginfo[2].year, 1, 1))
        e = parser.parse(end, parserinfo=None, default=datetime.datetime(loginfo[3].year, 12, 31))
    else:
        s = loginfo[2]
        e = loginfo[3]
    print(s)
    print(e)
    rateInfo = usageRate(log, path.join(app.root_path, ANALYZED_CSV_FOLDER, str(current_user.id),
                                        request.args['filename'].rsplit('.', 1)[0] + "_usageRate.csv"), s, e, term)
    print(rateInfo)
    dictionary = rateInfo[0]
    x = list(range(len(dictionary)))
    y = list(dictionary.values())
    plt.close()

    fig, ax = plt.subplots()
    ax.grid(True, alpha=0.3)

    plt.title("Usage Cases per hour", fontsize=24)
    plt.xlabel("Time", fontsize=18)
    plt.ylabel("Usage Cases", fontsize=18)

    points = ax.plot(x, y, 'o', markersize=10 ,mec='k', mew=1, alpha=.6)
    plt.xticks(x, dictionary.keys())
    # plt.xticks([i * 4 for i in range(int(len(dictionary) / 4))],
    #            [str(datetime.datetime.combine(rateInfo[2], datetime.time(4 * i)).strftime("%b %d %H:00")) \
    #             for i in range(int(len(dictionary) / 4))])
    fig.set_figheight(5)
    fig.set_figwidth(9)
    ax.set_ylim(ymin=0)
    fig.tight_layout()

    mpld3.plugins.connect(fig, mpld3.plugins.PointLabelTooltip(points[0], [str("({}, {})".format(key, val)) for key, val in dictionary.items()]))

    summarized = '<table class="table table-striped"><tr scope="row"><th>Usage Count by Hour</th><th>Count</th></tr>'
    for e in x:
        summarized += '<tr scope="row"><td>' + list(dictionary.keys())[e] + '</td>' + '<td>' + str(y[e]) + '</td></tr>'
    summarized += '</table>'
    html = '<div class="container container-fluid"><div class="row justify-content-center"' \
           + mpld3.fig_to_html(fig) + '</div><div class="row justify-content-center">' \
           + summarized + '</div></div>'

    return html


@app.route('/rate_err', methods=['GET', 'POST'])
def rate_error():
    if request.args['filename'] == 'Choose a file':
        return ''
    start = request.args['start']
    end = request.args['end']
    term = request.args['term']
    filename = path.join(app.root_path, UPLOAD_FOLDER, str(current_user.id), request.args['filename'])
    # src/--.py functions should be called here to return matplot html
    if not path.exists(path.join(app.root_path, ANALYZED_CSV_FOLDER, str(current_user.id))):
        makedirs(path.join(app.root_path, ANALYZED_CSV_FOLDER, str(current_user.id)))
    loginfo = errorlog(filename, path.join(app.root_path, ANALYZED_CSV_FOLDER, str(current_user.id),
                                           request.args['filename'].rsplit('.', 1)[0] + "_errorlog.csv"))
    log = loginfo[1]
    if start != '' and end != '':
        s = parser.parse(start, parserinfo=None, default=datetime.datetime(loginfo[2].year, 1, 1))
        e = parser.parse(end, parserinfo=None, default=datetime.datetime(loginfo[3].year, 12, 31))
    else:
        s = loginfo[2]
        e = loginfo[3]
    print(s)
    print(e)
    rateInfo = errorRate(log, path.join(app.root_path, ANALYZED_CSV_FOLDER, str(current_user.id),
                                        request.args['filename'].rsplit('.', 1)[0] + "_errorRate.csv"), s, e, term)
    print(rateInfo)
    dictionary = rateInfo[0]
    x = list(range(len(dictionary)))
    y = list(dictionary.values())
    plt.close()

    fig, ax = plt.subplots()
    ax.grid(True, alpha=0.3)
    plt.title("Errors per hour", fontsize=24)
    plt.xlabel("Time", fontsize=18)
    plt.ylabel("Errors", fontsize=18)
    points = ax.plot(x, y, 'o', markersize=10 ,mec='k', mew=1, alpha=.6)
    plt.xticks([i * 4 for i in range(int(len(dictionary) / 4))], [list(dictionary.keys())[i * 4] for i in range(int(len(dictionary) / 4))])
    # [str(datetime.datetime.combine(rateInfo[2], datetime.time(4 * i)).strftime("%b %d %H:00")) for i in range(int(len(dictionary) / 4))]
    fig.set_figheight(5)
    fig.set_figwidth(9)
    ax.set_ylim(ymin=0)
    fig.tight_layout()

    mpld3.plugins.connect(fig, mpld3.plugins.PointLabelTooltip(points[0], [str("({}, {})".format(key, val)) for key, val in dictionary.items()]))

    summarized = '<table class="table table-striped"><tr scope="row"><th>Error Count by Hour</th><th>Count</th></tr>'
    for e in x:
        summarized += '<tr scope="row"><td>' + list(dictionary.keys())[e] + '</td>' + '<td>' + str(y[e]) + '</td></tr>'
    summarized += '</table>'
    html = '<div class="container container-fluid"><div class="row justify-content-center"' \
           + mpld3.fig_to_html(fig) + '</div><div class="row justify-content-center">' \
           + summarized + '</div></div>'

    return html


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
