import os
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText


load_dotenv()


secret_key = os.getenv("JWT_SECRET_KEY")
secret_refresh_key = os.getenv("JWT_REFRESH_SECRET_KEY")

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
PASSWORD_RESET_EXPIRE_MINUTES = 15  # Token expires in 15 minutes
ALGORITHM = "HS256"


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)

def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
        
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
         
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, secret_key, ALGORITHM)
     
    return encoded_jwt

def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, secret_refresh_key, ALGORITHM)
    return encoded_jwt


def create_password_reset_token(email: str):
    expire = datetime.utcnow() + timedelta(minutes=PASSWORD_RESET_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "email": email}
    return jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)

def send_password_reset_email(email: str, token: str):
    reset_link = "http://localhost:8000/reset-password?token=" + token
    html_message = """
    <html>
      <body>
        <p>Click the link to reset your password: <a href="{link}">Reset Password</a></p>
      </body>
    </html>
    """.format(link=reset_link)
    
    message = MIMEText(html_message, "html")
    message["Subject"] = "Password Reset Request"
    message["From"] = "howellsdemilade2007@gmail.com"
    message["To"] = email

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("howellsdemilade2007@gmail.com", "bgfa ywsk cjzv ctzo")
        server.sendmail("howellsdemilade2007@gmail.com", email, message.as_string())

# Example usage
# send_password_reset_email("user@example.com", "your_token_here")