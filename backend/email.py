import smtplib
from email.message import EmailMessage
from config import EMAIL_ADDRESS, EMAIL_PASSWORD, EMAIL_CONFIRMATION_LINK, PASSWORD_RESET_LINK

def send_account_confirmation(username, recipient, token):
    msg = EmailMessage()
    msg["Subject"] = "Подтверждение аккаунта SolidEngineering"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = recipient

    msg.set_content(f"""
Добрый день,

Пожалуйста подтвердите ваш адрес электронной почты:

{EMAIL_CONFIRMATION_LINK.replace("#token", token)}

Ссылка действует 24 часа.

Если вы не регестрировались на сайте Solid-Engineering.strangebit.io, то проигнорируйте это сообщение.
""")

    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background:#f9fafb; padding:20px;">
      <div style="max-width:600px;margin:auto;background:white;padding:30px;border-radius:12px;box-shadow:0 10px 25px rgba(0,0,0,0.1);">
        
        <h2 style="margin-top:0;">Добрый день</h2>
        
        <p>Спасибо за регестрацию на сайте Solid-Engineering.strangebit.io! Пожалуйста подтвердите ваш адрес электронной почты:</p>

        <div style="text-align:center;margin:30px 0;">
          <a href="{EMAIL_CONFIRMATION_LINK.replace("#token", token).replace("#username", username)}" style="
            background: linear-gradient(135deg, #4f46e5, #7c3aed);
            color: white;
            padding: 14px 28px;
            text-decoration: none;
            border-radius: 8px;
            font-weight: bold;
            display: inline-block;
          ">
            Подтвердить регистрацию
          </a>
        </div>

        <p>Если кнопка не работает, пожалуйста, используйте ссылку:</p>
        <p style="word-break:break-all;color:#4f46e5;">{EMAIL_CONFIRMATION_LINK.replace("#token", token).replace("#username", username)}</p>

        <p style="color:#666;">Ссылка действует 24 часа.</p>

        <hr style="border:none;border-top:1px solid #eee;margin:30px 0;">

        <p style="font-size:12px;color:#999;">
          Если вы не регестрировались на сайте Solid-Engineering.strangebit.io, то проигнорируйте это сообщение.
        </p>

      </div>
    </body>
    </html>
    """

    msg.add_alternative(html_content, subtype="html")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

def send_password_reset_confirmation(username, recipient, token):
    msg = EmailMessage()
    msg["Subject"] = "Подтверждение аккаунта SolidEngineering"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = recipient

    msg.set_content(f"""
Добрый день,

Вы запросили сброс пароля для сервиса SolidEngineering. Пожалуйста подтвердите ваш адрес электронной почты:

{PASSWORD_RESET_LINK.replace("#token", token)}

Ссылка действует 24 часа.

Если вы не запрашивали смену пароля на сайте Solid-Engineering.strangebit.io для вашего аккаунта, то проигнорируйте это сообщение.
""")

    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background:#f9fafb; padding:20px;">
      <div style="max-width:600px;margin:auto;background:white;padding:30px;border-radius:12px;box-shadow:0 10px 25px rgba(0,0,0,0.1);">
        
        <h2 style="margin-top:0;">Добрый день</h2>
        
        <p>Вы запросили сброс пароля для сервиса SolidEngineering. Пожалуйста подтвердите ваш адрес электронной почты:</p>

        <div style="text-align:center;margin:30px 0;">
          <a href="{PASSWORD_RESET_LINK.replace("#token", token).replace("#username", username)}" style="
            background: linear-gradient(135deg, #4f46e5, #7c3aed);
            color: white;
            padding: 14px 28px;
            text-decoration: none;
            border-radius: 8px;
            font-weight: bold;
            display: inline-block;
          ">
            Подтвердить аккаунт
          </a>
        </div>

        <p>Если кнопка не работает, пожалуйста, используйте ссылку:</p>
        <p style="word-break:break-all;color:#4f46e5;">{PASSWORD_RESET_LINK.replace("#token", token).replace("#username", username)}</p>

        <p style="color:#666;">Ссылка действует 24 часа.</p>

        <hr style="border:none;border-top:1px solid #eee;margin:30px 0;">

        <p style="font-size:12px;color:#999;">
          Если вы не запрашивали смену пароля на сайте Solid-Engineering.strangebit.io для вашего аккаунта, то проигнорируйте это сообщение.
        </p>

      </div>
    </body>
    </html>
    """

    msg.add_alternative(html_content, subtype="html")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)