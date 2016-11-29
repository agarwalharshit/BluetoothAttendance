# coding=utf-8
import pymysql
import pymysql.cursors
from flask import Flask, render_template, jsonify
from flask import request
#import MySQLdb

app = Flask(__name__)


@app.route("/")
def main():
    return render_template('/index.html')

@app.route("/login", methods=['POST','GET'])
def login():
    _username=request.form['u']
    _password = request.form['p']

    print _username
    print _password
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
                print "professor"
                print professorID
                cursor.execute("SELECT lecture_id,lecture_name FROM RASPBERRY.lecture where professorID=%s", professorID)
                for lectures in cursor:
                    lectDict[lectures[0]]=lectures[1]
                return render_template("/class.html",lectDicts=lectDict)
            else:
                from flask import json
                return render_template("/index.html", errmsg='* Wrong Password')
    cursor.close()
   # print("inside Login",_username)
    return " "

@app.route("/getClassInfo",methods=['POST','GET'])
def getclassInfo():
    #classId = request.form['classNo']
    #startTime = request.form['starttime']
    #endTime = request.form['endtime']
    #getDate = request.form['getdate']
    #print startTime
    #print endTime
    #print getDate
    print classId
    data = []
    db = pymysql.connect(host="raspberry.ci2gh79a5gmr.us-west-2.rds.amazonaws.com", port=3306, user="pi",
                         passwd="raspberry", db="RASPBERRY")
    cursor = db.cursor()
    if getDate:
        cursor.execute("SELECT b.student_ID, b.student_name, attendance_date, attendance_status FROM RASPBERRY.attendance a right join RASPBERRY.students b  on a.student_ID=b.student_ID where b.lecture_ID=1 and attendance_date=%s order by b.student_name",getDate)
    else:
        cursor.execute("SELECT b.student_ID, b.student_name, attendance_date, attendance_status FROM RASPBERRY.attendance a right join RASPBERRY.students b  on a.student_ID=b.student_ID where b.lecture_ID=1 order by b.student_name")
    for record in cursor:
        if record[3] is not 'P':
            data.append([record[0],record[1],'','A'])
        else:
            data.append([record[0], record[1], record[2], record[3]])
    db.close()
    return render_template('/Attendance.html', items=data)






#Redirect to new class form html
@app.route("/getNewClassForm",methods=['POST','GET'])
def getNewClassForm():
  #  classId = request.form['classNo']
    return render_template('/NewClass.html')

# make entry of new Class
@app.route("/registerNewClass",methods=['POST','GET'])
def registerNewClass():
    startTime = request.form['starttime']
    endTime = request.form['endtime']
    className = request.form['className']
    updateTime = request.form['updateTime']
    professorID=101

    print startTime
    print endTime
    print className
    lectDict = {}
    db = pymysql.connect(host="raspberry.ci2gh79a5gmr.us-west-2.rds.amazonaws.com", port=3306, user="pi",
                         passwd="raspberry", db="RASPBERRY")
    cursor = db.cursor()
    cursor.execute("insert into lecture(lecture_name, professorID,start_time,end_time,update_time) values(%s,%s,%s,%s,%s)", (className,professorID,startTime,endTime,updateTime))
    db.commit()

    cursor.execute("SELECT lecture_id,lecture_name FROM RASPBERRY.lecture where professorID=%s", professorID)
    for lectures in cursor:
        lectDict[lectures[0]] = lectures[1]
    cursor.close()
    db.close()
    return render_template("/class.html", lectDicts=lectDict)

# get class attendance data
@app.route("/getAttendance",methods=['POST','GET'])
def classDetqq():
    classID = request.form['classNo']

    data=[]
    db = pymysql.connect(host="raspberry.ci2gh79a5gmr.us-west-2.rds.amazonaws.com", port=3306, user="pi",
                         passwd="raspberry", db="RASPBERRY")
    cursor = db.cursor()
    print "classID"
    print classID
    cursor.execute("SELECT b.student_ID, b.student_name, attendance_date, attendance_status FROM RASPBERRY.attendance a right join RASPBERRY.students b  on a.student_ID=b.student_ID where b.lecture_ID=%s order by b.student_name",classID)
    for record in cursor:

        if record[3] is not 'P':
            data.append([record[0], record[1], '', 'A'])
        else:
            data.append([record[0], record[1], record[2], record[3]])
    cursor.close()
    db.close()
    return render_template('/Attendance.html', items=data, classID=classID)

