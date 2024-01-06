from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/providers')
def providers():
    return render_template('providers.html')

@app.route('/appointments')
def appointments():
    return render_template('appointments.html')

if __name__ == '__main__':
    app.run(debug=True)
