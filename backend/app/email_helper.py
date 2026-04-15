import smtplib
from email.message import EmailMessage
import os

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS") if os.getenv("EMAIL_ADDRESS") else "dmitriy.kuptsov@gmail.com"
EMAIL_PASSWORD = "ctss qyjr onlq zxis"; #os.getenv("EMAIL_PASSWORD") if os.getenv("EMAIL_PASSWORD") else "FUCK YOU UP"
DOWNLOAD_LINK = os.getenv("EMAIL_PASSWORD") if os.getenv("EMAIL_PASSWORD") else "http://localhost/api/download/#order/#token"

def send_download_link(recipient, order, token):
    msg = EmailMessage()
    msg["Subject"] = "EDA-Archives report is ready!"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = recipient

    msg.set_content(f"""
Good day super star fella,

Please download your report using the following link

{DOWNLOAD_LINK.replace("#token", token).replace("#order", order)}

""")

    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background:#f9fafb; padding:20px;">
      <div style="max-width:600px;margin:auto;background:white;padding:30px;border-radius:12px;box-shadow:0 10px 25px rgba(0,0,0,0.1);">
        
        <h2 style="margin-top:0;">Good day, Fella!</h2>
        
        <p>Thank you for using our EDA-Archives service! Please press the link to download your gift!</p>

        <div style="text-align:center;margin:30px 0;">
          <a href="{DOWNLOAD_LINK.replace("#token", token).replace("#order", order)}" style="
            background: linear-gradient(135deg, #4f46e5, #7c3aed);
            color: white;
            padding: 14px 28px;
            text-decoration: none;
            border-radius: 8px;
            font-weight: bold;
            display: inline-block;
          ">
            DOWNLOAD YOUR REPORT
          </a>
        </div>
        <hr style="border:none;border-top:1px solid #eee;margin:30px 0;">
      </div>
    </body>
    </html>
    """

    msg.add_alternative(html_content, subtype="html")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

