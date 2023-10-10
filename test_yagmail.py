import yagmail

authorization_code = ''

try:
    yag=yagmail.SMTP(user='', password=authorization_code, host='smtp.qq.com')
    yag.send(to='',subject='test',contents='<h1>Hello</h1>')
    print('Email send success')
except:
    print('Email send fail')