import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_notification():
    message = Mail(
        from_email=os.environ.get('WEBSITE_EMAIL'),
        to_emails=os.environ.get('WEBSITE_EMAIL'),
        subject='Your move pal',
        html_content="<p>Someone's made a move</p>"
    )

    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)

