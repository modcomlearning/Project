#  Flask uses HTML/JS/CSS/Python/Jinja2
from flask import Flask, render_template
from flask import request
import pymysql
app = Flask(__name__)  # flask object takes the the name of the application

# Routing
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login')
def login():
    return render_template('login.html')



@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # we first connect to localhost and soko_db
        conn = pymysql.connect("localhost","root","","soko_db")

        # insert the records into the users tables
        cursor =  conn.cursor()
        cursor.execute("insert into users(email,password) values (%s,%s)", (email,password))
        conn.commit()
        return render_template('signup.html', msg= "Record Saved Succesfully")


    else:
        return render_template('signup.html')


# xampp
if __name__ == '__main__':
    app.debug = True
    app.run()


