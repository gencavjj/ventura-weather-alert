import os
import requests
import boto3
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    url = 'https://api.weather.gov/stations/KOXR/observations/latest'
    headers = {"User-Agent": os.environ.get("USER_AGENT", "weather-alert-lambda@example.com")}

    logger.info("Lambda function invoked")
    logger.info(f"Requesting data from: {url}")

    try:
        obs_data = requests.get(url, headers=headers, timeout=10).json()
        temp_c = obs_data['properties']['temperature']['value']

        if temp_c is None:
            logger.warning("No temperature data returned from NOAA API")
            return {'status': 'No temperature data'}

        temp_f = (temp_c * 9/5) + 32
        logger.info(f"Temperature (F): {temp_f}")

        threshold = float(os.environ.get("TEMP_THRESHOLD_F", 50))
        if temp_f >= threshold:
            logger.info(f"Threshold exceeded ({threshold}°F), sending email")
            ses = boto3.client('ses', region_name=os.environ["AWS_REGION"])
            response = ses.send_email(
                Source=os.environ["EMAIL_SENDER"],
                Destination={'ToAddresses': [os.environ["EMAIL_RECIPIENT"]]},
                Message={
                    'Subject': {'Data': 'Ventura Weather Alert'},
                    'Body': {'Text': {'Data': f"Temperature is {temp_f:.1f}°F in Ventura, CA."}}
                }
            )
            logger.info(f"Email sent, MessageId: {response['MessageId']}")
            return {'status': 'Email sent', 'temp_f': temp_f, 'ses_message_id': response['MessageId']}
        else:
            logger.info(f"Temperature below threshold ({threshold}°F), no alert sent")
            return {'status': 'No alert', 'temp_f': temp_f}

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        return {'status': 'Error', 'message': str(e)}
