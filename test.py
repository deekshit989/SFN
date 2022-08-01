import json
import boto3

def lambda_handler():
    
    ses = boto3.client('ses',region_name="us-east-1")

    body = """
	    Hello and welcome to the SES Lambda Python Demo.
	
	    Regards,
	    NKT Studios
    """

    ses.send_email(
	    Source = 'vkallepa@uab.edu',
	    Destination = {
		    'ToAddresses': [
                'rohanhamsala@gmail.com',
                'vk00773663@gmail.com'
		    ]
	    },
	    Message = {
		    'Subject': {
			    'Data': 'SES Demo',
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
    
    return {
        'statusCode': 200,
        'body': json.dumps('Successfully sent email from Lambda using Amazon SES')
    }

lambda_handler()