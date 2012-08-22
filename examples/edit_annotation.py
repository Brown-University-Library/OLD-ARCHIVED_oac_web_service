#! ~/Envs/oac/bin/jython

import base64
import urllib
import urllib2

pid = 'changeme:401'

put_url = "http://daxdev.services.brown.edu:8081/fedora/objects/%s" % pid
params = { 
    "label" : "mynewlabel"
}
encoded_data = urllib.urlencode( params )
request = urllib2.Request( put_url, encoded_data )
# Authenticate with Fedora credentials
username = ""
password = ""
base64_auth_string = base64.encodestring( '%s:%s' % (username, password) )[:-1]
request.add_header( "Authorization", "Basic %s" % base64_auth_string )
request.get_method = lambda: 'PUT'

response = urllib2.urlopen( request )
print response.read()
