# 🌤️ Ventura Weather Alert (AWS Lambda)

This AWS Lambda project sends weather alerts via **email (SES)** or **SMS (SNS)** when temperatures in Ventura, CA exceed a configurable threshold. It uses real-time NOAA data and is fully automated with EventBridge Scheduler.

---

## 🚀 Features

- ✅ Real-time temperature from [weather.gov](https://api.weather.gov/)
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

---

### 3. Create IAM Role

#### Name:
`LambdaWeatherAlertRole`

#### Trust Policy:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": [
          "lambda.amazonaws.com",
          "scheduler.amazonaws.com"
        ]
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

#### Attach AWS-managed Policies:
- `AWSLambdaBasicExecutionRole`
- `AmazonSESFullAccess` (for email)
- `AmazonSNSFullAccess` (for SMS)

#### Inline Policy (to allow EventBridge Scheduler to invoke Lambda):
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "lambda:InvokeFunction",
      "Resource": "arn:aws:lambda:<REGION>:<ACCOUNT_ID>:function:venturaWeatherAlertSES"
    }
  ]
}
```

**Policy name:** `AllowInvoke_VenturaWeatherAlert`  
**Description:** `Grants EventBridge Scheduler permission to invoke the venturaWeatherAlertSES Lambda function.`  
> Replace `<REGION>` and `<ACCOUNT_ID>` with your actual AWS region and account ID.

---

### 4. Deploy Lambda Functions

| Function       | Handler                          |
|----------------|----------------------------------|
| Email Alert    | `lambda_email_alert.lambda_handler` |
| SMS Alert      | `lambda_sms_alert.lambda_handler`   |

- Upload `weather-alert.zip`
- Runtime: Python 3.12
- Assign IAM Role: `LambdaWeatherAlertRole`

---

### 5. Set Environment Variables

| Key              | Example Value              |
|------------------|----------------------------|
| EMAIL_SENDER     | alerts@yourdomain.com      |
| EMAIL_RECIPIENT  | you@example.com            |
| PHONE_NUMBER     | +14435551234               |
| TEMP_THRESHOLD_F | 50                         |
| AWS_REGION       | us-west-1                  |
| USER_AGENT       | yourname@yourdomain.com    |

---

## 📨 Amazon SES Setup
- Verify sender & recipient emails
- (Optional) Request production access from AWS Support
- Set SES-related env vars in Lambda

---

## 📲 Amazon SNS Setup
- Add numbers in the SMS sandbox
- Request production access if needed
- Set `PHONE_NUMBER` in environment

---

## 📅 EventBridge Scheduler Setup

| Field            | Value                          |
|------------------|--------------------------------|
| Schedule name    | `ventura-weather-schedule`     |
| Type             | `rate(1 hour)`                 |
| Time zone        | `America/Los_Angeles`          |
| Payload          | `{}` (empty JSON)              |
| Flexible window  | Optional, e.g., 5 minutes      |
| Start time       | Must be in the past            |
| Target           | Lambda invoke → `venturaWeatherAlertSES` |
| Execution role   | `LambdaWeatherAlertRole`       |

---

## 🧪 Testing

1. In Lambda, test with:
```json
{}
```

2. Check logs in **CloudWatch**:
```
/aws/lambda/venturaWeatherAlertSES
```

---

## 🧹 Best Practices

- ❌ Never hardcode credentials or secrets
- ✅ Use environment variables for configuration
- 🔐 Apply least privilege for IAM roles
- 📉 Monitor logs, errors, and quotas via CloudWatch, SES, and SNS dashboards

---

## 📄 License
MIT License

---

## 👤 Author
**Jeremy Gencavage**  
[kingtidesolutions.com](https://kingtidesolutions.com)  
GitHub: [@gencavjj](https://github.com/gencavjj)
