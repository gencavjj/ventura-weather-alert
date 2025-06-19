# 🌤️ Ventura Weather Alert (AWS Lambda)

This project sends weather alerts via **email (Amazon SES)** or **SMS (Amazon SNS)** based on the latest temperature observations in Ventura, CA. The alerts are triggered when the temperature exceeds a configurable threshold, using data from the NOAA API and AWS Lambda automation.


## 🚀 Features


- ✅ Real-time temperature data via [weather.gov](https://api.weather.gov)
- ✅ Email alerts using Amazon SES
- ✅ SMS alerts using Amazon SNS
- ✅ Threshold and recipient info via environment variables
- ✅ Automated hourly checks using EventBridge Scheduler


## 📁 Project Structure


weather-alert/
- ├── lambda_email_alert.py # Lambda function to send email alerts (SES)
- ├── lambda_sms_alert.py # Lambda function to send SMS alerts (SNS)
- ├── README.md # This readme file
- └── .gitignore # Ignores ZIPs and environment files


## ⚙️ Prerequisites


- AWS account with permissions for:
  - Lambda
  - SES (with at least one verified email address)
  - SNS (SMS sandbox or production)
  - EventBridge Scheduler
- Python 3.12 or compatible


## 🔧 Setup Instructions (SOP)


### 1. Clone Repo & Install Dependencies

```bash
git clone https://github.com/YOUR_USERNAME/weather-alert.git
cd weather-alert
pip install requests boto3 -t .
```

### 2. Package Lambda Code

```bash
zip -r weather-alert.zip .
```

### 3. Create IAM Role for Lambda

* Name: `LambdaWeatherAlertRole`
* Trust policy: Lambda
* Attach these AWS-managed policies:

  * `AWSLambdaBasicExecutionRole`
  * `AmazonSESFullAccess` *(for SES functions)*
  * `AmazonSNSFullAccess` *(for SNS functions)*


### 4. Deploy Lambda Functions

Deploy each Lambda function separately:

| Function          | Handler Name                        |
| ----------------- | ----------------------------------- |
| Email Alert (SES) | `lambda_email_alert.lambda_handler` |
| SMS Alert (SNS)   | `lambda_sms_alert.lambda_handler`   |

* Upload `weather-alert.zip` for both functions
* Runtime: Python 3.12
* Assign the `LambdaWeatherAlertRole`


### 5. Configure Environment Variables

Go to **Lambda > Configuration > Environment Variables** and set the following:

| Key                | Example Value                                                        |
| ------------------ | -------------------------------------------------------------------- |
| `EMAIL_SENDER`     | [alerts@yourdomain.com](mailto:alerts@yourdomain.com)                |
| `EMAIL_RECIPIENT`  | [you@example.com](mailto:you@example.com)                            |
| `PHONE_NUMBER`     | +14435551234 (SNS only)                                              |
| `TEMP_THRESHOLD_F` | 50                                                                   |
| `AWS_REGION`       | us-west-1                                                            |
| `USER_AGENT`       | [yourname@yourdomain.com](mailto:yourname@yourdomain.com) (App Name) |

These ensure the code stays clean and secure.

---

## 📨 SES Setup (Email)

1. Open **Amazon SES > Verified Identities**
2. Verify your sender and recipient emails
3. If needed, request production SES access via AWS Support
4. Add the `EMAIL_SENDER` and `EMAIL_RECIPIENT` vars in Lambda

---

## 📲 SNS Setup (SMS)

1. Open **Amazon SNS > SMS and Sandbox**
2. Add your phone number to test SMS alerts
3. Request **production access** and **monthly spend limit** increase to exit sandbox
4. Set `PHONE_NUMBER` env var

---

## 📅 Create Scheduled Trigger

Use Amazon EventBridge Scheduler:

1. Go to **EventBridge > Scheduler**
2. Create schedule:

   * Name: `ventura-weather-schedule`
   * Expression: `rate(1 hour)`
   * Target: Your Lambda function (SES or SNS)
3. Permissions: Allow EventBridge to invoke the function

---

## 🧪 Test the Function

In the AWS Lambda console:

* Use the test event (any JSON payload, or `{}`)
* Check CloudWatch Logs for:

  * Retrieved temperature
  * Email or SMS delivery confirmation

---

## 🧹 Best Practices

* ❌ Never hardcode secrets or credentials in code
* ✅ Use environment variables for all configs
* 🔐 Rotate IAM credentials regularly
* 📉 Monitor SES/SNS quotas and errors in CloudWatch

---

## 📄 License

MIT License

---

## 👤 Author

**Jeremy Gencavage**
[kingtidesolutions.com](https://www.kingtidesolutions.com)

---

GitHub: [@gencavjj](https://github.com/)

