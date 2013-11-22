from purplehosts import passwd, ldap, config, mail

def run(args):
  conf = config.get('general')

  pw = passwd.generate()
  mailAddress = args.mailaddress

  ldap.add({
    'username': args.username,
    'givenname': args.givenname,
    'surname': args.surname,
    'password': pw,
    'usernumber': str(ldap.nextUid()),
    'groupnumber': str(conf['gid']),
    'mailaddress': mailAddress
  })

  mail.send({
    'Subject': 'Account auf ' + conf['domain'],
    'To': mailAddress,
    'From': "{0} <root@{0}>".format(conf['domain']),
    'Body': """Hallo {0},

  Dein Account {1} auf {2} wurde angelegt.

  Dein Passwort: {3}

  Viel Spass,
  {2}""".format(args.givenname, args.username, conf['domain'], pw)
  })
