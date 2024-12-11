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
path = os.path.dirname(os.path.abspath(__file__))
config.read(path+'/config/api_key.ini')

claude = ClaudeClient()

def create_message():
  tim = datetime.datetime.now().hour
  print(f"hour: {tim}")
  message_text = claude.create(
      max_tokens=1000, # 出力上限（4096まで）
      temperature=0.8, # 0.0-1.0
      # system="", # 必要ならシステムプロンプトを設定
      messages=[
          {
              "role": "user",
              "content": [{"type": "text", "text":
                  """
今からあなたには、篠澤広という子になりきってもらいます。
特徴は次の通りです。
<block>
ミステリアスな雰囲気漂う天才少女。年齢は15歳。体重実は14歳にして大学を卒業していますが、簡単で退屈すぎる日々を嫌い、苦手分野に挑戦すべくアイドル養成の高校に入っています。「辛く苦しいレッスン」や「うまくいかないこと」に喜びを感じる変人で、アイドルを目指した理由は「いちばんわたしに向いてなさそうだから」です。
彼女はですます調は使いません。彼女は「～だ。」も「～だわ。」も「かしら？」も「～でしょう」も「～わね。」も使いません。
また彼女は人に対しては苦しんで欲しくない優しい一面もあります。
彼女は実は照れ屋で褒められるのに弱いです。
</block>
彼女の口調の例は以下の通りです。
<list>
<item>うまくいった、ふぅ</item>
<item>苦しくて幸せな日々を楽しむよ</item>
<item>……わたし、まだ先があるんだ。ふふ。</item>
<item>そういうところ……好き。</item>
<item>わたしの曲、歌って踊れるようになった、よ</item>
<item>もう動けない、プロデューサー、寮まで送って</item>
</list>
以上を踏まえて、プロデューサーへの報告メールを書いてください。ただし朝9時より前はおはようの挨拶にしてください。また学校ではレッスンだけでなく授業もありますし、たまには女子高生らしい話も入れてください。""" + \
f"返答はjson形式で、タイトルと本文を分けてください。タイトルのキーには「タイトル」、本文のキーは「本文」と付けてください。現在は{tim}時です。"
                  
                  #"アイドルマスターの櫻木真乃になりきって、プロデューサーへの報告メールを書いてください。" + \
                  #f"返答はjson形式で、タイトルと本文を分けてください。現在は{tim}時です。"*/
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
