from App.base import *
from App.utilities import get_locale


@app.route("/")
def index():
    """
    Redirect to home page on url /
    :return: redirection to 'home' url
    """
    return redirect(url_for("home"))


@app.route("/home/")
def home():
    """
    Renders the index template
    :return: Rendered index template
    """
    try:
        homepage = open(app.config['HOME_PAGE_FOLDER'] + 'homepage.html', "r").read()
    # Store configuration file values
    except FileNotFoundError:
        homepage = ''
    # Keep preset values

    resp = make_response(render_template("home.html", page="index",
                                         homedoc=homepage, err=request.args.get('err', default=None)))
    if request.cookies.get('lang') is None:
        lang = get_locale()
        resp.set_cookie('lang', lang)
    return resp


@app.route("/home/", methods=["POST"])
def modify_homepage():
    """
    Function to modify the homepage
    """
    value = ""
    if request.form.get("newHome"):
        value = request.form.get("newHome")

    if not os.path.isdir(app.config['HOME_PAGE_FOLDER']):
        os.mkdir(app.config['HOME_PAGE_FOLDER'])

    homeFile= open(app.config['HOME_PAGE_FOLDER']+'homepage.html', "w+")
    homeFile.write(value)
    homeFile.seek(0)
    homeFile.flush()
    homeFile.close()

    files = request.files.getlist("Attachments")

    for file in files:
        print(file.filename, file=sys.stdout)
        nameFile = secure_filename(file.filename)
        file.save(os.path.join(app.config['HOME_PAGE_FOLDER'], nameFile))

    return jsonify(result=True)