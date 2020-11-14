import smtplib
import ssl
from email.mime.text import MIMEText
import sys, codecs
from datetime import datetime
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(verbose=True, dotenv_path=dotenv_path)

def send_email(email_address, url):
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout)
    gmail_account = os.environ.get("GMAIL_ADDRESS")
    gmail_password = os.environ.get("GMAIL_PASSWORD")  #このアプリ用に発行
    mail_to = email_address
    send_name = "New User" #送信先の名前
    today_date = datetime.today()
    subject = f"Dear {send_name}, please set your Password({today_date})"
    body = f"please set your password at<br>   {url}<br>within 24 hours"
    msg = MIMEText(body, "html") #print(msg)でアルファベット・数字の文字列で表示されていても大丈夫
    msg['Subject'] = subject
    msg['To'] = mail_to
    msg['From'] = gmail_account
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context())
    server.login(gmail_account, gmail_password)
    server.send_message(msg)
    server.close()