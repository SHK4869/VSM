from flask import Flask, render_template, request, flash, redirect, url_for, session
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from functools import wraps
from flask_mysqldb import MySQL

app=Flask(__name__)


# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'sa_project'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('index.html')

def is_player_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'player_logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('player_login'))
    return wrap

def is_LA_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'LA_logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('LA_login'))
    return wrap

# Register Form Class
class LARegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    idd = StringField('ID', [validators.Length(min=1, max=25)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])

    confirm = PasswordField('Confirm Password')

@app.route('/LA_reg', methods=['GET', 'POST'])
def LA_reg():
    form = LARegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        cur = mysql.connection.cursor()
        name = form.name.data
        idd = form.idd.data
        password = form.password.data
        print(name)
        print(idd)
        print(password)
        # Create cursor
        #cur = mysql.connection.cursor()

        # Execute query
        #cur.execute("INSERT INTO player(login, password, s1, s2, s3,c1,c2) VALUES(%s, %s, %s, %s, %s, %s, %s)", (username, password, class1, class3, class3, c1,c2))

        # Commit to DB
        #mysql.connection.commit()

        # Close connection
        #cur.close()
        cur.execute("INSERT INTO la VALUES(%s, %s, %s)", (idd, name, password))
        #s1 = cur.fetchall()
        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('LA_login'))
    return render_template('LA_reg.html', form=form)

@app.route('/LA_login', methods=['GET','POST'])
def LA_login():
    if request.method=='POST':
        cur = mysql.connection.cursor()
        login=request.form['login']
        password_given=request.form['password']
        #result=CURSOR.execute("SELECT * FROM LA WHERE login=%s",[login])
        print(login)
        print(password_given)
        #print(cur.execute("SELECT * FROM LA WHERE LA_ID=%s",[login]))
        result = cur.execute('SELECT LA_ID, Password FROM la WHERE LA_ID=%s AND Password=%s', (login, password_given))
        print(result)
        cur.close()
        if result>0:
        
            session['LA_logged_in']=True
            session['LA_username']=login
            return redirect(url_for('LA_dashboard'))
        else:
            error='No User Found'
            flash(error)
            form = LARegisterForm(request.form)
            return render_template('LA_reg.html',form=form)
    return render_template('LA_login.html')

# Register Form Class
class playerRegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    idd = StringField('ID', [validators.Length(min=1, max=25)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])

    confirm = PasswordField('Confirm Password')


@app.route('/player_reg', methods=['GET','POST'])
def player_reg():
    form = playerRegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        idd = form.idd.data
        password = form.password.data

        print(name)
        print(idd)
        print(password)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO player VALUES(%s, %s, %s, %s)", (idd, name,1000, password))
        #s1 = cur.fetchall()
        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()
        # Create cursor
        #cur = mysql.connection.cursor()

        # Execute query
        #cur.execute("INSERT INTO player(login, password, s1, s2, s3,c1,c2) VALUES(%s, %s, %s, %s, %s, %s, %s)", (username, password, class1, class3, class3, c1,c2))

        # Commit to DB
        #mysql.connection.commit()

        # Close connection
        #cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('player_login'))
    return render_template('player_reg.html', form = form)

@app.route('/player_login', methods=['GET','POST'])
def player_login():
   
    if request.method=='POST':
        cur = mysql.connection.cursor()
        login=request.form['login']
        password_given=request.form['password']
        #result=CURSOR.execute("SELECT * FROM LA WHERE login=%s",[login])
        result = cur.execute('SELECT Player_ID, Password FROM player WHERE Player_ID=%s AND Password=%s', (login, password_given))
        
        cur.close()
        if result>0:
        
            session['player_logged_in']=True
            session['player_username']=login
            return redirect(url_for('player_dashboard'))
        else:
            error='No User Found'
            flash(error)
            form = playerRegisterForm(request.form)
            return render_template('player_reg.html',form=form)
    return render_template('player_login.html')

@app.route('/notifications.html')
def notifications():
    return render_template('notifications.html')

#database me add karne wala idhar
@app.route('/add_news', methods=['GET','POST'])
def add_news():
    #print(request.form['Title'])
    if request.method=='POST':
        

        #s1 = cur.fetchall()
        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()
    return render_template('add_news.html')

