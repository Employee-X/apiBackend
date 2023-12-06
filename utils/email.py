import smtplib
from email.mime.text import MIMEText

def send_email(body, to_email, smtp_server = "smtp.gmail.com", smtp_port=587, from_email="ebook220033@gmail.com",password="kxehmmuluuofgolw",subject="Customer Query"):
	message = MIMEText(body)
	message['Subject'] = subject
	message['From'] = from_email
	message['To'] = to_email

	with smtplib.SMTP(smtp_server, smtp_port) as server:
		server.starttls()
		server.login(from_email, password)
		server.sendmail(from_email, [to_email], message.as_string())
