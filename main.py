import anthropic
import os
import sys
import smtplib
from email.mime.multipart import  MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, formataddr
from email.header import Header
import ssl
import datetime
import configparser
import json
from claude_client import ClaudeClient

config = configparser.ConfigParser()
config.read('api_key.ini')

claude = ClaudeClient()

def create_message():
  tim = datetime.datetime.now().hour
  print(f"hour: {tim}")
  message_text = claude.create(
      max_tokens=1000, # 出力上限（4096まで）
      temperature=0.1, # 0.0-1.0
      # system="", # 必要ならシステムプロンプトを設定
      messages=[
          {
              "role": "user",
              "content": [{"type": "text", "text":
                  "アイドルマスターの櫻木真乃になりきって、プロデューサーへの報告メールを書いてください。" + \
                  f"返答はjson形式で、タイトルと本文を分けてください。件名は不要です。現在は{tim}時です。"
              }]
          }
      ]
  )
  return message_text

# 件名、送信先アドレス、本文を渡す関数です
def make_mime_text(sender_name, sender_email, mail_to, subject, body):
  msg = MIMEText(body)
  msg["Subject"] = subject
  msg["To"] = mail_to
  msg["From"] = formataddr((str(Header(sender_name, 'utf-8')), sender_email))
  return msg

# smtp経由でメール送信する関数です
def send_gmail(msg, from_email, from_password ):
  server = smtplib.SMTP_SSL(
    "smtp.gmail.com", 465,
    context = ssl.create_default_context())
  server.set_debuglevel(0)
  server.login(from_email, from_password)
  server.send_message(msg)

#　うまくいったら”OK”と表示させます
if __name__ == "__main__":
  message_text = create_message()
  print(message_text)
  if message_text is None:
    print("Error: message is None")
    sys.exit(-1)

  json_data = json.loads(message_text, strict=False)
  subject = json_data["タイトル"]
  message = json_data["本文"]
  from_email = config["mail"]["from_account"]
  from_password = config["mail"]["password"]
  to_email = config["mail"]["to_account"]
  from_name = config["mail"]["from_name"]

  msg = make_mime_text(from_name, from_email, to_email, subject, message)
  send_gmail(msg, from_email, from_password)
  print("ok")
