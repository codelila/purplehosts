import subprocess
from email.mime.text import MIMEText

def send(args):
  msg = MIMEText(args['Body'])
  msg['Subject'] = args['Subject']
  msg['From'] = args['From'] ## Default
  msg['To'] = args['To']

  p = subprocess.Popen(['/usr/sbin/sendmail', '-t'], stdin=subprocess.PIPE)
  p.communicate(msg.as_string())
