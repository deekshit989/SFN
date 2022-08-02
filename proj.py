from crypt import methods
from email import message
import boto3
import os
from django.shortcuts import render
import psycopg2
import json
import datetime
from flask import Flask,flash, request,redirect, render_template,url_for

s3 = boto3.client("s3")
# ses = boto3.client("ses")
app = Flask(__name__)  
app.secret_key = 'jfsahiwesdsdhks'

# AWS Access Key ID: AKIAT3EJQHP3FKZ66LSA
# AWS Secret Access Key : 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

@app.route('/',methods=["GET","POST"])
def index():
    return render_template("signin.html")

@app.route("/signup",methods=["GET","POST"])
def signupIndex():
    return render_template("signup.html")

@app.route("/signin",methods=["GET","POST"])
def signinIndex():
    return render_template("signin.html")

@app.route("/signupsubmit",methods=["GET","POST"])
def signupsubmit():
    f_name = request.form.get("f_name")
    l_name = request.form.get("l_name")
    u_email = request.form.get("u_email")
    u_password = request.form.get("u_password")
    print("f_name",f_name,"l_name",l_name,"email",u_email,"password",u_password)
    db_conn = psycopg2.connect(
        database="postgres", user='postgres', password='Deekshit2399', host='database-1-instance-1.cpfgthxswpv6.us-east-1.rds.amazonaws.com', port= '5432'
    )
    db_conn_cur = db_conn.cursor()
    db_conn_cur.execute("""insert into users_data(first_name,last_name,email_id,password) values (%s,%s,%s,%s) """,(f_name,l_name,u_email,u_password))
    db_conn.commit()
    return render_template("signin.html")

@app.route("/signinsubmit",methods=["GET","POST"])
def signinsubmit():
    u_email = str(request.form.get("u_email"))
    u_password = request.form.get("u_password")
    print(u_email,u_password)
    db_conn = psycopg2.connect(
        database="postgres", user='postgres', password='Deekshit2399', host='database-1-instance-1.cpfgthxswpv6.us-east-1.rds.amazonaws.com', port= '5432'
    )
    db_conn_cur = db_conn.cursor()
    db_conn_cur.execute("""select * from users_data where email_id = '{email}' and password = '{password}' """.format(email = u_email,password =u_password))
    password_matcher = len(db_conn_cur.fetchall()) > 0
    print(password_matcher)
    if password_matcher:
        return render_template("index.html")
    else:
        message="Invalid Username or Password"
        return render_template("signin.html",message=message)
    

@app.route("/submit",methods=["GET","POST"])
def submitForm():
    file_upload_input = request.files["file_upload_input"]
    file_upload_input.save(file_upload_input.filename.replace(" ",""))
    recipient_1 = request.form.get("recipient_1")
    recipient_2 = request.form.get("recipient_2")
    recipient_3 = request.form.get("recipient_3")
    recipient_4 = request.form.get("recipient_4")
    recipient_5 = request.form.get("recipient_5")
    print(file_upload_input.filename.replace(" ",""))
    s3_upload_return = s3.upload_file(file_upload_input.filename,"bucketproj",file_upload_input.filename.replace(" ",""))
    email_client = boto3.client('ses',region_name="us-east-1")
    s3_file_link = "https://bucketproj.s3.amazonaws.com/{}".format(file_upload_input.filename.replace(" ",""))
    body = """Please click on the below link to download the file
    
            {}
    """.format(s3_file_link)
    emails_list = [recipient_1]
    if recipient_2:
        emails_list = [recipient_1,recipient_2]
    if recipient_3:
        emails_list = [recipient_1,recipient_2,recipient_3]
    if recipient_4:
        emails_list = [recipient_1,recipient_2,recipient_3,recipient_4]
    if recipient_5:
        emails_list = [recipient_1,recipient_2,recipient_3,recipient_4,recipient_5]
    print(emails_list)
    email_client.send_email(
        Source = 'vkallepa@uab.edu',
	    Destination = {
		    'ToAddresses': emails_list
	    },
	    Message = {
		    'Subject': {
			    'Data': 'Project File Upload',
			    'Charset': 'UTF-8'
		    },
		    'Body': {
			    'Text':{
				    'Data': body,
				    'Charset': 'UTF-8'
			    }
		    }
	    }
    )
    db_conn = psycopg2.connect(
        database="postgres", user='postgres', password='Deekshit2399', host='database-1-instance-1.cpfgthxswpv6.us-east-1.rds.amazonaws.com', port= '5432'
    )
    db_conn_cur = db_conn.cursor()
    current_time_stamp = datetime.datetime.now()
    db_conn_cur.execute("""insert into upload_data_billing(file_name,uploaded_on,emails_list) values (%s,%s,%s) """,(file_upload_input.filename,current_time_stamp,emails_list))
    db_conn.commit()
    
    return render_template("index.html")

if __name__=='__main__':
   app.run()