from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from paintings import get_paintings
from flask import make_response


app = Flask(__name__)
app.config['SECRET_KEY'] = 'python'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite'
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), nullable=False)
    username = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(40), nullable=False)

    def __str__(self):
        return f'E-mail:{self.Email}; username: {self.Username}; password: {self.Password}'

db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/user')
def user():
    return render_template('user.html', paintings=get_paintings())

@app.route('/about')
def about():
    return render_template('about.html')




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = Users.query.filter_by(username=username).first()

        if user:
            if user.username == username and user.password == password:
                session['username'] = username
                return redirect(url_for('user'))
            else:
                flash('Incorrect credential')
                return redirect(url_for('login'))
        else:
            flash("user doesn't exist!")
            return redirect(url_for('login'))



    elif request.method == "GET":
        if 'username' in request.args:
            username = request.args['username']
            return redirect(url_for('user'))
        return render_template('login.html')




@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method=="POST":

        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        if username=='' or email=='' or password=='': flash("All fields are required!", "error")
        else:
            user1 = Users(email=email, username=username, password=password)
            db.session.add(user1)
            db.session.commit()
            flash("The account was created successfully ", "info")


    return render_template('registration.html')


@app.route('/video')
def video():
    my_resp = make_response('Response!')
    my_resp.headers['warning'] = 'Warning'
    my_resp.status_code = 7564
    # my_resp.mimetype = 'video/ogg'
    return my_resp

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You are logged out!')
    return redirect(url_for('home'))

@app.errorhandler(404)
def pageNotFound(error):
    return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True)