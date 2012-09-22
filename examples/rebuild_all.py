#! ~/Envs/oac/bin/jython

import base64
import urllib
import urllib2

get_url = "http://daxdev.services.brown.edu:8081/oac_web_service/rebuild_all"

request = urllib2.Request( get_url )
# Authenticate with OAC credentials (defined in the OAC configuration file)
username = ""
password = ""
base64_auth_string = base64.encodestring( '%s:%s' % (username, password) )[:-1]
request.add_header( "Authorization", "Basic %s" % base64_auth_string )
response = urllib2.urlopen( request )

print response.read()

