from flask import flash
from config import ALLOWED_EXTENSIONS


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
