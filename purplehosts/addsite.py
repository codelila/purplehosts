from string import Template

from purplehosts.argdict import ArgDict

import purplehosts.config
conf = purplehosts.config.get('addsite')

username_tpl = Template(conf['system_user_name_template'])
nginx_conf_tpl = purplehosts.config.getFile('site_nginx.conf')
nginx_conf_filename_tpl = Template(conf['nginx_conf_filename_template'])

def _parseArg(sub_dict, arg):
  (argname, _, argval) = arg.partition('=')
  if argval == '':
    argval = True
  elif argval in ('false', 'no'):
    argval = False
  sub_dict[argname] = argval
  return sub_dict

def run(args):
  from purplehosts.utils import getHost, getDomain

  actions = []

  substitutes = ArgDict()
  substitutes.update({
    'fqdn': args.domain,
    'host': getHost(args.domain),
    'domain': getDomain(args.domain)
  })
  substitutes = reduce(_parseArg, args.additional_args, substitutes)

  # Crude hack: Do not add a new account if username is passed as arg
  if not 'username' in substitutes or not substitutes['username']:
    from purplehosts.action.addposixaccount import AddPosixAccount
    actions.append(AddPosixAccount(username_template = username_tpl))

  from purplehosts.action.createtlscert import CreateTLSCert
  actions.append(CreateTLSCert(args.domain))

  from purplehosts.action.addnginxsite import AddNginxSite
  actions.append(AddNginxSite(conf_template = nginx_conf_tpl, filename_template = nginx_conf_filename_tpl))

  # Add placeholders so that depending prepares work
  provided = []
  for action in actions:
    provided.extend(action.provides)
  substitutes.start_testing(provided)

  # Testing prepares
  for action in actions:
    new_subs = action.prepare(substitutes)
    for k in action.provides:
      substitutes[k] = new_subs[k]

  # Running prepares
  substitutes.start_preparing()
  for action in actions:
    new_subs = action.prepare(substitutes)
    for k in action.provides:
      substitutes[k] = new_subs[k]

  # Start doing things
  for action in actions:
    action.execute()
