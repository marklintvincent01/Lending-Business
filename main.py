import datetime
import os, secrets
import functools
from flask import Flask, render_template, request, redirect, session, url_for, flash, current_app
from forms import RegistrationForm, LoginForm, CustomerForm, LoanStatus
from flask_mysqldb import MySQL
import MySQLdb.cursors
import string
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
        if not session.get('roleid'):
            return redirect(url_for('loginpage'))
        return view(**kwargs)
    return wrapped_view

def admin_check(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs): 
        if session.get('roleid') != 1:
            return redirect(url_for('customers'))
        return view(**kwargs)
    return wrapped_view

def employee_check(view):
    @functools.wraps(view)
    def wrapped_view2(**kwargs): 
        if session.get('roleid') != 2:
            return redirect(url_for('register'))
        return view(**kwargs)
    return wrapped_view2

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def landingpage():
    loan_stat = LoanStatus()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # if request.method == 'POST':

        # cursor.execute(f'''
        #     SELECT ls.*, CONCAT(c.Lname, ", ", c.Fname, " ", c.Mname) AS "c_name", c.contact_num, c.address, c.loan_amount, c.gender, c.email, c.dob, pm.payment_Mode, r.rate_package, r.interest, CONCAT(le.Lname, ", ", le.Fname, " ", le.Mname) AS "le_name", le.contact_num
        #     FROM loan_status AS ls 
        #     INNER JOIN customer AS c
        #         ON {loan_stat.cus_id.data} = c.cusID
        #     INNER JOIN payment_mode AS pm
        #         ON c.mode_ID = pm.mode_ID
        #     INNER JOIN rates AS r
        #         ON c.rateID = r.rateID
        #     INNER JOIN lender_employee AS le
        #         ON {loan_stat.emp_id.data} = le.lenderID
        #     WHERE ls.cusID = {loan_stat.cus_id.data} AND le.lenderID = {loan_stat.emp_id.data}
        #     ''')
        # ls_data = cursor.fetchone()
    # return render_template('landingpage.html', loan_stat=loan_stat, ls_data=ls_data)
    return render_template('landingpage.html', loan_stat=loan_stat)

@app.route('/about')
def aboutpage():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def loginpage():
    login_form = LoginForm()

    if request.method == 'POST':
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM lender_employee WHERE username = %s', (login_form.Lusername.data,))
            account = cursor.fetchone()
            lender_id = account.get("lenderID")
            cursor.execute('SELECT role_id FROM user_role WHERE lenderID = %s', (lender_id,))
            user_role = cursor.fetchone()
            roleid = user_role.get("role_id")
            lpass_hashed = account.get("lender_password")
            verify = sha256_crypt.verify(login_form.Lpassword.data, lpass_hashed)
        except:
            flash("The username you entered isn't connected to an account.")
            return redirect(url_for('loginpage'))

        if verify:
            session['loggedin'] = True
            session['id'] = lender_id
            session['username'] = login_form.Lusername.data
            session['roleid'] = roleid

            if roleid == 1:  
                return redirect(url_for('register'))
            else:
                return redirect(url_for('customers'))

        else:
            flash("The password you entered is incorrect.")
            return redirect(url_for('loginpage'))

    else:  
        return render_template('loginpage.html', title='Login', login_form=login_form)

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('roleid', None)
    # Redirect to login page
    return redirect(url_for('loginpage'))

@app.route('/employees', methods=['GET', 'POST'])
@login_required
@admin_check
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
        date_hired = date.today()
        id = IDGeneratorCheck('employee')
        hashed_password = sha256_crypt.hash(register_form.password.data)
        cursor.execute('SELECT * FROM lender_employee WHERE username = %s', (register_form.username.data,))
        account = cursor.fetchone()

        if account:
            status = 404
        
        else:
            cursor.execute(f"""
                INSERT INTO lender_employee VALUES
                ('{id}', '{register_form.Fname.data}', '{register_form.Mname.data}', '{register_form.Lname.data}', '{register_form.username.data}', '{hashed_password}', {register_form.age.data}, '{register_form.email.data}', '{date_hired}', '{register_form.dateofbirth.data}', '{register_form.contact_num.data}', '{register_form.address.data}', '{register_form.gender.data}');
            """)
            cursor.execute(f"""
                INSERT INTO user_role VALUES
                ({register_form.role.data}, '{id}');
            """)
            mysql.connection.commit()

        if status == 404:
            flash(f'Username "{register_form.username.data}" already exists!', 'danger')
        else:
            flash(f'Account created for {register_form.username.data}!', 'success')

        return redirect(url_for('register'))
        
    else:
        return render_template('employees.html', register_form=register_form, data=data)

