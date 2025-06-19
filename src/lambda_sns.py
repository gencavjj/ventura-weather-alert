import os
import requests
import boto3

def lambda_handler(event, context):
    url = 'https://api.weather.gov/stations/KOXR/observations/latest'
    headers = {"User-Agent": os.environ.get("USER_AGENT", "weather-alert-lambda@example.com")}

    try:
        obs_data = requests.get(url, headers=headers, timeout=10).json()
        temp_c = obs_data['properties']['temperature']['value']

        if temp_c is None:
            return {'status': 'No temperature data'}

        temp_f = (temp_c * 9/5) + 32

        if temp_f >= float(os.environ.get("TEMP_THRESHOLD_F", 50)):
            sns = boto3.client('sns', region_name=os.environ["AWS_REGION"])
            response = sns.publish(
                PhoneNumber=os.environ["PHONE_NUMBER"],
                Message=f"Temp Alert: {temp_f:.1f}°F in Ventura, CA."
            )
            return {'status': 'SMS sent', 'temp_f': temp_f, 'sns_message_id': response['MessageId']}
        else:
            return {'status': 'No alert', 'temp_f': temp_f}

    except Exception as e:
        return {'status': 'Error', 'message': str(e)}
