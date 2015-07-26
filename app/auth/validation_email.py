"""
Send Validation Email

Using multipart/alternative for text + html
"""

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.headerregistry import Address

from app.config import config


text_template = \
"""
Dear {user.name},

Please validate the email for your Sage developer account by going to
the following link:

{config.baseurl}/#!/validate-email/{user.email_validation_secret}

Please do not reply to this email. If you have any suggestions please
post to the sage-devel mailinglist.  
"""

html_template = \
"""
<html>
  <head></head>
  <body>
    <p>
      Dear {user.name},
    </p>

    <p>
      Please validate the email for your Sage developer account by going to
      the following link:
    </p>

    <p><a href="{config.baseurl}/#!/validate-email/{user.email_validation_secret}">
      {config.baseurl}/#!/validate-email/{user.email_validation_secret}
    </a></p>

    <p>
      Please do not reply to this email. If you have any suggestions please
      post to the sage-devel mailinglist.  
    </p>
  </body>
</html>
"""


def send_validation_email(user):
    local, domain = config.email.sender_addr.split('@', 1)
    sender = str(Address(config.email.sender_name, local, domain))
    
    local, domain = user.email.split('@', 1)
    recipient = str(Address(user.name, local, domain))
    
    html = html_template.format(user=user, config=config)
    text = text_template.format(user=user, config=config)
    
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "E-Mail Verification"
    msg['From'] = sender
    msg['To'] = recipient

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    
    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Send the message via local SMTP server.
    s = smtplib.SMTP(config.email.smtphost)
    if config.email.username:
        s.login(config.email.username, config.email.password)
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(sender, recipient, msg.as_string())
    s.quit()
