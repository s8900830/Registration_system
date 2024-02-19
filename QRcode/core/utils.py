import random
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

class mainfunction:

    def code(num):
        to62list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                    'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                    'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D',
                    'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                    'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        test = random.choices(to62list, k=num)

        return ''.join(test)


if __name__ == "__main__":
    print(mainfunction.code(10))


class email:
    def send_email(send_user_email,user_name,QRcode,message):
        if send_user_email or user_name is None:
            subject = 'Registration System'

            email_template = render_to_string('email_template.html', {
                'user_name':user_name,
                'QRcode':QRcode,
                'context': message}
                )
            
            email = EmailMessage(
                    subject,  # 電子郵件標題
                    email_template,  # 電子郵件內容
                    settings.EMAIL_HOST_USER,  # 寄件者
                    [send_user_email]  # 收件者
                )
            email.fail_silently = False
            email.send()
            return 'success'
        else:
            return 'error'