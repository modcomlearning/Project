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



from flask import request
@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        pass


    else:
        return render_template('signup.html')


# xampp
if __name__ == '__main__':
    app.debug = True
    app.run()


