import flask
from flask_mail import Mail
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

DEV_DB = 'postgresql://aerousr:rumair@localhost/rumair_inventory_db'
PROD_DB = 'postgresql://efalozdnlswiuk:a81aba78488b90d9f6d846d45e04db658cd78219286f0a72a445e7cd1ff37b84@ec2-34-236-215-156.compute-1.amazonaws.com:5432/d206k08qottimm'

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = PROD_DB
app.secret_key = "rumair"

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'rumairinventoryapp@gmail.com'
app.config['MAIL_PASSWORD'] = 'TarzanAero802'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'rumairinventoryapp@gmail.com'

mail = Mail(app)

db = SQLAlchemy(app)
CORS(app)