@app.route('/employees/<emp_id>', methods=['GET', 'POST'])
@login_required
@admin_check
def employee_details(emp_id):
    register_form = RegistrationForm()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute(f'''
        SELECT le.lenderID, le.Lname, le.Fname, le.Mname, le.age, le.email, le.date_hired, le.dob, le.contact_num, le.address, le.gender, r.role_id, r.role_name
        FROM lender_employee AS le 
        INNER JOIN user_role AS ur
            ON le.lenderID = ur.lenderID
        INNER JOIN roles AS r
            ON ur.role_id = r.role_id
        WHERE le.lenderID = '{emp_id}'
        ''')
    emp_data = cursor.fetchone()

    if not emp_data:
        flash(f'User "{emp_id}" doesn\'t exist!', 'danger')
    
    if request.method == 'POST':    
        role = request.form.get('role', False)
        

        cursor.execute(f"""
            UPDATE lender_employee
            SET 
                Fname = '{register_form.Fname.data}',
                Mname = '{register_form.Fname.data}',
                Lname = '{register_form.Lname.data}',
                age = {register_form.age.data},
                email = '{register_form.email.data}',
                dob = '{register_form.dateofbirth.data}',
                contact_num = '{register_form.contact_num.data}',
                address = '{register_form.address.data}',
                gender = '{register_form.gender.data}'
            WHERE
                lenderID = '{emp_id}'; 
            """)
        cursor.execute(f"""
            UPDATE user_role
            SET 
                role_id = '{role}'
            WHERE
                lenderID = '{emp_id}';
            """)

        mysql.connection.commit()

    
        flash(f'Employee  #"{emp_id}" updated!', 'success')
        return redirect(url_for('register'))
    else:
        return render_template('employee-details.html', register_form=register_form, emp_data=emp_data)

