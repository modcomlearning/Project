#  Flask uses HTML/JS/CSS/Python/Jinja2
from flask import Flask, render_template
app = Flask(__name__)  # flask object takes the the name of the application

# Routing
@app.route('/home')
def home():
    return render_template('home.html')





if __name__ == '__main__':
    app.run()

