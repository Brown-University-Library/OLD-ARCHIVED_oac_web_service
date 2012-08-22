#! ~/Envs/oac/bin/jython

import base64
import urllib
import urllib2
post_url = "http://daxdev.services.brown.edu:8081/oac_web_service/create"
params = { 
  "pid" : "changeme:308",
}
encoded_data = urllib.urlencode( params )
request = urllib2.Request( post_url, encoded_data )
# Authenticate with Fedora credentials
username = ""
password = ""
base64_auth_string = base64.encodestring( '%s:%s' % (username, password) )[:-1]
request.add_header( "Authorization", "Basic %s" % base64_auth_string )

response = urllib2.urlopen( request )
print response.read()
