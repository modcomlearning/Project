#  Flask uses HTML/JS/CSS/Python/Jinja2
from flask import Flask, render_template, session
from flask import request
import pymysql
from pandas.io import sql

app = Flask(__name__)  # flask object takes the the name of the application

# create a secret key used in encrypting the sessions
app.secret_key = "Wdg@#$%89jMfh2879mT"
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

        if cursor.rowcount == 1:
            # take me to a different route and create a session
            session['key'] = email
            from flask import redirect
            #after successfull login, we create user session and redirect the user to /checkout
            return redirect('/checkout')

        else:
            return render_template('login.html', msg="Login Failed")

    else:
        return render_template('login.html')

# install python, pycharm, xampp
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



# This routes reads products based on id
@app.route('/purchase/<id>')
def purchase(id):
    conn = pymysql.connect("localhost", "root", "", "soko_db")
    cursor = conn.cursor()
    # execute the query using the cursor
    cursor.execute("select * from products where product_id = %s", (id))
    # check if no records were found
    if cursor.rowcount < 1:
        return render_template('purchase.html', msg="This Product does not exist")
    else:
        # return all rows found
        rows = cursor.fetchall()
        return render_template('purchase.html', rows=rows)



# this route, users will need to login to access it
@app.route('/checkout')
def checkout():
    if 'key' in session:
        logged_in = session['key']
        return render_template('checkout.html')

    else:
        from flask import redirect
        return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('key',None)
    from flask import redirect
    return redirect('/login')





# build a simple cart with sqlite
import sqlite3
con = sqlite3.connect('cart.db')
con.execute('create table if not exists items(id INT, name TEXT, cost INT, qtty INT, total INT)')
@app.route('/cart', methods=['POST','GET'])
def cart():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        cost = float(request.form['cost'])
        qtty = float(request.form['name'])
        total  = cost * qtty

















# xampp
if __name__ == '__main__':
    app.debug = True
    app.run()


