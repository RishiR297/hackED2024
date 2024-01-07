from flask import Flask, jsonify, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy()
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

openai.api_key = os.getenv("OPENAI_API_KEY")
CORS(app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(user, user_id)

class user(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))

with app.app_context():
    db.create_all()

@app.route('/data', methods=['POST', 'GET'])
def get_data():
    if request.method == 'POST':
        data = request.get_json()
        user_input = data.get('data')
        try:
            response = openai.ChatCompletion.create(
              model="gpt-3.5-turbo",
              messages=[
                    {"role": "system", "content": "You are baymax from big hero 6 movie."},
                    {"role": "user", "content": user_input}
                ]
            )
            output = response['choices'][0]['message']['content']
            return jsonify({"response": True, "message": output})
        except Exception as e:
            print(e)
            error_message = f'Error: {str(e)}'
            return jsonify({"message": error_message, "response": False})
    else:
        # Handle GET request here
        return render_template('index.html')

@app.route('/index', methods=['POST','GET'])
def index():
    return render_template('index.html')
    
@app.route('/', methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        print("email: ", email)

        query = db.session.execute(db.select(user).where(user.email == email))
        userss = query.scalar()
        # Email doesn't exist or password incorrect.
        if not userss:
            print("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(userss.password, password):
            print('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(userss)
            return redirect(url_for('newhome'))

    return render_template("login.html", logged_in=current_user.is_authenticated)



@app.route('/signup', methods = ["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        query = db.session.execute(db.select(user).where(user.email == email))

        userss = query.scalar()
        if userss:
            print("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))
        
        hash_and_salted_password = generate_password_hash(
            request.form.get('password'),
            method='pbkdf2:sha256',
            salt_length=8)

        new_user = user(
        username=request.form.get('name'),
        email = request.form.get('email'),
        password = hash_and_salted_password,

        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('login'))

    return render_template('signup.html', logged_in=current_user.is_authenticated)

@app.route('/newhome')
def newhome():
    return render_template('newhome.html')

@app.route('/reset_password')
def reset_password():
    return render_template('reset_password.html')

@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/appointments')
def appointments():
    return render_template('appointments.html')

@app.route('/survey')
def survey():
    return render_template('survey.html')

@app.route('/secrets')
@login_required
def secrets():
    print(current_user.name)
    return render_template("secrets.html", name=current_user.name, logged_in=True)

if __name__ == '__main__':
    app.run(debug=True)