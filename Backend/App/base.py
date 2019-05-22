import datetime
import json
import re
import sys
from functools import wraps

from flask import *
from flask.templating import render_template
from flask_babel import *
from flask_login import LoginManager
from flask_login import login_user, logout_user, current_user
from werkzeug.utils import secure_filename

from dbConnection import setConnection

from Document import *
from Employee import Employee
from MailService import MailService
from Project import Project
from RelevanceCalculator import RelevanceCalculator
from ResearchGroup import ResearchGroup
from Session import *
from User import *
from config import config_data
from TagCalculator import findTag

ROOT = "../../"

app = Flask(__name__, template_folder=ROOT+"html/templates/", static_folder=ROOT+"html/static")
app_data = {'app_name': "newName"}
app.config['BABEL_TRANSLATION_DIRECTORIES'] = ROOT+"babel/translations/"
app.config['UPLOAD_FOLDER'] = ROOT+"attachments/"
app.config['HOME_PAGE_FOLDER'] ="../homepage/"
ALLOWED_EXTENSIONS = {'html', 'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
babel = Babel(app)
app.secret_key = b'&-s\xa6\xbe\x9b(g\x8a~\xcd9\x8c)\x01]\xf5\xb8F\x1d\xb2'
login_manager = LoginManager()
login_manager.init_app(app)

# setting up the database connection
ip = config_data['ip']
port = config_data['port']
setConnection(dbname=config_data['dbname'], dbuser=config_data['dbuser'], dbpass=config_data['dbpass'],
                               dbhost=config_data['dbhost'])
