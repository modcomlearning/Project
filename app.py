#  Flask uses HTML/JS/CSS/Python/Jinja2
from flask import Flask, render_template
from flask import request
import pymysql
app = Flask(__name__)  # flask object takes the the name of the application

# Routing
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        # # hash the password/ strength
        # # we first connect to localhost and soko_db
        conn = pymysql.connect("localhost", "root", "", "soko_db")

        # insert the records into the users tables
        cursor = conn.cursor()
        cursor.execute("select * from users where email = %s and password=%s", (email, password))

        if cursor.rowcount ==1:
            # take me to a different route and create a session
            return render_template('login.html', msg="Login Succesfully")

        else:
            return render_template('login.html', msg="Login Failed")

    else:
        return render_template('login.html')


@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == "POST":

        email = request.form['email']
        password = request.form['password']

        # hash the password
        # we first connect to localhost and soko_db
        conn = pymysql.connect("localhost","root","","soko_db")

        # insert the records into the users tables
        cursor =  conn.cursor()
        cursor.execute("insert into users(email,password) values (%s,%s)", (email,password))
        conn.commit()
        return render_template('signup.html', msg= "Record Saved Succesfully")

    else:
        return render_template('signup.html')


@app.route('/products')
def products():
    # Connect to database
    conn = pymysql.connect("localhost", "root", "", "soko_db")
    cursor = conn.cursor()
    # execute the query using the cursor
    cursor.execute("select * from products")
    # check if no records were found
    if cursor.rowcount < 1:
        return render_template('products.html', msg="No Products")
    else:
        # return all rows found
        rows = cursor.fetchall()
        return render_template('products.html',rows=rows)








@app.route('/purchase/<id>')
def purchase(id):
    conn = pymysql.connect("localhost", "root", "", "soko_db")
    cursor = conn.cursor()
    # execute the query using the cursor
    cursor.execute("select * from products where product_id = %s", (id))
    # check if no records were found
    if cursor.rowcount < 1:
        return render_template('purchase.html', msg="No Products")
    else:
        # return all rows found
        rows = cursor.fetchall()
        return render_template('purchase.html', rows=rows)




# xampp
if __name__ == '__main__':
    app.debug = True
    app.run()


