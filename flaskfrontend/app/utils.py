from flask import flash, url_for, redirect
from werkzeug.utils import secure_filename
from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from app import app, models, db
from os import path, remove, makedirs, rename
from flask_login import current_user
import hashlib
import csv
from re import *


def allowed_file(filename):
    ret = True
    if '.' not in filename:
        flash('Upload unsuccessful: File must have an extension')
        ret = ret and False
    if len(filename) > 128:
        flash('Upload unsuccessful: Filename must be less than 128 characters')
        ret = ret and False
    if filename.rsplit('.', 1)[1].lower() not in ALLOWED_EXTENSIONS:
        flash('Upload unsuccessful: Filetype not allowed')
        ret = ret and False
    return ret


def file_save_seq(f):
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
        hash = hasher.hexdigest()

        log_hash = models.Log.query.filter_by(file_hash=hash, user_id=current_user.id).first()
        if log_hash is not None:
            remove(tmp_path)
            flash('Upload unsuccessful: file already exist')
            return redirect(url_for('upload'))
        f_name = secure_filename(f.filename)
        i_f_name = f_name.rsplit('.', 1)[0] + '_'
        i = 0
        dest_path = path.join(app.root_path, UPLOAD_FOLDER, str(current_user.id))
        if not path.exists(dest_path):
            makedirs(dest_path)
        while path.isfile(path.join(app.root_path, UPLOAD_FOLDER, str(current_user.id),
                                    i_f_name + str(current_user.id) + "_" + str(i) + '.' + f_name.rsplit('.', 1)[1])):
            i += 1
        i_f_name = i_f_name + str(current_user.id) + "_" + str(i) + '.' + f_name.rsplit('.', 1)[1]

        new_log = models.Log(owner=current_user)
        new_log.file_hash = hash
        new_log.filename = f_name
        new_log.internal_f_name = i_f_name
        db.session.add(new_log)
        db.session.commit()

        rename(tmp_path, path.join(dest_path, i_f_name))
        flash('File uploaded: ' + f_name)
        return redirect(url_for('index'))
    return redirect(url_for('upload'))


def findUserFiles(target_user):
    import os
    from config import UPLOAD_FOLDER
    fileArray = []
    userFolder = os.path.join(app.root_path, UPLOAD_FOLDER, str(target_user.id))
    if (os.path.exists(userFolder)):
        for filename in os.listdir(userFolder):
            if filename.endswith(".log"):
                filePath = os.path.abspath(userFolder + "/" + filename)
                fileArray.append({'filename': filename})  # .replace('_' + str(current_user.id),'')
    return fileArray


def errorPieChart(fin, fout):
    dictionary = errorlog(fin, fout)
    return dictionary


