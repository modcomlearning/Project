#  Flask uses HTML/JS/CSS/Python/Jinja2
from flask import Flask
app = Flask(__name__)  # flask object takes the the name of the application

# Routing
@app.route('/home')
def home():
    return 'My First flask application'


if __name__ == '__main__':
    app.run()

