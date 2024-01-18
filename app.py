from flask import Flask, jsonify, render_template, request, url_for, redirect, request, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

openai.api_key = "[KEY]"
CORS(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
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
                    {"role": "system", "content": "You are baymax from big hero 6 movie but call yourself maxbay."},
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

@app.route('/viewdata', methods=['GET'])
def view_data():
    users = User.query.all()  # Retrieve all users from the database
    user_list = []
    for user in users:
        user_list.append({'username': user.username, 'email': user.email})  # Add each user's username and email to the list
    return jsonify(user_list)  # Return the list of users as JSON

@app.route('/index', methods=['POST','GET'])
def index():
    return render_template('index.html')
    
@app.route('/', methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        print("email: ", email)

        user = User.query.filter_by(email=email).first()
        # Email doesn't exist or password incorrect.
        if not user:
            print("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            print('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('newhome'))

    return render_template("login.html", logged_in=current_user.is_authenticated)

@app.route('/signup', methods = ["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            print("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            password,
            method='pbkdf2:sha256',
            salt_length=8)

        new_user = User(
        username=username,
        email=email,
        password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('login'))

    return render_template('signup.html', logged_in=current_user.is_authenticated)


app.config['UPLOAD_FOLDER'] = 'static/uploads/'

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'profile_picture' in request.files:
        file = request.files['profile_picture']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'File uploaded successfully'
    
@app.route('/newhome')
@login_required
def newhome():
    return render_template('newhome.html', user=current_user)

@app.route('/reset_password')
def reset_password():
    return render_template('reset_password.html')

@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@app.route('/contact')
@login_required
def contact():
    return render_template('contact.html')

@app.route('/appointments')
@login_required
def appointments():
    return render_template('appointments.html')

@app.route('/survey')
@login_required
def survey():
    return render_template('survey.html')

@app.route('/calendar', methods = ["GET", "POST"])
@login_required
def calendar():
    return render_template('calendar.html')

@app.route('/secrets')
@login_required
def secrets():
    print(current_user.username)
    return render_template("secrets.html", name=current_user.username, logged_in=True)

if __name__ == '__main__':
    app.run(debug=True)