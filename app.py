from flask import Flask, url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from database.model import User, db
from flask_session import Session
from flask import jsonify
from discord import DiscordChat
# from flask_httpauth import HTTPBasicAuth
# auth = HTTPBasicAuth()


app = Flask(__name__)
app.secret_key =  b'\x031\xa0\xb4\xd0\xb6aB\xf6\xc7\xb2\xd4Y\xb7\xce\xc1'
app.config['SESSION_TYPE'] = 'redis'
app.debug = True 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:yourpass@localhost/discord_chat'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
# db = SQLAlchemy(app)
db.init_app(app)
Session(app)


@app.route('/', methods=['GET'])
def index():
    if session.get('logged_in'):
        return render_template('home.html')
    else:
        return render_template('index.html', message="Hello!")


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            User(username=request.form['username'], password=request.form['password']).save()
            return redirect(url_for('login'))
        except:
            return render_template('index.html', message="User Already Exists")
    else:
        return render_template('register.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        try:
            u = request.form['username']
            p = request.form['password']
            data = User.query.filter_by(username=u, password=p).first()
            if data is not None:
                print(session)
                session['logged_in'] = data.id
                return redirect(url_for('index'))
        except Exception:
            pass
        return render_template('index.html', message="Incorrect Details")



@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))


@app.route('/chat', methods=['POST', 'GET'])
def chat():
    if not session.get('logged_in'):
        return render_template('index.html', message="Hello!")
    if request.method == 'POST':
        reply_chat = DiscordChat().chat(request)
        return {'data': reply_chat}
    return {'error': 'only post request accepted'}


if(__name__ == '__main__'):
    # db.metadata.create_all(db.engine)
    app.run()
