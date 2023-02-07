import json
import smtplib
from dataclasses import dataclass
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from uuid import UUID, uuid4

from flask import current_app

from setting_util import mail_redirect_url


@dataclass
class MailSender:
    server: str
    port: int
    mailname: str
    password: str


def send_verification_email(username: str, email: str) -> None:
    random_uuid: UUID = uuid4()
    mail_sender: MailSender = _get_mail_sender()
    logo_image: MIMEImage = _get_logo_mime_image()
    mime_text_content: MIMEText = _get_mail_content_mime_text(username, str(random_uuid))
    
    mime_mail: MIMEMultipart = _build_verification_mail([logo_image], "NuOJ 驗證信件", "NuOJ@noreply.me", email, mime_text_content)
    
    _send_email(mail_sender, mime_mail)


def _send_email(sender: MailSender, mail: MIMEMultipart):
    with smtplib.SMTP(host=sender.server, port=sender.port) as smtp:  # 設定SMTP伺服器
        try:
            smtp.ehlo()  # 驗證SMTP伺服器
            smtp.starttls()  # 建立加密傳輸
            smtp.login(sender.mailname, sender.password)  # 登入寄件者gmail
            smtp.send_message(mail)  # 寄送郵件
            print("Complete!")
        except Exception as e:
            print("Error message: ", e)


def _build_verification_mail(
    images: list[MIMEImage], 
    subject: str, 
    from_address: str, 
    to_address: str, 
    content: MIMEText
) -> MIMEMultipart:
    multipart_email = MIMEMultipart()
    multipart_email["subject"] = subject
    multipart_email["from"] = from_address
    multipart_email["to"] = to_address
    
    for image in images:
        image.add_header('Content-ID', f'<{image.get_filename()}>')
        multipart_email.attach(image)
    
    multipart_email.attach(content)
    return multipart_email


def _put_parameter_to_mail_content(content: str, verification_url: str, username: str) -> str:
    '''
    This function will replace all the {{verification_url}} and {{username}} to the real verification URL and user in the content.
    '''
    content = content.replace("{{verification_url}}", verification_url)
    content = content.replace("{{username}}", username)
    return content

def _get_mail_sender() -> MailSender:
    with open("/etc/nuoj/setting.json", "r") as file:
        file_content = file.read()
        setting_dict = json.loads(file_content)
        mail_info = setting_dict["mail"]
        mail_sender = MailSender(mail_info["server"], mail_info["port"], mail_info["mailname"], mail_info["password"])
        
        return mail_sender

def _get_logo_mime_image() -> MIMEImage:
    image_content: bytes
    
    with open("/etc/nuoj/static/logo_min.png", "rb") as file:
        image_content = file.read()
    
    mime_image = MIMEImage(image_content, name="logo_min.png")
    return mime_image

def _get_mail_content_mime_text(username: str, random_uuid: str) -> str:
    mail_content: str
    with open("/etc/nuoj/templates/mail_template.html", "r") as file:
        mail_content = file.read()
    mail_content_with_code = _put_parameter_to_mail_content(mail_content, mail_redirect_url() + f"?vericode={random_uuid}", username)
    mime_text_content = MIMEText(mail_content_with_code, 'html')
    return mime_text_content

def _send_verification_email_to_stroage(username: str, email: str) -> None:
    random_uuid: UUID = uuid4()
    mail_sender: MailSender = _get_mail_sender()
    logo_image: MIMEImage = _get_logo_mime_image()
    mime_text_content: MIMEText = _get_mail_content_mime_text(username, str(random_uuid))
    
    mime_mail: MIMEMultipart = _build_verification_mail([logo_image], "NuOJ 驗證信件", "NuOJ@noreply.me", email, mime_text_content)
    
    _send_email_to_storage(mail_sender, mime_mail)


def _send_email_to_storage(sender: MailSender, mail: MIMEMultipart) -> None:
    storage_path: str = current_app.config.get("STORAGE_PATH")
    storage_path_object: Path = Path(storage_path)
    mail_file_path: Path = storage_path_object / ("mail.txt")
    sender_file_path: Path = storage_path_object / ('sender.txt')
    
    with open(mail_file_path, "w") as file:
        file.write(mail.as_string())
        
    with open(sender_file_path, "w") as file:
        file.write(str(sender))
    
    print("Complete! [Mock]")