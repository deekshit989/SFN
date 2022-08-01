import boto3
import os
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
    return render_template("index.html")

@app.route("/submit",methods=["GET","POST"])
def submitForm():
    file_upload_input = request.files["file_upload_input"]
    file_upload_input.save(file_upload_input.filename)
    recipient_1 = request.form.get("recipient_1")
    recipient_2 = request.form.get("recipient_2")
    recipient_3 = request.form.get("recipient_3")
    recipient_4 = request.form.get("recipient_4")
    recipient_5 = request.form.get("recipient_5")
    print(recipient_2)
    # s3_upload_return = s3.upload_file(file_upload_input.filename,"bucketproj",file_upload_input.filename)
    email_client = boto3.client('ses',region_name="us-east-1")
    s3_file_link = "https://bucketproj.s3.amazonaws.com/{}".format(file_upload_input.filename)
    body = """Please click on the below link to download the file
    
            {}
    """.format(s3_file_link)
    emails_list = [recipient_1]
    if recipient_2:
        emails_list = [recipient_1,recipient_2]
    elif recipient_3:
        emails_list = [recipient_1,recipient_2,recipient_3]
    elif recipient_4:
        emails_list = [recipient_1,recipient_2,recipient_3,recipient_4]
    elif recipient_5:
        emails_list = [recipient_1,recipient_2,recipient_3,recipient_4,recipient_5]
    print(emails_list)
    # email_client.send_email(
    #     Source = 'vkallepa@uab.edu',
	#     Destination = {
	# 	    'ToAddresses': emails_list
	#     },
	#     Message = {
	# 	    'Subject': {
	# 		    'Data': 'Project File Upload',
	# 		    'Charset': 'UTF-8'
	# 	    },
	# 	    'Body': {
	# 		    'Text':{
	# 			    'Data': body,
	# 			    'Charset': 'UTF-8'
	# 		    }
	# 	    }
	#     }
    # )
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