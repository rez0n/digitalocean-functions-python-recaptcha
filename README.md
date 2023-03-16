# DigitalOcean Functions: Send Email using AWS SES
This repository is a PoC of the marketing website (landing page) hosted on DigitalOcean Apps as static website
and "Function" component to process for example newsletter subscription secured by reCAPTCHA v3.

This repository can be deployed via "Create App" dialog.

### Environment variables
```
RECAPTCHA_SECRET_KEY=  # required
RECAPTCHA_REQUIRED_V3_SCORE=  # optional, default 0.5
```
You also need adjust reCAPTCHA "SITE KEY" in the script.js and "apiUrl" to set function component public URL
