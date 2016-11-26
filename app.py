# coding=utf-8
import pymysql
import pymysql.cursors
from flask import Flask, render_template, jsonify
from flask import request
#import MySQLdb
from sqlalchemy import null

app = Flask(__name__)


@app.route("/")
def main():
    return render_template('/index.html')

@app.route("/Details")
def output():
    db = pymysql.connect(host="raspberry.ci2gh79a5gmr.us-west-2.rds.amazonaws.com", port=3306, user="pi",
                         passwd="raspberry", db="RASPBERRY")
    cursor = db.cursor()
    reply={
      'devices' : ['E0:98:61:E5:F6:30', '14:30:C6:83:BB:47'] ,
      'start_time': '22:59:59',
      'end_time': '23:59:59',
     'update_time': '1 day'
    }
    return jsonify(reply)



@app.route("/login", methods=['POST','GET'])
def login():
    _username=request.form['u']
    _password = request.form['p']
    db=pymysql.connect(host="raspberry.ci2gh79a5gmr.us-west-2.rds.amazonaws.com",port=3306,user="pi",passwd="raspberry", db="RASPBERRY")
    cursor=db.cursor()

    cursor.execute("select password,professor_ID,professor_name from professors where professor_username=%s",_username)

    if cursor.rowcount<=0:
        return render_template("/index.html", errmsg='* User not present')
    else:
        for record in cursor:
            if _password==record[0]:
                lectDict={}
                professorID=int(record[1])
                professorName=record[2]
                a=()
                cursor.execute("SELECT lecture_id,lecture_name FROM RASPBERRY.lecture where professorID=%s", professorID)
                for lectures in cursor:
                    lectDict[lectures[0]]=lectures[1]
                return render_template("/classe.html",lectDicts=lectDict)
            else:
                from flask import json
                return render_template("/index.html", errmsg='* Wrong Password')
    cursor.close()
   # print("inside Login",_username)
    return " "

@app.route("/class",methods=['POST','GET'])
def classDet():
  #  classId = request.form['classNo']
    data = []
    db = pymysql.connect(host="raspberry.ci2gh79a5gmr.us-west-2.rds.amazonaws.com", port=3306, user="pi",
                         passwd="raspberry", db="RASPBERRY")
    cursor = db.cursor()
    cursor.execute("SELECT b.student_ID, b.student_name, attendance_date, attendance_status FROM RASPBERRY.attendance a right join RASPBERRY.students b  on a.student_ID=b.student_ID where b.lecture_ID=1 order by b.student_name")
    for record in cursor:
        if record[3] is not 'P':
            data.append([record[0],record[1],'','A'])
        else:
            data.append([record[0], record[1], record[2], record[3]])
    return render_template('/Attendance.html', items=data)



@app.route("/getStudentDetails", methods=['GET','POST'])
def getStudentDetail(): 
    
    req= request.json
    studentid = req["studentid"]
    mac_adr = req["mac_adr"]
    username = req["username"]
    name = req["name"]
    password = req["password"]
    isLogin = req["isLogin"]
    db = pymysql.connect(host="raspberry.ci2gh79a5gmr.us-west-2.rds.amazonaws.com", port=3306, user="pi",
                         passwd="raspberry", db="RASPBERRY")

    if isLogin:
        isloginFailed = True
        cursor = db.cursor()   
        print password
        cursor.execute("SELECT password FROM RASPBERRY.students where student_ID= %s limit 1", int(studentid))
        for record in cursor:
            print record[0]
            if (null!=record) and (record[0]==password):
                isloginFailed=False
                cursor.execute(
                    "SELECT attendance_date, attendance_status FROM RASPBERRY.attendance  where student_ID=%d order by b.student_name")

        jsonResp={
        "isLoginFailed": isloginFailed,
            "error": "LoginFailed",
            "attendance": ""
        }     
    else:
        
     
    return jsonify(jsonResp)




if __name__=="__main__":
    app.run(port=5000)