# Modify attendance search
@app.route("/modifyAttendanceSearch",methods=['POST','GET'])
def modifyAttendanceSearch():
    classID = request.form['classNo']
    startTime = request.form['starttime']
    endTime = request.form['endtime']
    getDate = request.form['getdate']
    print startTime
    print endTime
    print getDate
    data = []
    db = pymysql.connect(host="raspberry.ci2gh79a5gmr.us-west-2.rds.amazonaws.com", port=3306, user="pi",
                         passwd="raspberry", db="RASPBERRY")
    cursor = db.cursor()
    if getDate:
        cursor.execute("SELECT b.student_ID, b.student_name, attendance_date, attendance_status FROM RASPBERRY.attendance a right join RASPBERRY.students b  on a.student_ID=b.student_ID where b.lecture_ID=%s and attendance_date=%s order by b.student_name",(classID,getDate))
    else:
        cursor.execute("SELECT b.student_ID, b.student_name, attendance_date, attendance_status FROM RASPBERRY.attendance a right join RASPBERRY.students b  on a.student_ID=b.student_ID where b.lecture_ID=%s order by b.student_name",classID)
    for record in cursor:
        if record[3] is not 'P':
            data.append([record[0],record[1],'','A'])
        else:
            data.append([record[0], record[1], record[2], record[3]])

    if startTime and endTime:
        cursor.execute("update lecture set start_time=%s,end_time=%s where lecture_ID=%s",(startTime,endTime,classID))
    elif startTime:
        cursor.execute("update lecture set start_time=%s where lecture_ID=%s",(startTime, classID))
    elif endTime:
        cursor.execute("update lecture set end_time=%s where lecture_ID=%s",(endTime, classID))
    db.commit()
    cursor.close()
    db.close()
    return render_template('/Attendance.html', items=data, classID=classID)









#Apoorva login API
@app.route("/getStudentDetails", methods=['GET','POST'])
def getStudentDetail():
    req= request.json
    i=0
    jsonResp={}

    studentid = req["studentid"]
    mac_adr = req["mac_adr"]
    username = req["username"]
    name = req["name"]
    password = req["password"]
    isLogin = req["isLogin"]
    db = pymysql.connect(host="raspberry.ci2gh79a5gmr.us-west-2.rds.amazonaws.com", port=3306, user="pi",
                         passwd="raspberry", db="RASPBERRY")

    if isLogin=='true':
        isloginFailed = True
        data=""
        cursor = db.cursor()   
        print password
        try:
            cursor.execute("SELECT password FROM RASPBERRY.students where student_ID= %s limit 1", int(studentid))
            for record in cursor:
                i=1
                print record
                print record[0]
                if (record[0]==password):
                    isloginFailed=False
                    data=[]
                    cursor.execute("SELECT attendance_date, attendance_status FROM RASPBERRY.attendance  where student_ID=%s order by attendance_date desc",int(studentid))
                    for record in cursor:
                        listStr={"date":record[0],"attendance":record[1]}
                        print listStr
                        data.append(listStr)
                    jsonResp = {
                        "isLoginFailed": 'false',
                        "error": "LoginFailed",
                        "attendance": data
                    }

                else:
                    jsonResp={
                        "isLoginFailed": "true",
                        "error": "LoginFailed",
                        "attendance": ""
                    }
            if i is 0:
                jsonResp = {
                    "isLoginFailed": "true",
                    "error": "LoginFailed",
                    "attendance": ""
                }


        except Exception:
            jsonResp = {
                "isLoginFailed": "true",
                "error": "LoginFailed:Database Error",
                "attendance": ""
            }
    else:
        print "hiihh"
        cursor = db.cursor()
        data = ""
        print studentid
        print username
        print mac_adr
        print password
        try:
            i=cursor.execute("INSERT INTO `RASPBERRY`.`students` (`student_ID`,`student_name`, `MAC_ID`, `lecture_ID`, `password`) VALUES (%s,%s, %s,'123463',%s)",(studentid,username,mac_adr,password))
            db.commit()
            cursor.close()
            db.close()
            if i==1:
                data = []
                jsonResp = {
                    "isLoginFailed": "false",
                    "error": "SignUpFailed",
                    "attendance": ""
                }
            else:
                jsonResp = {
                    "isLoginFailed": "true",
                    "error": "SignUpFailed",
                    "attendance": ""
                }
        except Exception:
            jsonResp = {
                "isLoginFailed": "true",
                "error": "SignUpFailed:Database Error",
                "attendance": ""
            }

    print jsonResp
    return jsonify(jsonResp)


#Course Details API
@app.route("/CourseDetails")
def output():
    db = pymysql.connect(host="raspberry.ci2gh79a5gmr.us-west-2.rds.amazonaws.com", port=3306, user="pi",
                         passwd="raspberry", db="RASPBERRY")
    cursor = db.cursor()
    cursor.execute("SELECT lecture_ID, start_time, end_time, update_time FROM RASPBERRY.lecture")

    for rows in cursor:
        print rows
        print str(rows[1])
        reply={
            "courseId" : rows[0],
            "startTime" : str(rows[1]),
            "endTime" : str(rows[2]),
            "updateTime" : rows[3]
        }
    return jsonify(reply)


if __name__=="__main__":
    app.run(port=5000)