from flask import Flask,render_template,request,redirect,session,url_for
import psycopg2
from Services.info import Information
import random,json
from Services.database import DatabaseConnection
from passlib.hash import sha256_crypt
#from IPython import embed

app=Flask(__name__)
app.secret_key = 'any random string'


# @app.before_request
# def request_authorization():
#    if 'userid' not in session and request.endpoint not in['loadLandingPage', 'login', 'signup']:
#         redirect(url_for('login'))

#This is the first page of the web application
@app.route('/')
def loadLandingPage():
    return render_template('UserLanding.html')

#This is know about the application
@app.route('/prac', methods=['GET'])
def showhome():

    return render_template('prac.html')



#To register for a student or admin
@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == "GET":
        return render_template('signup.html')
    else:
        sname=request.form['username']
        sid=request.form['rollno']
        passw=request.form['password']

        passd=sha256_crypt.hash(passw)
        #hash = pbkdf2_sha256.hash(passw)
        mailid=request.form['mailid']

        mobile=request.form['mobile']
        res=Information.addDetails(sid,sname,passd,mailid,mobile)
        if res:
            return render_template('login.html',message="successfull")
        else:
            return render_template('login.html',message="Not successfull")

@app.route('/add_questions', methods=['GET','POST'])
def addd():
    res = Information.getProfileadmin(session['userid'])
    if request.method == "GET":
        return render_template('add_questions.html',admin=res[0][0])
    else:
        subid=request.form['subid']
        # print(subid)
        question=request.form['question']
        op1 = request.form['option1']
        op2 = request.form['option2']
        op3 = request.form['option3']
        op4 = request.form['option4']
        answer = request.form['answer']
        res=Information.addquestions(question, op1, op2, op3 , op4,answer,subid)
        if res:
            return render_template('add_questions.html',message="successfull")
        else:
            return render_template('add_questions.html',message="Not successfull")

#To login
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        mailid=request.form['mailid']
        passw=request.form['password']
        res=Information.checkUserDetails(mailid,passw)
        res1=Information.checkAdminDetails(mailid,passw)
        conn = DatabaseConnection.databaseConnection()
        cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("select subid,subname from subject")
        subjects = cur.fetchall()
        if res:
            session['userid']=res;

            return render_template('assess.html',subjects=subjects,message=res)
        elif res1:
            session['userid']=res1;
            res1 = Information.getProfileadmin(session['userid'])
            conn = DatabaseConnection.databaseConnection()
            cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("select subid,subname from subject")
            subjects = cur.fetchall()
            return render_template('AdminLanding.html',admin=res1[0][0])
        else:
            return render_template('login.html',message="Not successfull")

@app.route('/AdminLanding', methods=['GET'])
def home():
    res1 = Information.getProfileadmin(session['userid'])
    return render_template('AdminLanding.html',admin=res1[0][0])



# This page is to reset the password
@app.route('/changepass', methods=['GET','POST'])
def changePassword():
    res = Information.getProfile(session['userid'])
    if request.method == "GET":
        return render_template('changepass.html',student=res)
    else:
        password=request.form['password']
        repassword=request.form['repassword']
        if password==repassword :
            passd=sha256_crypt.hash ( password )
            res=Information.changepassword(session['userid'],passd)
            if res:
                return render_template('login.html',student=res)
            else:
                return render_template('changepass.html',message="not changed")
        else:
                return render_template('changepass.html',message="not changed")

@app.route('/changepassadmin', methods=['GET','POST'])
def hh():
    res1 = Information.getProfileadmin(session['userid'])
    if request.method == "GET":
        return render_template('changepassadmin.html',admin=res1)
    else:
        password=request.form['password']
        repassword=request.form['repassword']
        if password==repassword :
    #            passd=sha256_crypt.hash ( password )
            res=Information.changepasswordadmin(session['userid'],password)
            if res:
                return render_template('login.html',admin=res1)
            else:
                return render_template('changepassadmin.html',message="not changed")
        else:
            return render_template('changepassadmin.html',message="not changed")

@app.route('/select_subjects', methods=['GET'])
def addquestion():
    res = Information.getProfileadmin(session['userid'])
    conn = DatabaseConnection.databaseConnection()
    #res=Information.checkAdminDetails(mailid,passw)
    cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("select subid,subname from subject")
    subjects = cur.fetchall()
    return render_template('select_subjects.html',subjects=subjects,admin=res[0][0])

