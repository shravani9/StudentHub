from flask import Flask, request
import psycopg2,random
from Services.database import DatabaseConnection
from passlib.hash import sha256_crypt

class Information():
    @classmethod
    #Inserts the user details into the database
    def addDetails(cls,sid,sname,passw,mailid,mobile):
        conn = DatabaseConnection.databaseConnection()
        cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query="insert into student (sid,sname,pass,mailid,mobile) values(%s,%s,%s,%s,%s) RETURNING SID"
        cur.execute(query,(sid,sname,passw,mailid,mobile))
        inline_return = cur.fetchone()
        cur.execute('commit')
        print(inline_return)
        a = inline_return[0]
        cur.close()
        conn.close()
        return a

    @classmethod
    #validates the user login form
    def checkUserDetails(cls,mailid,passw):
        conn = DatabaseConnection.databaseConnection()
        cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query="select pass from student where mailid=%s"
        cur.execute(query,(mailid,))
        res = cur.fetchone()
        if res:
            if(sha256_crypt.verify(passw, res[0])):
                query="select * from student where mailid=%s"
                cur.execute(query,(mailid,))
                ree=cur.fetchone()
                return ree

        else:
            return False

    @classmethod
    #validates the user login form
    def checkAdminDetails(cls,mail_id,passw):
        conn = DatabaseConnection.databaseConnection()
        cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query="select admin_id from admin where mail_id=%s and pswd=%s"
        cur.execute(query,(mail_id,passw))
        if cur.rowcount:
            inline_return = cur.fetchone()
            return inline_return[0]
        else:
            return False

    @classmethod
    #Resets the user password
    def changepassword(cls,sid,passw):
        conn = DatabaseConnection.databaseConnection()
        cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query="UPDATE student SET pass=%s WHERE sid=%s"
        cur.execute(query,(passw,sid[0]))
        query="select * from student where sid=%s"
        cur.execute(query,(sid[0],))
        res = cur.fetchone()
        cur.execute('commit')
        cur.close()
        conn.close()
        return res
    @classmethod
    #Resets the admin password
    def changepasswordadmin(cls,admin_id,passw):
        conn = DatabaseConnection.databaseConnection()
        cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query="UPDATE admin SET pswd=%s WHERE admin_id=%s"
        cur.execute(query,(passw,admin_id))
        cur.execute('commit')
        cur.close()
        conn.close()
        return cur.rowcount


    @classmethod
    #Returns the details of the user
    def getProfile(cls,sid):
        print(sid[0])
        conn = DatabaseConnection.databaseConnection()
        cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query="select * from student where sid = %s"
        cur.execute(query,(sid[0],))
        inline_return = cur.fetchall()
        cur.execute('commit')
        return inline_return

    @classmethod
    #Returns the details of the user
    def getProfileadmin(cls,admin_id):
        conn = DatabaseConnection.databaseConnection()
        cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query="select * from admin where admin_id = %s"
        cur.execute(query,(admin_id,))
        inline_return = cur.fetchall()
        cur.execute('commit')
        return inline_return


    @classmethod
    #Displays the questions
    def getques(cls,subid):
        conn = DatabaseConnection.databaseConnection()
        cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #    aptitudeqns=[]
        query= "select * from question where subid=%s order by RANDOM() LIMIT 10"
        cur.execute(query,(subid,))
        return cur.fetchall()

    @classmethod
    #Displays the questions
    def addquestions(cls,question, op1, op2, op3 , op4, answer,subid):
        conn = DatabaseConnection.databaseConnection()
        cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #    aptitudeqns=[]
        query= "insert into question(qname, op1, op2, op3 , op4, ans, subid) \
         values(%s,%s,%s,%s,%s,%s,%s)"
        cur.execute(query,(question, op1, op2, op3 , op4, answer,subid))
        cur.execute("Commit")
        return True




    @classmethod
    #Displays the questions
    def getleader(cls,subid):
        conn = DatabaseConnection.databaseConnection()
        cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query= "select a.sid,a.sname,round((a.average),2), rank() over(order \
         by a.average desc) from (select t.sid,s.sname,avg(t.score) \
         as average from student s \
         join tests t on s.sid=t.sid where t.subid=%s \
         group by t.sid,t.subid,s.sname order by average desc) as a"
        cur.execute(query,(subid,))
        return cur.fetchall()

    @classmethod
    #Displays the questions
    def getrank(cls,subid,sid):
        conn = DatabaseConnection.databaseConnection()
        cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query= "select a.average, rank() over(order by a.average desc) from (select t.sid,s.sname,avg(t.score) as average from student s join tests t on s.sid=t.sid where t.subid=%s group by t.sid,t.subid,s.sname order by average desc) as a where a.sid=%s"
        cur.execute(query,(subid,sid,))
        return cur.fetchone()

    @classmethod
    def getlog(cls,subid,sid):
        conn = DatabaseConnection.databaseConnection()
        cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query= "select score from tests where subid=%s and sid=%s"
        cur.execute(query,(subid,sid,))
        return cur.fetchall()



    @classmethod
    def validate_question(cls, cur, key, value):
        #print("-------%s",key)
        query="select ans from question where qid=%s"
        cur.execute(query,(key, ))
        answer = cur.fetchone()[0]
        if answer == value:
            return True

    @classmethod
    def push_result(cls,cur,score,subject,userid):
        # query="select subid from subject where subject=%s"
        # cur.execute(query,(subject, ))
        # asd=cur.fetchone()
        query= "insert into tests(sid,subid,score) values(%s,%s,%s)"
        print(userid)
        cur.execute(query,(userid[0],subject,score ))
        cur.execute("Commit")

    #    cur.execute(query,(userid[0],subject[0] ))
        #cur.execute("Commit")

        return True

    @classmethod
    def addstudent(cls,cur,rollno,name,password,mailid,mobile,userid):
        query="insert into student values(%s,%s,%s,%s,%s,%s)"
        cur.execute(query,(rollno,name,password,mailid,mobile,))
        cur.execute("Commit")
        query="select * from admin where admin_id=%s"
        cur.execute(query,(userid[0], ))
        cur.execute("Commit")


        return True

    @classmethod
    def removestudent(cls,cur,rollno):
        query="delete  from student where sid=%s"
        cur.execute(query,(rollno,))
        cur.execute("Commit")
        return True
