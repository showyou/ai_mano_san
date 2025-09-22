import unittest
from unittest.mock import patch, MagicMock
from main_trash import make_mime_text, create_message, send_gmail
import json
from email.mime.text import MIMEText
import email.utils

class TestMainTrash(unittest.TestCase):
    def test_make_mime_text(self):
        """make_mime_text関数のテスト"""
        # テストデータ
        sender_name = "テスト送信者"
        sender_email = "test@example.com"
        mail_to = "to@example.com"
        subject = "テスト件名"
        body = "テスト本文"

        # 関数実行
        msg = make_mime_text(sender_name, sender_email, mail_to, subject, body)

        # 検証
        self.assertIsInstance(msg, MIMEText)
        self.assertEqual(msg["Subject"], subject)
        self.assertEqual(msg["To"], mail_to)
        # Base64エンコードされた送信者名とメールアドレスの検証
        from_addr = email.utils.parseaddr(msg["From"])[1]
        self.assertEqual(from_addr, sender_email)

    @patch('main_trash.ClaudeClient')
    def test_create_message(self, mock_claude):
        """create_message関数のテスト"""
        # モックの設定
        mock_instance = MagicMock()
        mock_claude.return_value = mock_instance
        mock_instance.create.return_value = json.dumps({
            "タイトル": "テストタイトル",
            "本文": "テスト本文"
        })

        # 関数実行
        result = create_message()

        # 検証
        self.assertIsNotNone(result)
        json_data = json.loads(result)
        self.assertIn("タイトル", json_data)
        self.assertIn("本文", json_data)

        # createメソッドが正しく呼び出されたことを確認
        mock_instance.create.assert_called_once()

    @patch('main_trash.smtplib.SMTP_SSL')
    def test_send_gmail(self, mock_smtp):
        """send_gmail関数のテスト"""
        # テストデータ
        msg = MIMEText("テスト本文")
        msg["Subject"] = "テスト件名"
        msg["To"] = "to@example.com"
        msg["From"] = "from@example.com"
        from_email = "from@example.com"
        from_password = "password123"

        # モックの設定
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server

        # 関数実行
        send_gmail(msg, from_email, from_password)

        # 検証
        mock_smtp.assert_called_once()
        mock_server.login.assert_called_once_with(from_email, from_password)
        mock_server.send_message.assert_called_once_with(msg)

if __name__ == '__main__':
    unittest.main()
