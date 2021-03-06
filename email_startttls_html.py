import smtplib, ssl, os, zipfile
from string import Template
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def parse_template_to_string(path, args) -> str:
    with open(path, 'r', encoding='utf-8') as file:
        src = Template(file.read())
        return src.substitute(args)

def is_there_xlsx_files(path) -> bool:
    if path :
        for filename in os.listdir(path):
            if filename and filename.endswith(".xlsx"):
                return True
    return False


def zip_files(path, file_name):
    if path and is_there_xlsx_files(path):
        with zipfile.ZipFile(os.path.join(path, file_name), 'w') as file:
            for filename in os.listdir(path):
                if filename and filename.endswith(".xlsx"):
                    file.write(filename, compress_type = zipfile.ZIP_DEFLATED)

def attach_files(message, path):
    if path:
        for filename in os.listdir(path):
            if filename and filename.endswith(".zip"):
                with open(os.path.join(path, filename), "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f"attachment; filename= {filename}",
                    )
                    message.attach(part)

def attach_process(message):
    dir_path = os.path.dirname(__file__)
    # dir_path = f'C:{os.sep}tmp'
    zip_file_name = 'sheets.zip'
    zip_files(dir_path, zip_file_name)
    if os.path.isfile(os.path.join(dir_path, zip_file_name)):
        attach_files(message, dir_path)


def main():
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = "feniciaresidencia@gmail.com"
    receiver_email = "feniciaresidencia@gmail.com"
    other_receiver_email = "feniciaresidencia@gmail.com"
    password = "uga2buga"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Teste Multipart"
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Bcc"] = other_receiver_email

    try:
        text_msg = parse_template_to_string(os.path.join(os.path.dirname(__file__), f'template{os.sep}text'), args={"name": "Daniel"})
        html_msg = parse_template_to_string(os.path.join(os.path.dirname(__file__), f'template{os.sep}html'), args={"name": "Daniel"})
        message.attach(MIMEText(text_msg, "plain"))
        message.attach(MIMEText(html_msg, "html"))
        attach_process(message)
        context = ssl.create_default_context()
        server = smtplib.SMTP(smtp_server,port)
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as e:
        print(e)
    finally:
        server.quit()


if __name__ == '__main__': main()