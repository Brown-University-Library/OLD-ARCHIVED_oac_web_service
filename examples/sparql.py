#! ~/Envs/oac/bin/jython

import urllib
import urllib2
import httplib2
httplib2.debuglevel=5

url = "http://daxdev.services.brown.edu:8081/oac_web_service/sparql"

"""
"SELECT (count(*) AS ?count) { ?s ?p ?o }"
"SELECT * { ?s ?p ?o }"
"""
query = "SELECT * { ?s ?p ?o }"

params = { 'query' : query }
encoded_data = urllib.urlencode( params )

# urllib2 POST
request = urllib2.Request( url, encoded_data )
response = urllib2.urlopen( request )
print response.read()

# urllib2 GET
request = urllib2.Request( url + "?" + encoded_data)
response = urllib2.urlopen( request )
print response.read()

# httplib2 POST
h = httplib2.Http()

headers = {'Content-type': 'application/x-www-form-urlencoded'}
resp, content = h.request(url, "POST", headers=headers, body=encoded_data)
print content

# httplib2 GET
resp, content = h.request(url + "?" + encoded_data, "GET")
print content



