import smtplib, ssl, os, zipfile
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def zip_files(path, file_name):
    if path:
        with zipfile.ZipFile(os.path.join(path, file_name), 'w') as file:
            for filename in os.listdir(path):
                if filename and filename.endswith(".csv"):
                    file.write(filename, compress_type = zipfile.ZIP_DEFLATED)
                    # file.write(os.path.join(path, filename), compress_type = zipfile.ZIP_DEFLATED)


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

def main():
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = "x@gmail.com"
    receiver_email = "x@gmail.com"
    other_receiver_email = "x@gmail.com"
    password = ""

    message = MIMEMultipart("alternative")
    message["Subject"] = "Teste Multipart"
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Bcc"] = other_receiver_email  # Recommended for mass emails

    # Create the plain-text and HTML version of your message
    text_msg = """\
    Olá,
    Teste de email com texto simples e com html
    """
    html_msg = """\
    <html>
    <body>
        <p>Olá,<br>
        Teste de email com texto simples e com html<br>
        <a href="http://www.realpython.com">Real Python</a> 
        has many great tutorials.
        </p>
    </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(MIMEText(text_msg, "plain"))
    message.attach(MIMEText(html_msg, "html"))

    # path = f'C:{os.sep}Users{os.sep}king_{os.sep}Documents{os.sep}workspace_python{os.sep}email'
    path = f'C:{os.sep}tmp'
    zip_file_name = 'sheets.zip'
    zip_files(path, zip_file_name)
    attach_files(message, path)

    context = ssl.create_default_context()
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit()


if __name__ == '__main__': main()