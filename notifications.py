import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(subject, body, to_email):
    from_email = "your_email@example.com"  # Zajistíme, že je řetězec uzavřený
    from_password = "your_password"

    server = smtplib.SMTP("smtp.example.com", 587)
    server.starttls()
    server.login(from_email, from_password)

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()
