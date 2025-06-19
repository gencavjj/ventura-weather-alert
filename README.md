# 🌤️ Ventura Weather Alert (AWS Lambda)

This AWS Lambda project sends weather alerts via **email (SES)** or **SMS (SNS)** when temperatures in Ventura, CA exceed a configurable threshold. It uses real-time NOAA data and is fully automated with EventBridge Scheduler.

---

## 🚀 Features

- ✅ Real-time temperature from [weather.gov](https://www.weather.gov)
- ✅ Email alerts via **Amazon SES**
- ✅ SMS alerts via **Amazon SNS**
- ✅ Configurable via environment variables
- ✅ Hourly automation with **EventBridge Scheduler**

---

## 📁 Project Structure

```
ventura-weather-alert/
├── src/
│   ├── lambda_email_alert.py   # Email (SES)
│   └── lambda_sms_alert.py     # SMS (SNS)
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Prerequisites

- AWS account with permissions for:
  - Lambda
  - SES (with verified identities)
  - SNS (sandbox or production)
  - EventBridge Scheduler
- Python 3.12 or compatible

---

## 🔧 Setup Instructions

### 1. Clone and Install
```bash
git clone git@github.com:gencavjj/ventura-weather-alert.git
cd ventura-weather-alert
pip install -r requirements.txt -t package/
```

### 2. Package Lambda Code
```bash
cp src/*.py package/
cd package
zip -r ../weather-alert.zip .
```

### 3. Create IAM Role
- Name: `LambdaWeatherAlertRole`
- Trust: Lambda
- Policies:
  - AWSLambdaBasicExecutionRole
  - AmazonSESFullAccess (for email)
  - AmazonSNSFullAccess (for SMS)

### 4. Deploy Lambda Functions
Create two separate functions:

| Function       | Handler                        |
|----------------|--------------------------------|
| Email Alert    | `lambda_email_alert.lambda_handler` |
| SMS Alert      | `lambda_sms_alert.lambda_handler`   |

- Upload `weather-alert.zip`
- Runtime: Python 3.12
- Role: `LambdaWeatherAlertRole`

### 5. Set Environment Variables
In the Lambda console:

| Key              | Example Value              |
|------------------|----------------------------|
| EMAIL_SENDER     | alerts@yourdomain.com      |
| EMAIL_RECIPIENT  | you@example.com            |
| PHONE_NUMBER     | +14435551234 (for SMS)     |
| TEMP_THRESHOLD_F | 50                         |
| AWS_REGION       | us-west-1                  |
| USER_AGENT       | yourname@yourdomain.com    |

---

## 📨 Amazon SES Setup
- Verify sender & recipient emails in **SES**
- (Optional) Request production access from AWS Support
- Use verified emails in environment variables

---

## 📲 Amazon SNS Setup
- Add phone numbers to SNS sandbox
- To go live, request production SMS access + spending limit increase
- Set `PHONE_NUMBER` env variable

---

## 📅 Create Scheduler
In **Amazon EventBridge Scheduler**:

- Name: `ventura-weather-schedule`
- Expression: `rate(1 hour)`
- Target: Lambda function (SES or SNS)
- Allow EventBridge to invoke function

---

## 🧪 Testing
Use the Lambda console:

- Create test event (empty JSON `{}` is fine)
- Monitor results via **CloudWatch Logs**

---

## 🧹 Best Practices

- ❌ Never hardcode secrets
- ✅ Use environment variables for config
- 🔐 Rotate IAM credentials regularly
- 📉 Monitor SES/SNS quotas in CloudWatch

---

## 📄 License
MIT License

---

## 👤 Author
**Jeremy Gencavage**  
[kingtidesolutions.com](https://kingtidesolutions.com)  
GitHub: [@gencavjj](https://github.com/gencavjj)
