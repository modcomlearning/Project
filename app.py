#  Flask uses HTML/JS/CSS/Python/Jinja2
from flask import Flask, render_template
app = Flask(__name__)  # flask object takes the the name of the application

# Routing
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run()

