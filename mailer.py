import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Mailer:
    def __init__(self):
        pass

    @staticmethod
    def send_email(message, headers, url):
        from_adr = "xxx@gmail.com"
        to_adr = ['x1@gmail.com', 'x2@gmail.com']

        gmail_user = "xx@gmail.com"
        gmail_pwd = "xx"
        subject = ', '.join(headers)
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "1177 changes detected! " + subject
        msg['From'] = from_adr
        msg['To'] = ", ".join(to_adr)

        # Create the body of the message (a plain-text and an HTML version).
        text = 'Errors: ' + url
        html = """\
        <html>
         <head></head>
         <body>
           <p>Hey!<br/><br/>
              INSERT_MESSAGE_HERE<br/><br/>
              INSERT_HEADERS_HERE<br/><br/>
              <a href="INSERT_URL_HERE">INSERT_URL_HERE</a><br/>
              <br/>
              Best regards,<br/>
              Logger.54365<br/>
              <br/>
              <br/>
              <br/>
              <br/>
           </p>
         </body>
        </html>
        """

        html = html.replace('INSERT_MESSAGE_HERE', message)
        html = html.replace('INSERT_HEADERS_HERE', "<br/>".join(headers))
        html = html.replace('INSERT_URL_HERE', url)

        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)

        print(msg.as_string())

        try:
            # Send the message with Gmail
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(gmail_user, gmail_pwd)
            server.sendmail(from_adr, to_adr, msg.as_string())
            server.close()
            print('Successfully mailed: ' + ", ".join(to_adr))
        except:
            print('Failed to send mail: ' + ", ".join(to_adr))