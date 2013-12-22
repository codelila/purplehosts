from purplehosts.actionbundle import ActionBundle

import purplehosts.config
conf = purplehosts.config.get('addsite')

username_tpl = conf['system_user_name_template']
nginx_conf_tpl = purplehosts.config.valFromDef(('site_nginx.conf', 'File', 'MustacheTemplate'))
nginx_conf_filename_tpl = conf['nginx_conf_filename_template']

def _parseArg(sub_dict, arg):
  (argname, _, argval) = arg.partition('=')
  if argval == '':
    argval = True
  elif argval in ('false', 'no'):
    argval = False
  sub_dict[argname] = argval
  return sub_dict

def run(args):
  # Parse args
  from purplehosts.utils import getHost, getDomain
  substitutes = reduce(_parseArg, args.additional_args, {
    'fqdn': args.domain,
    'host': getHost(args.domain),
    'domain': getDomain(args.domain)
  })

  # Create actions list
  from purplehosts.action.createtlscert import CreateTLSCert
  from purplehosts.action.addnginxsite import AddNginxSite

  actions = [
    CreateTLSCert(),
    AddNginxSite(conf_template = nginx_conf_tpl, filename_template = nginx_conf_filename_tpl)
  ]

  # Crude hack: Do not add a new account if username is passed as arg
  if not 'username' in substitutes or not substitutes['username']:
    from purplehosts.action.addposixaccount import AddPosixAccount
    actions.insert(0, AddPosixAccount(username_template = username_tpl))

  actionbundle = ActionBundle(actions)

  # Prepare actions
  actionbundle.prepare(substitutes)

  # Execute actions
  actionbundle.execute()
