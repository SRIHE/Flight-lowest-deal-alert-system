from twilio.rest import Client
import smtplib

account_sid = 'PUT YOUR ID HERE'
auth_token = 'PUT YOUR ID HERE'




class NotificationManager:

    def __init__(self):
        self.client=Client(account_sid,auth_token)
        self.email = "MAIL ID"
        self.password = "PASSWORD"

    def send_sms(self,message_body):
        message = self.client.messages.create(
            from_='+15754182703',
            to='+YOUR NUMBER',
            body=message_body
        )

    def send_email(self,message,receiver_email):

        with smtplib.SMTP("smtp.gmail.com",port=587) as self.connection:
            self.connection.starttls()
            self.connection.login(user=self.email,password=self.password)
            self.connection.sendmail(from_addr=self.email,to_addrs=receiver_email,msg=message)
