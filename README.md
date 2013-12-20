Requirements
------------

  * plumbum
  * pystache

For tests

  * python-mock

Setup
-----

  * Copy and modify `config/addsite.conf.py`
  * Copy and modify `config/general.conf.py`
  * Copy and modify `config/ldap.conf.py`
  * Copy and modify `config/tls.conf.py`
  * Copy and modify `config/site_nginx.conf.example`
  * Copy and modify one of `config/user.ldif.example-{with,without}-account` to `config.user.ldif`

TODO
----
  PHP
   create fpm pool
   make log dir
   link fpm pool
   restart fpm
