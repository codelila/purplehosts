from plumbum import FG
from plumbum.cmd import sendmail
from email.mime.text import MIMEText

def send(args):
  msg = MIMEText(args['Body'])
  msg['Subject'] = args['Subject']
  msg['From'] = args['From'] ## Default
  msg['To'] = args['To']

  (sendmail['-t'] << msg.as_string())()
