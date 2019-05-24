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

    this_dir = os.path.dirname(__file__)
    home_file = app.config['HOME_PAGE_FOLDER'] + 'homepage.html'
    try:
        homepage = open(os.path.join(this_dir, home_file), "r").read()
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
    this_dir = os.path.dirname(__file__)
    home_file = app.config['HOME_PAGE_FOLDER'] + 'homepage.html'
    value = ""
    if request.form.get("newHome"):
        value = request.form.get("newHome")

    # if not os.path.isdir(app.config['HOME_PAGE_FOLDER']):
    #     os.mkdir(app.config['HOME_PAGE_FOLDER'])

    homeFile= open(os.path.join(this_dir, home_file), "w+")
    homeFile.write(value)
    homeFile.flush()

    files = request.files.getlist("Attachments")

    for file in files:
        print(file.filename, file=sys.stdout)
        nameFile = secure_filename(file.filename)
        file.save(os.path.join(this_dir, app.config['HOME_PAGE_FOLDER'], nameFile))

    return jsonify(result=True)