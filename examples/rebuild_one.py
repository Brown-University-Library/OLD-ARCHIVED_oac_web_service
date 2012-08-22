#! ~/Envs/oac/bin/jython

import base64
import urllib
import urllib2
post_url = "http://daxdev.services.brown.edu:8081/oac_web_service/rebuild_one"
params = { 
  "pid" : "changeme:308",
}
encoded_data = urllib.urlencode( params )
request = urllib2.Request( post_url, encoded_data )
response = urllib2.urlopen( request )

print response.read()
