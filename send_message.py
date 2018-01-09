# -*- coding: utf-8 -*-
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

import conf

you = 'To: ' + ', '.join(conf.toaddr)
msg = MIMEMultipart('mixed')
msg['Subject'] = 'Find consignors'
msg['From'] = conf.me
#msg['To'] = ', '.join(conf.toaddr[0:4])
#msg['cc'] = ', '.join([ conf.toaddr[4] ])
msg['To'] = ', '.join(conf.test_toaddr[0:2])
# Genering E-mail
puth = 'report.xlsx'
try:
	fo = open(puth, 'rb')
	filecontent = fo.read()
	fo.close()
	part2 = MIMEApplication(filecontent, 'application/xls;name="report.xlsx"')

except:
	print('good')

msg.attach(conf.part1_failure)
#msg.attach(part2)
msg.attach(conf.part3)

# Connecting
s = smtplib.SMTP(conf.server, conf.port)
s.ehlo()
s.starttls()
s.ehlo()
# Autorization
s.login(conf.user_name, conf.user_passwd)
# Send message
s.sendmail(conf.me, conf.toaddr, msg.as_string())
s.quit()
