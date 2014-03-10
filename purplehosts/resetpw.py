# coding=utf-8
from purplehosts import passwd, ldap, config, mail

def run(args):
  conf = config.get('general')
  ldapConf = config.get('ldap')

  new_pw = passwd.generate()
  user_name = args.username

  # FIXME This is configuration
  cn = "cn=" + user_name
  dn = cn + "," + ldapConf['people_root'].value()
  user = ldap.getUser(cn)
  ldap.modify("dn: " + dn + "\n" +
    "changetype: modify\n" +
    "replace: userPassword\n"
    "userPassword: " + new_pw)

  mail.send({
    'Subject': 'Passwort für ' + conf['domain'].value(),
    'To': user['mail'][0],
    'From': "{0} <root@{0}>".format(conf['domain'].value()),
    'Body': """Hallo {0},

  Das Passwort für deinen Account {1} auf {2} wurde zurückgesetzt.

  Dein neues Passwort: {3}

  Viel Spass,
  {2}""".format(user['givenName'][0], args.username, conf['domain'].value(), new_pw)
  })
