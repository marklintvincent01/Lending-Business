import functools
from flask import Flask, render_template, request, redirect, session, url_for, flash
from forms import RegistrationForm, LoginForm
from flask_mysqldb import MySQL
import MySQLdb.cursors
import string
from random import choice
from datetime import date
from passlib.hash import sha256_crypt

app = Flask(__name__)

app.config['SECRET_KEY'] = 'f9773dc56c46b09f651bfdfad603adc8'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'lending_business'

mysql = MySQL(app)

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not session.get('id'):
            return redirect(url_for('loginpage'))

        return view(**kwargs)
    return wrapped_view

@app.route('/')
@app.route('/home')
def landingpage():
    return render_template('landingpage.html')

@app.route('/about')
def aboutpage():
    return render_template('about.html')

#, methods=['GET', 'POST']
@app.route('/employees', methods=['GET', 'POST'])
@login_required
def register():
    register_form = RegistrationForm()
    msg = ''
    
    if request.method == 'POST':
        Fname = register_form.Fname.data
        Mname = register_form.Mname.data
        Mname = register_form.Mname.data
        age = register_form.age.data
        contact_num = register_form.contact_num.data
        address = register_form.address.data
        username = register_form.username.data
        password = register_form.password.data
        print(password)
        email = register_form.email.data
        date_hired = date.today()
        dob = register_form.dateofbirth.data
        gender = register_form.gender.data
        id = IDGeneratorCheck()
        hashed_password = sha256_crypt.hash(password)
        print(hashed_password)

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM lender_employee WHERE username = %s', (username,))
        account = cursor.fetchone()
        

        if account:
            msg = 'Account already exists!' 
        else:
            cursor.execute(f"""
                INSERT INTO lender_employee VALUES
                ({id}, '{Fname}', '{Mname}', '{Fname}', {age}, '{contact_num}', '{address}', '{username}', '{hashed_password}', '{email}', '{date_hired}', '{dob}', '{gender}');
            """)
            mysql.connection.commit()

        flash(f'Account created for {register_form.username.data}!', 'success')
        return redirect(url_for('register'))
         
    return render_template('employees.html', register_form=register_form)

@app.route('/login', methods=['GET', 'POST'])
def loginpage():
    login_form = LoginForm()

    if request.method == 'POST':
        # Create variables for easy access
        username = login_form.Lusername.data
        password = login_form.Lpassword.data
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM lender_employee WHERE username = %s', (username,))
            account = cursor.fetchone()
            lpass_hashed = account.get("lender_password")
            verify = sha256_crypt.verify(password, lpass_hashed)
        except:
            flash("The username you entered isn't connected to an account.")
            return redirect(url_for('loginpage'))

        if verify:
            session['loggedin'] = True
            session['id'] = account['LenderID']
            session['username'] = account['username']
            return redirect(url_for('register'))
        else:
            flash("The password you entered is incorrect.")
            return redirect(url_for('loginpage'))

        #The username or mobile number you entered isn't connected to an account.
    else:  
        return render_template('loginpage.html', title='Login', login_form=login_form)

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('loginpage'))



def IDGenerator():
    chars = string.digits
    random =  ''.join(choice(chars) for _ in range(4))
    digits_to_int = int(random)
    return digits_to_int

def IDGeneratorCheck():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    idgen = IDGenerator()

    cursor.execute('SELECT * FROM lender_employee WHERE LenderID = %s', (idgen,))
    id = cursor.fetchone()

    while id:
        idgen = IDGenerator()

    return idgen



if __name__ == '__main__':
    app.run(debug = True)
