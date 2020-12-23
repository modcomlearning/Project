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
            return redirect('/mycart')

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




@app.route('/logout')
def logout():
    session.pop('key',None)
    from flask import redirect
    return redirect('/login')




# build a simple cart with sqlite
from flask import redirect, url_for
import sqlite3
con = sqlite3.connect('cart.db')
con.execute('create table if not exists items(id INT, name TEXT, cost INT, qtty INT, total INT)')
@app.route('/cart', methods=['POST','GET'])
def cart():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        cost = float(request.form['cost'])
        qtty = float(request.form['qtty'])
        total  = cost * qtty

        with sqlite3.connect('cart.db') as con:
            cursor = con.cursor()
            cursor.execute("insert into items(id,name,cost,qtty,total) values(?,?,?,?,?)",
                           (id,name,cost,qtty,total))
            con.commit()

            return redirect(url_for('purchase', id=id))
    else:
        return redirect('products')



@app.route('/mycart')
def mycart():
    with sqlite3.connect('cart.db') as con:
        cursor = con.cursor()
        cursor.execute("select * from items")

        if cursor.rowcount==0:
            return render_template('mycart.html', msg = "Your Basket is Empty")
        else:
            rows = cursor.fetchall()
            # get totals
            total_sum =0
            for row in rows:
                total_sum = total_sum + row[4]

            return render_template('mycart.html', rows = rows, total_sum = total_sum)


# Clear from sqlite
@app.route('/empty')
def empty():
    with sqlite3.connect('cart.db') as con:
        cursor = con.cursor()
        cursor.execute("delete  from items")
        return redirect('/mycart')



import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth
@app.route('/mpesa_payment/<total_amount>', methods = ['POST','GET'])
def mpesa_payment(total_amount):
    if 'key' in session:
        if request.method == 'POST':
            phone = str(request.form['phone'])
            amount = str(request.form['amount'])
            #GENERATING THE ACCESS TOKEN
            consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
            consumer_secret = "amFbAoUByPV2rM5A"

            api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials" #AUTH URL
            r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

            data = r.json()
            access_token = "Bearer" + ' ' + data['access_token']

            #  GETTING THE PASSWORD
            timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
            passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
            business_short_code = "174379"
            data = business_short_code + passkey + timestamp
            encoded = base64.b64encode(data.encode())
            password = encoded.decode('utf-8')


            # BODY OR PAYLOAD
            payload = {
                "BusinessShortCode": "174379",
                "Password": "{}".format(password),
                "Timestamp": "{}".format(timestamp),
                "TransactionType": "CustomerPayBillOnline",
                "Amount": "1",  # use 1 when testing
                "PartyA": phone,  # change to your number
                "PartyB": "174379",
                "PhoneNumber": phone,
                "CallBackURL": "https://modcom.co.ke/job/confirmation.php",
                "AccountReference": "account",
                "TransactionDesc": "account"
            }

            # POPULAING THE HTTP HEADER
            headers = {
                "Authorization": access_token,
                "Content-Type": "application/json"
            }

            url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest" #C2B URL

            response = requests.post(url, json=payload, headers=headers)
            print (response.text)
            return render_template('mpesa_payment.html', msg = 'Please Complete Payment in Your Phone')
        else:
            return render_template('mpesa_payment.html', total_amount=total_amount)

    else:
        return redirect('/login')

# xampp
if __name__ == '__main__':
    app.debug = True
    app.run()


