import json
import smtplib
from dataclasses import dataclass
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from uuid import UUID, uuid4

from flask import current_app

from setting.util import Setting


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
    mime_text_content: MIMEText = _get_mail_content_mime_text(
        username, str(random_uuid)
    )

    mime_mail: MIMEMultipart = _build_verification_mail(
        [logo_image], "NuOJ 驗證信件", "NuOJ@noreply.me", email, mime_text_content
    )

    current_app.config["mail_verification_code"] |= {random_uuid: username}

    _send_email(mail_sender, mime_mail)


def _send_email(sender: MailSender, mail: MIMEMultipart):
    with smtplib.SMTP(host=sender.server, port=sender.port) as smtp:  # 設定SMTP伺服器
        smtp.ehlo()  # 驗證SMTP伺服器
        smtp.starttls()  # 建立加密傳輸
        smtp.login(sender.mailname, sender.password)  # 登入寄件者gmail
        smtp.send_message(mail)  # 寄送郵件


def _build_verification_mail(
    images: list[MIMEImage],
    subject: str,
    from_address: str,
    to_address: str,
    content: MIMEText,
) -> MIMEMultipart:
    multipart_email = MIMEMultipart()
    multipart_email["subject"] = subject
    multipart_email["from"] = from_address
    multipart_email["to"] = to_address

    for image in images:
        image.add_header("Content-ID", f"<{image.get_filename()}>")
        multipart_email.attach(image)

    multipart_email.attach(content)
    return multipart_email


def _put_parameter_to_mail_content(
    content: str, verification_url: str, username: str
) -> str:
    """
    This function will replace all the {{verification_url}} and {{username}} to the real verification URL and user in the content.
    """
    content = content.replace("{{verification_url}}", verification_url)
    content = content.replace("{{username}}", username)
    return content


def _get_mail_sender() -> MailSender:
    setting: Setting = current_app.config.get("setting", None)
    assert setting is not None

    mail_sender = MailSender(
        setting.mail_server(),
        setting.mail_port(),
        setting.mail_mailname(),
        setting.mail_password(),
    )

    return mail_sender


def _get_logo_mime_image() -> MIMEImage:
    image_content: bytes

    with open("/etc/nuoj/static/logo_min.png", "rb") as file:
        image_content = file.read()

    mime_image = MIMEImage(image_content, name="logo_min.png")
    return mime_image


def _get_mail_content_mime_text(username: str, random_uuid: str) -> str:
    mail_content: str
    setting: Setting = current_app.config.get("setting")
    with open("/etc/nuoj/templates/mail_template.html", "r") as file:
        mail_content = file.read()
    mail_content_with_code = _put_parameter_to_mail_content(
        mail_content, setting.mail_redirect_url() + f"?code={random_uuid}", username
    )
    mime_text_content = MIMEText(mail_content_with_code, "html")
    return mime_text_content
