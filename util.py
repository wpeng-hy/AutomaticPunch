import requests
from PIL import Image, ImageDraw, ImageFont
import base64
import smtplib
from email.mime.text import MIMEText
from email.header import Header


# 图片加水印
def water_mark(day, ms, address):
    ttf = 'DroidSansFallback-Regular.ttf'
    # t = time.localtime()
    # print(time)
    # d = str('%02d' % t.tm_hour) + ':' + str('%02d' % t.tm_min) + ':' + str('%02d' % t.tm_sec)
    # y = str(t.tm_year) + "-" + str('%02d' % t.tm_mon) + "-" + str('%02d' % t.tm_mday)
    # d = "15:39:00"
    img = Image.open("./img/wpeng.jpg")
    draw = ImageDraw.Draw(img, "RGBA")
    # 设置字体
    font = ImageFont.truetype(ttf, 14)
    shape = [(10, 10), (10, 80)]
    # 添加水印文字
    draw.line(shape, fill='white', width=6)
    draw.text((18, 15), ms, font=ImageFont.truetype(ttf, 22))
    draw.text((122, 21), day, font=font)
    icon = Image.open("./img/new_icon.png")
    # new_icon = icon.resize((icon.width // 5, icon.height // 5))
    # new_icon = new_icon.save('./img/new_icon.png')
    r, g, b, a = icon.split()
    img.paste(icon, (18, 50), mask=a)
    draw.text((icon.width + 20, 52), address, font=font)
    draw.text((1180, 20), "1151610", font=font)
    # img.show()
    img.save('./img/temp_watermark.jpg')
    return imgToBase64()


def imgToBase64():
    img = open("./img/temp_watermark.jpg", 'rb')
    res = base64.b64encode(img.read())
    img.close()
    return str(res, 'UTF-8')


# day = '2022-05-02'
# ms = '14:25:00'
# address = '浙江省杭州市西湖区蒋村街道文一西路757正绿城西溪国际'
# water_mark(day, ms, address)
#
# icon = Image.open('./img/icon.png')
# new_icon = icon.resize((icon.width // 10, icon.height // 10))
# new_icon = new_icon.save('./img/new_icon.png')


def holiday(date):
    url = 'https://api.apihubs.cn/holiday/get?field=workday,holiday,date&date={}&cn=1&size=31'
    params = {
        'field': 'workday,holiday,date',
        'date': date,
        'cn': '1',
        'size': '31'
    }
    res = requests.get(url, params=params)
    data = res.json()['data']['list'][0]['workday_cn']
    print(data)
    return data

# holiday('20220502')


def send_email(msg, email_addr):
    mail_host = 'smtp.qq.com'
    mail_user = '314093315@qq.com'
    mail_pass = 'vwwccxebrlqrbgeb'

    sender = '314093315@qq.com'
    receivers = {email_addr}

    message = MIMEText(msg, 'plain', 'utf-8')
    # message['From'] = Header("314093315")
    # message['To'] = Header("wpeng")

    subject = "自动打卡"
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP()
        # 25 为 SMTP 端口号
        smtpObj.connect(mail_host, 25)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("发送邮件异常")


# send_email("测试")