@app.route('/player_buy')
def player_buy():
    #UPDATE IDHAR
    #agar ad ya edit project se aa a=raha hai toh form ka data uthao else database se uthao using project title
    idd= request.args.get('idd', None)
    print(idd)
    if request.method == 'POST' and idd=="new":
        #if ttitle doesnt exist, INSERT else UPDte
        #db me naya project add kardo

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO project VALUES(%s, %s, %s, %s, %s)", (project_title, project_date, project_duration, project_description, project_professor))
        mysql.connection.commit()
        session['data'] = request.form
        print(request.form['Task3_date'])
        return render_template('LA_view_project.html', form = request.form)
    #db se jo dashboard se idd mila wo project uthao
    data = {}
    data['Task3_des']="ewaeas"
    data['Task3_date']="654"
    session['data'] = data
    return render_template('player_buy.html', form = data)

"""
@app.route('/player_buy')
@is_player_logged_in
def player_buy():
    idd= request.args.get('idd', None)
    print(idd)
    data = {}
    data['Title']="Title"
    data['Description']="des"
    data['Duration']="34-34"
    data['Date']="2121"
    data['Professor']="sir"
    data['player1']="s1"
    data['player2']="s2"
    data['player3']="s3"
    data['Status1']="design"
    data['Status1_Date']="34"
    data['Status1_marks']="4"
    data['Status2']="s2"
    data['Status2_Date']="3"
    data['Status2_marks']="7"
    data['Status3']="s3"
    data['Status3_Date']="32"
    data['Status3_marks']="0"
    data['Status4']="eww"
    data['Status4_Date']="232"
    data['Status4_marks']="4"
    data['Status5']="s3"
    data['Status5_Date']="43"
    data['Status5_marks']="4"
    data['Task1']="sas"
    data['Task1_des']="asdsasa"
    data['Task1_date']="33"
    data['Task2']="esds"
    data['Task2_des']="2"
    data['Task2_date']="645"
    data['Task3']="dsf"
    data['Task3_des']="ewaeas"
    data['Task3_date']="654"
    session['data'] = data
    return render_template('player_project_view.html', form=data)
"""
@app.route('/LA_project_edit', methods=['GET','POST'])
def LA_project_edit():
    
    return render_template('LA_project_edit.html', form = session['data'])

@app.route('/LA_dashboard')
def LA_dashboard():
    #database se count aur right first panel leo with proj title

    data = [] #list of dictionaries
    data = [{'Title':"Helllo",'Date':"23/4/2018",'Professor':"Sir",'player1':"Humaira",'player2':"Khatoon",'player3':"Sayyed"},{'Title':"fdssfd",'Date':"23/4/2011",'Professor':"Sir",'player1':"Humaira",'player2':"Khatoon",'player3':"Sayyed"},{'Title':"dsasd2",'Date':"3/4/2018",'Professor':"Sir",'player1':"Humaira",'player2':"Khatoon",'player3':"Sayyed"}]
    return render_template('LA_dashboard.html', data = data)

@app.route('/player_dashboard')
def player_dashboard():
    cur = mysql.connection.cursor()
    result = cur.execute('SELECT * FROM stock')
    data1 = cur.fetchall()
    cur.close()
    cur = mysql.connection.cursor()
    data = dict()
    data['stocks'] = data1
    result = cur.execute('SELECT * FROM transactions')
    result = cur.fetchall()
    data['player_stocks'] = result
    cur.close()
    print(data)
    return render_template('player_dashboard.html', data = data)

@app.route('/player_profile')
def player_profile():
    return render_template('player_profile.html')

@app.route('/LA_profile')
def LA_profile():
    return render_template('LA_profile.html')

@app.route('/LA_logout')
def LA_logout():
    del session['LA_logged_in']
    flash('You are now logged out', 'success')
    return redirect(url_for('LA_login'))

@app.route('/player_logout')
def player_logout():
    del session['player_logged_in']
    flash('You are now logged out', 'success')
    return redirect(url_for('player_login'))


if __name__=="__main__":
    app.secret_key='shhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh'
    app.run(port=5001,debug=True)