def errorlog(fin, fout):
    word_code = '[38866]: '
    count = 0
    error_dict = {}
    with open(fout, 'w') as csvfile:
        writer = csv.writer(csvfile, lineterminator='\n', delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['type', 'error', 'date', 'time', 'details'])

        # open a syslog file to read from
        with open(fin, 'r') as in_file:

            # ------------ Errors --------------------
            # ----------------------------------------
            # ----------------------------------------
            # fail  <---- nothing in the logs
            # unauthorized <---- httpclienterror
            # refused <---- nothing in the logs
            # NoSuchPageException <---- nothing in the logs
            # 500 <---- nothing in the logs

            # -------------- Client Errors --------------
            for line in in_file:
                if search('HttpClientError', line):
                    end_index = line.index(word_code) + len(word_code)
                    error_type = 'Error'
                    error_name = 'Http Client Error'
                    error_detail = line[end_index:].rstrip()
                    error_date = search('\w{3}\s\d{1,2}', line).group(0)
                    error_time = search('\d{2}:\d{2}:\d{2}', line).group(0)

                    writer.writerow([error_type, error_name, error_date, error_time, error_detail])
                    count += 1
            error_dict['HttpClientError'] = count
            in_file.seek(0)

            # -------------- Access Denied --------------
            for line in in_file:
                if search('AccessDenied', line):

                    if search('AuditListener', line):
                        this_word_code = 'AuditListener     :'
                        end_index = line.index(this_word_code) + len(this_word_code)
                    else:
                        end_index = line.index(word_code) + len(word_code)
                    error_type = 'Error'
                    error_name = 'Access Denied'
                    error_detail = line[end_index:].rstrip()
                    if search('1 --- ', error_detail):
                        end_index = error_detail.index('1 --- ') + len('1 --- ')
                        error_detail = error_detail[end_index:].rstrip()
                    error_date = search('\w{3}\s\d{1,2}', line).group(0)
                    error_time = search('\d{2}:\d{2}:\d{2}', line).group(0)

                    writer.writerow([error_type, error_name, error_date, error_time, error_detail])
                    count += 1
            error_dict['AccessDenied'] = count
            count = 0

            in_file.seek(0)

            # -------------- Runtime Exception --------------
            for line in in_file:
                if search('RuntimeException', line):
                    end_index = line.index(word_code) + len(word_code)
                    error_type = 'Error'
                    error_name = 'Runtime Exception'
                    error_detail = line[end_index:].rstrip()
                    error_date = search('\w{3}\s\d{1,2}', line).group(0)
                    error_time = search('\d{2}:\d{2}:\d{2}', line).group(0)

                    writer.writerow([error_type, error_name, error_date, error_time, error_detail])
                    count += 1
            error_dict['RuntimeException'] = count
            count = 0
            in_file.seek(0)

            # -------------- Transport Error --------------
            for line in in_file:
                if search('transport error', line):

                    end_index = line.index(word_code) + len(word_code)
                    error_type = 'Error'
                    error_name = 'Transport Error'
                    error_detail = line[end_index:].rstrip()
                    if search('1 --- ', error_detail):
                        end_index = error_detail.index('1 --- ') + len('1 --- ')
                        error_detail_start = error_detail.index('sockJsScheduler')
                        error_detail = error_detail[end_index:53] + " - " + error_detail[error_detail_start:]
                    error_date = search('\w{3}\s\d{1,2}', line).group(0)
                    error_time = search('\d{2}:\d{2}:\d{2}', line).group(0)

                    writer.writerow([error_type, error_name, error_date, error_time, error_detail])
                    count += 1
            error_dict['transport error'] = count
            count = 0
            in_file.seek(0)

            # -------------- Default Response Handler Error --------------
            for line in in_file:
                if search('DefaultResponseErrorHandler', line):
                    end_index = line.index(word_code) + len(word_code)
                    error_type = 'Error'
                    error_name = 'Default Response Error Handler'
                    error_detail = line[end_index:].rstrip()
                    error_date = search('\w{3}\s\d{1,2}', line).group(0)
                    error_time = search('\d{2}:\d{2}:\d{2}', line).group(0)

                    writer.writerow([error_type, error_name, error_date, error_time, error_detail])
                    count += 1
            error_dict['DefaultResponseErrorHandler'] = count
            count = 0
            in_file.seek(0)

            # -------------- WARN --------------
            for line in in_file:
                if search('WARN', line):

                    this_word_code = 'WARN '
                    end_index = line.index(this_word_code) + len(this_word_code)
                    error_type = 'Error'
                    error_name = 'Warning'
                    error_detail = line[end_index:].rstrip()
                    if match('1 --- ', error_detail):
                        error_detail = error_detail[5:].rstrip()
                    error_date = search('\w{3}\s\d{1,2}', line).group(0)
                    error_time = search('\d{2}:\d{2}:\d{2}', line).group(0)

                    writer.writerow([error_type, error_name, error_date, error_time, error_detail])
                    count += 1
            error_dict['WARN'] = count
            count = 0
            in_file.seek(0)

            # -------------- Timeout --------------
            for line in in_file:
                if search('timeout', line):
                    end_index = line.index(word_code) + len(word_code)
                    error_type = 'Error'
                    error_name = 'Timeout'
                    error_detail = line[end_index:].rstrip()
                    error_date = search('\w{3}\s\d{1,2}', line).group(0)
                    error_time = search('\d{2}:\d{2}:\d{2}', line).group(0)

                    writer.writerow([error_type, error_name, error_date, error_time, error_detail])
                    count += 1
            error_dict['timeout'] = count
            count = 0
            in_file.seek(0)
    return error_dict


'''
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
'''

'''
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()

    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        form.file.data.save('uploads/' + filename)
        return redirect(url_for('index'))

    return render_template('index.html', form=form)


from logMetrics import errorPieChart, usagePieChart, errorRate
'''

'''
@app.route('/graph')
def show_graph():
    errpie = errorPieChart({{url_for('static', filename='syslog3.log')}},
                           {{url_for('static', filename='errorlog.csv')}})
    usepie = usagePieChart({{url_for('static', filename='syslog3.log')}},
                           {{url_for('static', filename='usagelog.csv')}})
    errrate = errorRate({{url_for('static', filename='errorlog.csv')}})
    return render_template('graph.html', epie=errpie, upie=usepie, err=errrate)
'''
