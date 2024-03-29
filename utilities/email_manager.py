from pydantic import EmailStr
import smtplib
from email.message import EmailMessage
from string import Template
from pathlib import Path
import os


def send_email_with_subject(email_from: str, email_to: str, email_subject: str, email_content: str):
    email = EmailMessage()
    email['from'] = email_from
    email['to'] = email_to
    email['subject'] = email_subject
    email.set_content(email_content)
    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(os.getenv('NEXT_PUBLIC_EMAIL_ADDRESS'),
                   os.getenv('NEXT_PUBLIC_EMAIL_PASSWORD'))
        smtp.send_message(email)
        # print('sent')


def send_mail(reciever: EmailStr, content: str):
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as connection:
        email_address = os.getenv('NEXT_PUBLIC_EMAIL_ADDRESS')
        email_password = os.getenv('NEXT_PUBLIC_EMAIL_PASSWORD')
        connection.login(email_address, email_password)
        connection.sendmail(from_addr=email_address, to_addrs=reciever,
                            msg=content)


# TODO: fix the parameters, maybe use the name and link as parameters or something else.
def send_html_email_with_subject(email_from: str, email_to: str, email_subject: str, email_content: str):
    """
    Sends an HTML email with a specified subject, from a specified email address to a specified recipient.

    Args:
    email_from (str): The email address from which the email will be sent.
    email_to (str): The email address of the recipient.
    email_subject (str): The subject of the email.
    email_content (str): The content of the email in HTML format.

    Returns:
    None
    """
    html = Template(Path('utilities/templates/reset.html').read_text())
    content = html.substitute(
        {'name': 'name', 'link': 'link'})
    email = EmailMessage()
    email['from'] = email_from
    email['to'] = email_to
    email['subject'] = email_subject
    email.set_content(email_content, 'html')
    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(os.getenv('NEXT_PUBLIC_EMAIL_ADDRESS'),
                   os.getenv('NEXT_PUBLIC_EMAIL_PASSWORD'))
        smtp.send_message(email)
