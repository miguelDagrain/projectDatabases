from App.base import *
from DataAccess.employeeAccess import EmployeeAccess


def login_required(role="ANY"):
    """
    Overrides the default login manager of Flask-Login to support roles.
    https://stackoverflow.com/questions/15871391/implementing-flask-login-with-multiple-user-classes
    :param role: role of the user that logged in
    :return: function wrapper
    """

    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            if (role not in current_user.roles) and (role != "ANY"):
                return login_manager.unauthorized()
            return fn(*args, **kwargs)

        return decorated_view

    return wrapper


@babel.localeselector
def get_locale():
    """
    If the language cookie is set, use its value
    Else determine the language that fits best based on the user's accept header
    :return: Language code
    """
    lang = request.cookies.get('lang')
    if lang is not None:
        return lang
    else:
        lang = request.accept_languages.best_match(config_data['supported_langs'])
        return lang


@app.route('/download/<string:name>', methods=['GET'])
def download(name):
    """
    Creates the possibility to download stored files.
    :param name: Name of the file to download
    :return: file
    """
    return send_from_directory(directory=app.config['UPLOAD_FOLDER'], filename=name, as_attachment=True)


@app.route('/download_homepage/<string:name>', methods=['GET'])
def download_homepage(name):
    '''
    Download the files from the homepage
    :param name: File to download
    :return: file
    '''
    return send_from_directory(directory=app.config['HOME_PAGE_FOLDER'], filename=name, as_attachment=True)


@app.errorhandler(404)
def handle_404(e):
    """
    Handles error 404 (missing page)
    :param e: Exception container
    :return: Rendered template of the 404.html file
    """
    return render_template("404.html"), 404


@app.route("/lang/", methods=["GET"])
def pick_language():
    """
    Sets the selected language and reload current page.
    :return: response that redirects to the current page and sets the language cookie
    """
    lang = request.args.get('send')
    url = request.args.get('url_redirect')
    resp = make_response(redirect(url))
    resp.set_cookie('lang', lang)
    return resp


@app.route("/check/empl_names", methods=["GET"])
def check_empl_names():
    """
    Used to create suggestions for employee names
    :return: Suggestions for employee names
    """
    from DataAccess.employeeAccess import EmployeeAccess
    Eaccess = EmployeeAccess()
    employees = Eaccess.get_employees()

    given_letters = request.args.get("letters")

    possibilities = list()

    for empl in employees:
        if given_letters in empl.name:
            possibilities.append(empl.name)
            if len(possibilities) > 4:
                break

    return jsonify(possibilities)


@app.route("/check/empl_name_correct", methods=["GET"])
def check_empl_name_correct():
    """
    Checks if an employee name is correct.
    :return: True if correct, else false (jsonified)
    """
    Eaccess = EmployeeAccess()
    employees = Eaccess.get_employees()

    given_name = request.args.get('input')

    for empl in employees:
        if given_name == empl.name:
            return jsonify(True)

    return jsonify(False)


@app.route("/check/project_titles", methods=["GET"])
def check_project_titles():
    """
    Used to create suggestions for project titles
    :return: Suggestions for project titles
    """
    from DataAccess.projectAccess import ProjectAccess
    Paccess = ProjectAccess()
    projects = Paccess.get_projects()

    given_letters = request.args.get('letters')

    possibilities = list()

    for proj in projects:
        if given_letters in proj.title:
            possibilities.append(proj.title)
            if len(possibilities) > 4:
                break

    return jsonify(possibilities)


@app.route("/check/project_title_correct", methods=["GET"])
def check_project_title_correct():
    """
    Checks if a project title is correct
    :return: True if correct, else false (jsonified)
    """
    from DataAccess.projectAccess import ProjectAccess
    Paccess = ProjectAccess()
    projects = Paccess.get_projects()

    given_title = request.args.get('input')

    for proj in projects:
        if given_title == proj.title:
            return jsonify(True)

    return jsonify(False)


@login_manager.user_loader
def load_user(user_id):
    """
    Loads a user
    :param user_id: id of the user
    :return: the loaded user
    """
    from DataAccess.employeeAccess import EmployeeAccess
    eors = EORS.UNKNOWN
    if user_id[0] == "S":
        from DataAccess.sessionAccess import SessionAccess
        sa = SessionAccess()
        se = sa.get_SessionOnId(user_id[1:])
        us = User(se)

        # eors = EORS.STUDENT
        # us = User(Session(0, user_id[1:], 0, eors))
    elif user_id[0] == "E":
        eors = EORS.EMPLOYEE
        us = User(Session(0, user_id[1:], 0, eors))

    eAcces = EmployeeAccess()
    us.roles = list()
    if user_id != 'None' and us.session.EORS == EORS.EMPLOYEE:
        us.roles = eAcces.get_employeeRoles(user_id[1:])
        us.roles.append("employee")
    elif user_id != 'None' and us.session.EORS == EORS.STUDENT:
        us.roles.append('student')
    us.auth = True
    us.active = True
    return us


@login_manager.unauthorized_handler
def unauthorized():
    """
    Redirect to home page if an unauthorized user tries to visit a page he can not see.
    :return: redirection to home page
    """
    return redirect(url_for('home', err="login_required"))


@app.route('/login/', methods=['POST'])
def login():
    """
    Logs a user in.
    :return: True if user is logged in correctly, else false
    """
    from DataAccess.sessionAccess import SessionAccess
    sa = SessionAccess()
    us = User(Session(None, 1, sa.get_CurentSQLTime(), EORS.UNKNOWN))
    username = request.form["username"]
    password = request.form["password"]
    try:
        if us.login(username, password):
            if us.session.EORS == EORS.STUDENT:
                sa.add_Session(us.session)
            login_user(us)
            temp = current_user
            flash('Logged in successfully.')
            flash("you are now logged in")
            return "true"
        else:
            raise Exception('unable to log in, did you type your ussername or password correctly?')
    except:
        print("authentication error")
        return "false"


@app.route("/logout/", methods=['GET', 'POST'])
def logout():
    """
    Logs the user out.
    :return: redirection to home page
    """
    if current_user.session.EORS == EORS.STUDENT:
        from DataAccess.sessionAccess import SessionAccess
        us = current_user
        sa = SessionAccess()
        sa.add_Session(us.session)
    logout_user()
    next = request.args.get('logout')
    flash("you are now logged out")
    return redirect(next or url_for('index'))


@app.route('/upload/')
def upload():
    """
    Create template to upload files
    :return: rendered template of uploader.html
    """
    return render_template('uploader.html')


def allowed_file(filename):
    """
    Determine if file extension is allowed
    :param filename: filename
    :return: true if the extension is allowed
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    """
    Upload a file
    :return: redirection to url
    """
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if not os.path.exists(app.config['UPLOAD_FOLDER'] + "test/"):
                os.mkdir(app.config['UPLOAD_FOLDER'] + "test/")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], "test/" + filename))
    return 'file uploaded successfully'