import pymysql
from flask import Flask, render_template, redirect, url_for, request

conn = pymysql.connect(host = 'sql1.njit.edu', user = 'mhj5', password = 'mike023133', db = 'mhj5', cursorclass = pymysql.cursors.DictCursor)
cur = conn.cursor()


def logIn(username, password):
    cur.execute('SELECT permission, ID FROM people WHERE (username = \''+ username +'\' && password = \''+ password +'\')')
    if(cur.rowcount != 0):
        return cur.fetchall()[0]
    else:
        return "No match"

def LoggInCheck(user, passwd):    
    try:
        result = logIn(user, passwd)
        if(result['permission'] == "No match"):
            return redirect(url_for('logInSite'))
        return result
    except:
        print('server error')
        return redirect(url_for('logInSite'))

def courseSearch(CRN, name, term):
    cur.execute('SELECT * FROM courses WHERE (CRN = '+ CRN +' || name = '+ name +' || term = '+ term +')')
    if(len(cur.fetchall()) != 0):
        return cur.fetchall()
    else:
        return "Not found"

def addUser(first, last, user, passwd, permission):
    if(cur.execute('SELECT username FROM people WHERE (username = \''+ user +'\')') != 0):
        return  'Username \'' + user + '\' is already in system'
    else:
        cur.execute("INSERT INTO people (first, last, username, password, permission) VALUES ('"+first+"','"+last+"','"+user+"','"+passwd+"','"+permission+"')")
        conn.commit()
        return first + ' ' + last + ' has benn added'

def addCourse(num, name, credit):
    if(cur.execute("SELECT * FROM courses WHERE (courseNum = '"+ num +"' || name = '"+ name +"')") != 0):
        return  num + '-' + name + ' is already in system'
    else:
        cur.execute("INSERT INTO courses (courseNum, name, credits) VALUES ('" + num + "','" + name + "',"+ credit +")")
        conn.commit()
        return num + '-' + name + ' has been added'

def removeCourse(num, name):
    if(num == ''):
        course = name
    else:
        course = num
    if(cur.execute("SELECT * FROM courses WHERE (courseNum = '"+ num +"' || name = '"+ name +"')") < 0):
        return  course + ' is not in system'
    else:
        cur.execute("DELETE FROM courses WHERE (courseNum = '"+ num +"' || name = '"+ name +"')")
        conn.commit()
        return course + ' has been removed'

def courseAdd(ID, courseNum):
    if(cur.execute("SELECT courseNum FROM courses WHERE courseNum = '"+ courseNum +"'") == 0):
        return courseNum + " is not in system"
    if(cur.execute("SELECT * FROM classes WHERE (courseNum = '"+ courseNum +"' && ID = "+ ID +")") != 0):
        return "Course already added"
    else:
        cur.execute("INSERT INTO classes (ID, courseNum) VALUES ("+ ID +", '"+ courseNum +"')")
        conn.commit()
        return "Course added"

def courseDrop(ID, courseNum):
    if(cur.execute("SELECT courseNum FROM courses WHERE courseNum = '"+ courseNum +"'") == 0):
        return courseNum + " is not in system"
    if(cur.execute("SELECT * FROM classes WHERE (courseNum = '"+ courseNum +"' && ID = "+ ID +")") == 0):
        return "Course has not been added"
    else:
        cur.execute("DELETE FROM classes WHERE (courseNum = '"+ courseNum +"' && ID = '"+ ID +"')")
        conn.commit()
        return "Course dropped"




app = Flask(__name__)
@app.route('/', methods = ['GET', 'POST'])
def logInSite():
    return render_template('login.html')


@app.route('/LoggedIn', methods = ['POST'])
def loggingIn():
    user = request.form['username']
    passwd = request.form['password']

    result = LoggInCheck(user, passwd)

    creds = {'username' : user, 'password' : passwd , 'permission': result['permission'], 'ID' : result['ID']}

    if(result['permission'] == 'admin'):
        return render_template('formpage.1.html', cred = creds)

    if(result['permission'] == 'student'):
        return render_template('formpage.2.html', cred = creds)

    if(result['permission'] == 'teacher'):
        return render_template('formpage.3.html', cred = creds)

    return '<h1>Permission: '+ result['permission'] +'<br>UserID: '+ str(result['ID']) +'</h1>'

@app.route('/Process', methods = ['POST'])
def Processing():
    if request.form.post['submitAddNewUser']:
        return addUser(request.form[addFirst], request.form[addLast], request.form[addUser], request.form[addPasswd], request.form[permission])
    else:
        return render_template('login.html')

if __name__ == '__main__':
    app.run(debug = True)