@app.route('/customers', methods=['GET', 'POST'])
@login_required
@employee_check
def customers():
    cus_form = CustomerForm()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''
        SELECT c.cusID, CONCAT(c.Lname, ", ", c.Fname, " ", c.Mname) AS "c_name", c.contact_num, c.address, c.loan_amount, c.gender, c.email, c.loan_made, c.dob, CONCAT(cm.Lname, ", ", cm.Fname, " ", cm.Lname) AS "cm_name", cm.contact_num AS "c_contact_num", cm.address AS "c_address", pm.payment_Mode, r.rate_package, cl.contract
        FROM customer AS c
        INNER JOIN co_maker AS cm
            ON c.cusID = cm.cusID
        INNER JOIN payment_mode AS pm
            ON c.mode_ID = pm.mode_ID
        INNER JOIN rates AS r
            ON c.rateID = r.rateID
        INNER JOIN collateral AS cl
            ON c.cusID = cl.cusID
        ORDER BY c_name ASC
        ''')
    data = cursor.fetchall()
    
    if request.method == 'POST':
        id = IDGeneratorCheck('customer')
        emp_id = session.get('id')
        loan_made = date.today()
        created = datetime.datetime.now() + datetime.timedelta(days=2*365)
        deadline = created.date()
        collected = 'collected'
        incomplete = 'incomplete'

        cursor.execute(f"""
            INSERT INTO customer VALUES
            ('{id}', '{cus_form.Fname.data}', '{cus_form.Mname.data}', '{cus_form.Lname.data}', '{cus_form.contact_num.data}', '{cus_form.address.data}', {cus_form.amount.data}, {cus_form.mode.data}, {cus_form.rate.data}, '{cus_form.gender.data}', '{cus_form.email.data}', '{loan_made}', '{cus_form.dateofbirth.data}');
        """)
        cursor.execute(f"""
            INSERT INTO co_maker VALUES
            ('{id}', '{cus_form.c_Fname.data}', '{cus_form.c_Mname.data}', '{cus_form.c_Lname.data}', '{cus_form.c_contact_num.data}', '{cus_form.c_address.data}');
            """)
        cursor.execute(f"""
            INSERT INTO loan_status VALUES
            ('{id}', '{emp_id}', {cus_form.amount.data}, '{loan_made}', '{deadline}', '{collected}', '{incomplete}');
            """)
        
        if cus_form.contract.data:
            contract_name = saveAvatar(cus_form.contract.data)
            cursor.execute(f"""
            INSERT INTO collateral VALUES
            ('{id}', '{contract_name}');
            """)
        mysql.connection.commit()

        flash(f'Customer {cus_form.Lname.data} added!', 'success')
        #return jsonify(status='ok')
        return redirect(url_for('customers'))
        
    else:
        return render_template('customers.html', cus_form=cus_form, data=data)


@app.route('/collect')
@login_required
@employee_check
def collect():

    return render_template('collect.html')


@app.route('/customers/<cus_id>', methods=['GET', 'POST'])
@login_required
@employee_check
def customer_details(cus_id):
    cus_form = CustomerForm()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(f'''
        SELECT c.cusID, c.Lname, c.Fname, c.Mname, c.contact_num, c.address, c.loan_amount, c.gender, c.email, c.loan_made, c.dob, cm.Lname AS "c_Lname", cm.Fname AS "c_Fname", cm.Mname AS "c_Mname", cm.contact_num AS "c_contact_num", cm.address AS "c_address", pm.mode_ID, r.rateID
        FROM customer AS c
        INNER JOIN co_maker AS cm
            ON c.cusID = cm.cusID
        INNER JOIN payment_mode AS pm
            ON c.mode_ID = pm.mode_ID
        INNER JOIN rates AS r
            ON c.rateID = r.rateID
        WHERE c.cusID = '{cus_id}'
        ''')
    cus_data = cursor.fetchone()

    if not cus_data:
        flash(f'User "{cus_id}" doesn\'t exist!', 'danger')

    if request.method == 'POST':
        rate = request.form.get('rate', False)

        cursor.execute(f"""
            UPDATE customer
            SET 
                Fname = '{cus_form.Fname.data}',
                Mname = '{cus_form.Mname.data}',
                Lname = '{cus_form.Lname.data}',
                contact_num = '{cus_form.contact_num.data}',
                address = '{cus_form.address.data}',
                loan_amount = {cus_form.amount.data},
                mode_id = {cus_form.mode.data},
                rateid = {rate},
                gender = '{cus_form.gender.data}',
                email = '{cus_form.email.data}',
                dob = '{cus_form.dateofbirth.data}'
            WHERE
                cusID = '{cus_id}'; 
            """)
        cursor.execute(f"""
            UPDATE co_maker
            SET 
                Fname = '{cus_form.c_Fname.data}',
                Mname = '{cus_form.c_Mname.data}',
                Lname = '{cus_form.c_Lname.data}',
                contact_num = '{cus_form.c_contact_num.data}',
                address = '{cus_form.c_address.data}'
            WHERE
                cusID = '{cus_id}';
            """)
        if cus_form.contract.data:
            contractdata = saveAvatar(cus_form.contract.data)
            sendAvatar(cus_id, contractdata)

        mysql.connection.commit()

        flash(f'Customer #{cus_id} updated!', 'success')
        return redirect(url_for('customers'))
        #return jsonify(status='ok')
        
    else:
        return render_template('customer-details.html', cus_form=cus_form, cus_data=cus_data)

@app.route('/customer/delete/<cus_id>')
@login_required
@employee_check
def cus_delete(cus_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM customer WHERE cusID =  %s', (cus_id,))
    mysql.connection.commit()
    flash(f'Customer #{cus_id} deleted!', 'success')
    return redirect(url_for('customers'))

@app.route('/employee/delete/<emp_id>')
@login_required
@admin_check
def emp_delete(emp_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM lender_employee WHERE lenderID =  %s', (emp_id,))
    mysql.connection.commit()
    flash(f'Employee #{emp_id} deleted!', 'success')
    return redirect(url_for('customers'))

# locally save avatar
def saveAvatar(userAvatar):
    
    # configure filename and path
    randName = secrets.token_hex(16)
    _, fileExt = os.path.splitext(userAvatar.filename)
    newFileName = randName + fileExt
    newFilePath = os.path.join(current_app.root_path, 'static', 'contract', newFileName)

    # save avatar in static/avatars
    userAvatar.save(newFilePath)
    
    return newFileName

# update user avatar in database    
def sendAvatar(userID, fileName):
        cur = mysql.connection.cursor()
        
        cur.execute(f'''
                    UPDATE collateral
                    SET contract = '{fileName}'
                    WHERE cusID ='{userID}'
                    ''')
        mysql.connection.commit()


def IDGenerator():
    chars = string.digits + string.ascii_uppercase
    genstring = ''.join(secrets.choice(chars) for i in range(4))

    return genstring

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


#possible magamit system for change username and password
# if status == 404:
#     flash(f'Username "{register_form.username.data}" already exists!', 'danger')
# else: