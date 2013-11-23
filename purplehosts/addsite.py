import os.path
from string import Template

from plumbum.cmd import adduser, echo, ln, nginx
from pystache import Renderer

renderer = Renderer(missing_tags='strict')

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
  import purplehosts.tls
  from purplehosts.utils import getHost, getDomain

  substitutes = reduce(_parseArg, args.additional_args, {
    'fqdn': args.domain,
    'host': getHost(args.domain),
    'domain': getDomain(args.domain),
    'tls_paths': {'crt': 'crt', 'csr': 'csr', 'key': 'key'}
  })

  username = username_tpl.substitute(substitutes)
  substitutes['username'] = username
  # Test nginx conf tpl before doing anything
  nginx_conf = renderer.render(nginx_conf_tpl, substitutes)
  nginx_conf_filename = nginx_conf_filename_tpl.substitute(substitutes)

  # Start doing things
  substitutes['tls_paths'] = purplehosts.tls.TLS(args.domain).make()
  # Rerender nginx conf with actual tls paths
  nginx_conf = renderer.render(nginx_conf_tpl, substitutes)
  adduser['--system'](username)
  (echo << nginx_conf > nginx_conf_filename)()

  ln['-s'](os.path.relpath(nginx_conf_filename, '/etc/nginx/sites-enabled/'), '/etc/nginx/sites-enabled/')
  nginx('-t')

