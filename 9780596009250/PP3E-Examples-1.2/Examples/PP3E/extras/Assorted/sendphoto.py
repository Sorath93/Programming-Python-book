from email.MIMEMultipart import MIMEMultipart
from email.MIMEImage     import MIMEImage
from email.MIMEText      import MIMEText

mainmsg = MIMEMultipart()
mainmsg['From'] = 'amilleville@opsware.com'
mainmsg['To']   = 'pp3e@earthlink.net'
submsg  = MIMEText('Here you go...')   # text/plain
mainmsg.attach(submsg)

photo  = r'C:\Mark\nycphotos\109_0312.JPG'
data   = open(photo, 'rb')
submsg = MIMEImage(data.read(), _subtype='jpeg')   # image/jpeg
submsg.add_header('Content-Disposition',
                  'attachment', filename='109_0312.JPG')
mainmsg.attach(submsg) 
fulltext = mainmsg.as_string()

import smtplib
srvr = smtplib.SMTP('mayhem.opsware.com')
srvr.sendmail('amilleville@opsware.com', ['pp3e@earthlink.net'], fulltext)
srvr.close()
