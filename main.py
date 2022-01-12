import functools
from flask import Flask, render_template, request, redirect, session, url_for, flash
from forms import RegistrationForm, LoginForm, CustomerForm
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

        if session.get('roleid') == 2:
            return redirect(url_for('aboutpage'))

        return view(**kwargs)
    return wrapped_view

@app.route('/')
@app.route('/home')
def landingpage():
    return render_template('landingpage.html')

@app.route('/about')
def aboutpage():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def loginpage():
    login_form = LoginForm()

    if request.method == 'POST':
        username = login_form.Lusername.data
        password = login_form.Lpassword.data
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM lender_employee WHERE username = %s', (username,))
            account = cursor.fetchone()
            lender_id = account.get("lenderID")
            cursor.execute('SELECT role_id FROM user_role WHERE lenderID = %s', (lender_id,))
            user_role = cursor.fetchone()
            roleid = user_role.get("role_id")
            lpass_hashed = account.get("lender_password")
            verify = sha256_crypt.verify(password, lpass_hashed)
        except:
            flash("The username you entered isn't connected to an account.")
            return redirect(url_for('loginpage'))

        if verify:
            session['loggedin'] = True
            session['id'] = account['lenderID']
            session['username'] = account['username']
            session['roleid'] = user_role['role_id']
            if roleid == 1:  
                return redirect(url_for('register'))
            else:
                return redirect(url_for('aboutpage'))

        else:
            flash("The password you entered is incorrect.")
            return redirect(url_for('loginpage'))

    else:  
        return render_template('loginpage.html', title='Login', login_form=login_form)

@app.route('/employees', methods=['GET', 'POST'])
@login_required
def register():
    register_form = RegistrationForm()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''
        SELECT le.lenderID, CONCAT(le.Lname, ", ", le.Fname, " ", le.Mname) AS "name", le.username, le.age, le.email, le.date_hired, le.dob, le.contact_num, le.address, le.gender, r.role_name
        FROM lender_employee AS le 
        INNER JOIN user_role AS ur
            ON le.lenderID = ur.lenderID
        INNER JOIN roles AS r
            ON ur.role_id = r.role_id
        ORDER BY name ASC
        ''')
    data = cursor.fetchall()
    status = 1
    if request.method == 'POST':
        Fname = register_form.Fname.data
        Mname = register_form.Mname.data
        Lname = register_form.Lname.data
        age = register_form.age.data
        contact_num = register_form.contact_num.data
        address = register_form.address.data
        username = register_form.username.data
        password = register_form.password.data
        email = register_form.email.data
        date_hired = date.today()
        dob = register_form.dateofbirth.data
        gender = register_form.gender.data
        role = register_form.role.data
        id = IDGeneratorCheck('employee')
        hashed_password = sha256_crypt.hash(password)
        cursor.execute('SELECT * FROM lender_employee WHERE username = %s', (username,))
        account = cursor.fetchone()

        if account:
            #raise ValidationError("Account already exists!")
            #msg = 'Account already exists!'
            #flash('Account already exists!')
            # errors ={'Error':'Account already exists.'}
            # data = json.dumps(errors)
            # return jsonify(data)
            status = 2
            
        else:
            cursor.execute(f"""
                INSERT INTO lender_employee VALUES
                ('{id}', '{Fname}', '{Mname}', '{Lname}', '{username}', '{hashed_password}', {age}, '{email}', '{date_hired}', '{dob}', '{contact_num}', '{address}', '{gender}');
            """)
            cursor.execute(f"""
                INSERT INTO user_role VALUES
                ({role}, '{id}');
            """)
            mysql.connection.commit()

        if status == 2:
            flash(f'Username "{register_form.username.data}" already exists!', 'danger')
        else:
            flash(f'Account created for {register_form.username.data}!', 'success')
        #return jsonify(status='ok')
        return redirect(url_for('register'))
        
    else:
        return render_template('employees.html', register_form=register_form, data=data)


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('loginpage'))

@app.route('/customers', methods=['GET', 'POST'])
def customers():
    cus_form = CustomerForm()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''
        SELECT c.cusID, CONCAT(c.Lname, ", ", c.Fname, " ", c.Mname) AS "c_name", c.contact_num, c.address, c.loan_amount, c.gender, c.email, c.loan_made, c.dob, CONCAT(cm.Lname, ", ", cm.Fname, " ", cm.Lname) AS "cm_name", cm.contact_num AS "c_contact_num", cm.address AS "c_address", pm.payment_Mode, r.rate_package
        FROM customer AS c
        INNER JOIN co_maker AS cm
            ON c.cusID = cm.cusID
        INNER JOIN payment_mode AS pm
            ON c.mode_ID = pm.mode_ID
        INNER JOIN rates AS r
            ON c.rateID = r.rateID
        ORDER BY c_name ASC
        ''')
    data = cursor.fetchall()
    
    if request.method == 'POST':
        id = IDGeneratorCheck('customer')
        Fname = cus_form.Fname.data
        Mname = cus_form.Mname.data
        Lname = cus_form.Lname.data
        email = cus_form.email.data
        gender = cus_form.gender.data
        contact_num = cus_form.contact_num.data
        dob = cus_form.dateofbirth.data
        address = cus_form.address.data
        amount = cus_form.amount.data
        mode = cus_form.mode.data
        rate = cus_form.rate.data
        loan_made = date.today()
        c_Fname = cus_form.c_Fname.data
        c_Mname = cus_form.c_Mname.data
        c_Lname = cus_form.c_Lname.data
        c_contact_num = cus_form.c_contact_num.data
        c_address = cus_form.c_address.data
        # contract = cus_form.contract.data

        cursor.execute(f"""
            INSERT INTO customer VALUES
            ('{id}', '{Fname}', '{Mname}', '{Lname}', '{contact_num}', '{address}', {amount}, {mode}, {rate}, '{gender}', '{email}', '{loan_made}', '{dob}');
        """)
        cursor.execute(f"""
            INSERT INTO co_maker VALUES
            ('{id}', '{c_Fname}', '{c_Mname}', '{c_Lname}', '{c_contact_num}', '{c_address}');
            """)
        mysql.connection.commit()

        flash(f'Customer {cus_form.Lname.data} added!', 'success')
        #return jsonify(status='ok')
        return redirect(url_for('customers'))
        
    else:
        return render_template('customers.html', cus_form=cus_form, data=data)



def IDGenerator():
    chars = string.digits
    random =  ''.join(choice(chars) for _ in range(4))

    return random

def IDGeneratorCheck(table):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    idgen = IDGenerator()

    if table == 'customer':
        cursor.execute('SELECT * FROM customer WHERE cusID = %s', (idgen,))
        id = cursor.fetchone()
        while id:
            idgen = IDGenerator()
    else:
        cursor.execute('SELECT * FROM lender_employee WHERE lenderID = %s', (idgen,))
        id = cursor.fetchone()
        while id:
            idgen = IDGenerator()

    return idgen



if __name__ == '__main__':
    app.run(debug = True)