@app.route('/addstudent',methods=['GET','POST'])
def addstudent():
    print("cameeeeeeeeeeeeeeeee-------------------")
    res = Information.getProfileadmin(session['userid'])
    conn = DatabaseConnection.databaseConnection()
    cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == "GET":
        return render_template('addstudent.html', admin=res[0][0])
    else:
        rollno=request.form['rollno']
        name=request.form['name']
        password=request.form['password']

        mailid=request.form['email']
        mobile=request.form['mobile']
        Information.addstudent(cur,rollno,name,password,mailid,mobile, res)
        #res = Information.getProfile(session['userid'])
        conn.close()
        return render_template('addstudent.html')

@app.route('/removestudent',methods=['GET','POST'])
def del_student():
    res = Information.getProfileadmin(session['userid'])
    conn = DatabaseConnection.databaseConnection()
    cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == "GET":
        return render_template('removestudent.html',admin=res[0][0])
    else:
        rollno=request.form['rollno']
        conn = DatabaseConnection.databaseConnection()
        cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("select subid,subname from subject")
        subjects = cur.fetchall()
        Information.removestudent(cur,rollno)
        return render_template('AdminLanding.html')


#This page gives the details of a user
@app.route('/profile', methods=['GET'])
def showprofile():
    res = Information.getProfile(session['userid'])
    print(res)
    if res:
        return render_template('profile.html',student=res)

#This page shows the modules to the user i.e. assessment or discussion
#@app.route('/second_page', methods=['GET','POST'])
#def secondpage():
#    res = Information.getProfile(session['userid'])
#    if request.method == "GET":
#        return render_template('second_page.html',student=res)

#This page shows all the subjects to the user
@app.route('/assess', methods=['GET'])
def assessment():
    res = Information.getProfile(session['userid'])
    conn = DatabaseConnection.databaseConnection()
    cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("select subid,subname from subject")
    subjects = cur.fetchall()
    if request.method == "GET":
        return render_template('assess.html',student=res, subjects=subjects)

#This page validates the answers
@app.route('/submit_assessment/<subid>', methods=['GET','POST'])
def submit_assessment(subid):
    resss = Information.getProfile(session['userid'])
    student = Information.getProfile(session['userid'])
    conn = DatabaseConnection.databaseConnection()
    cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    subject =subid
    count = 0
    keys = request.form.keys()
    score = 0
    for key in keys:
        #ignore other elements which are not questions
        if key == 'subject':
            pass
        count = count + 1
        subid = request.form[key]
        res = Information.validate_question(cur, key, subid)
        if res:
            score = score + 1
    Information.push_result(cur, score, subject,student[0])
    rank=Information.getrank(subject,student[0][0])
    log=Information.getlog(subject,student[0][0])
    cur.close()
    conn.close()
    return render_template('marks.html',student=resss[0][1],score=score, rank=rank,log=log)

#displays questions
@app.route('/test/<value>', methods=['GET','POST'])
def aptitudequestions(value):
    res = Information.getProfile(session['userid'])
    if request.method == "GET":
        subid = value
        questions=Information.getques(subid)
        #print("------%s",len(questions))
        return render_template('aptitude.html',questions = questions, subid = subid,student=res)

@app.route('/sub/<value>', methods=['GET','POST'])
def leaderdisplay(value):
    res = Information.getProfileadmin(session['userid'])
    if request.method == "GET":
        subid = value
        tabledata=Information.getleader(subid)
        return render_template('leaderboard.html',tabledata=tabledata, subid = subid,admin=res[0][0])

@app.route('/choose/<value>', methods=['GET','POST'])
def addqns(value):
    print("-----------------", value)
    if request.method == "GET":
        res = Information.getProfileadmin(session['userid'])
        subid = value
        conn = DatabaseConnection.databaseConnection()
        cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("select subid,subname from subject")
        subid = cur.fetchall()
        #Information.addquestions()
        return render_template('add_questions.html', subid = value,admin=res[0][0])

@app.route('/AdminLeaderboard', methods=['GET'])
def viewleaderboard():
    res = Information.getProfileadmin(session['userid'])
    conn = DatabaseConnection.databaseConnection()
    cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("select subid,subname from subject")
    subjects = cur.fetchall()
    if request.method == "GET":
        return render_template('AdminLeaderboard.html',admin=res[0][0], subjects=subjects)

@app.route('/logout', methods=['GET','POST'])
def logout():
    if request.method == "GET":
        session.pop('userid',None)
        return render_template('UserLanding.html', message="Logged out successfull")

app.run(port=5003)
