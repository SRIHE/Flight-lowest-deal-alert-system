from twilio.rest import Client
import smtplib

account_sid = 'AC0c6f673efc5bcf9eaf764e55fb6b3206'
auth_token = '27635c18c4bf2d48460c6af614ecff4'




class NotificationManager:

    def __init__(self):
        self.client=Client(account_sid,auth_token)
        self.email = "srisri1461@gmail.com"
        self.password = "wchysvzentfxuwif"

    def send_sms(self,message_body):
        message = self.client.messages.create(
            from_='+15754182703',
            to='+918012457421',
            body=message_body
        )

    def send_email(self,message,receiver_email):

        with smtplib.SMTP("smtp.gmail.com",port=587) as self.connection:
            self.connection.starttls()
            self.connection.login(user=self.email,password=self.password)
            self.connection.sendmail(from_addr=self.email,to_addrs=receiver_email,msg=message)