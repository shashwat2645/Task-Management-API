from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List


conf = ConnectionConfig(
    MAIL_USERNAME="notifications.dev.services@gmail.com",
    MAIL_PASSWORD="qhfl fqmn jyyt kusf",
    MAIL_FROM="notifications.dev.services@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="Task Management API",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True

)


async def send_mail(email: List[str]):
    html = """<p>Hi, Thanks for registering here...</p>"""
    message = MessageSchema(
        subject="Registration Successful",
        recipients = email,
        body = html,
        subtype = MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    return {"message": "Email has been sent"}

