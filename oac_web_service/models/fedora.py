import csv
import base64
import urllib2, urllib
from oac_web_service import app
from xml.etree import ElementTree as ET

username = app.config['FEDORA_USER']
password = app.config['FEDORA_PASS']

class Fedora(object):

    @classmethod
    def post_foxml(cls, **kwargs):
        """
            Post FOXML to the fedora repository, thus creating a new object
        """
        try:
            url = app.config['FEDORA_INGEST_URL']
            data = ET.tostring(kwargs.pop('element'))

            request = urllib2.Request( url, data )

            base64_auth_string = base64.encodestring( '%s:%s' % (username, password) )[:-1]
            request.add_header( "Authorization", "Basic %s" % base64_auth_string )
            request.add_header( "Content-type", "text/xml" )
            response = urllib2.urlopen( request )
            return response.read()

        except urllib2.HTTPError, e:
            if e.code == 201:
                return e.read()
            else:
                return False

        except urllib2.URLError, e:
            return False

    @classmethod
    def put_datastream(cls, **kwargs):
        """
            Put an XML datastream object to the fedora repository, thus editing it
        """

        pid = kwargs.pop('pid')
        dsid = kwargs.pop('dsid')

        try:
            url = app.config['FEDORA_DATASTREAM_URL'].replace('{pid}', pid).replace('{dsid}', dsid)
            data = ET.tostring(kwargs.pop('element'))

            request = urllib2.Request( url, data )

            base64_auth_string = base64.encodestring( '%s:%s' % (username, password) )[:-1]
            request.add_header( "Authorization", "Basic %s" % base64_auth_string )
            request.add_header( "Content-type", "text/xml" )
            request.get_method = lambda: 'PUT'
            response = urllib2.urlopen( request )
            return response.read()

        except urllib2.HTTPError, e:
            if e.code == 200:
                return e.read()
            else:
                return False

        except urllib2.URLError, e:
            return False

    @classmethod
    def get_datastream(cls, pid, dsid):
        """
            Get a datastreams XML representation
        """
        try: 
            url = app.config['FEDORA_GET_DATASTREAM_URL'].replace('{pid}', pid).replace('{dsid}', dsid)

            request = urllib2.Request( url )

            base64_auth_string = base64.encodestring( '%s:%s' % (username, password) )[:-1]
            request.add_header( "Authorization", "Basic %s" % base64_auth_string )
            response = urllib2.urlopen( request )

            # Parse out and return Datastream XML
            return ET.fromstring(response.read())

        except urllib2.HTTPError, e:
            if e.code == 404:
                return "No object with the PID %s and DSID %s" % (pid, dsid)
            else:
                return e.read()

    @classmethod
    def get_datastream_list(cls, pid):
        """
            Get a list of datastream IDs from a PID
        """
        try:
            url = app.config['FEDORA_LIST_DATASTREAMS_URL'].replace('{pid}', pid)
            url += "?format=xml"

            request = urllib2.Request( url )

            base64_auth_string = base64.encodestring( '%s:%s' % (username, password) )[:-1]
            request.add_header( "Authorization", "Basic %s" % base64_auth_string )
            response = urllib2.urlopen( request )

            # Parse out and return Datastream IDs
            element = ET.fromstring(response.read())
            return [e.get('dsid') for e in element.findall('{http://www.fedora.info/definitions/1/0/access/}datastream')]

        except urllib2.HTTPError, e:
            if e.code == 404:
                return "No object with the PID %s" % pid
            else:
                return e.read()

    @classmethod
    def get_sparql_query_resuts(cls, query):
        url = app.config['FEDORA_SPARQL_QUERY_URL']
        params = { 
          "dt"            : "on",
          "format"        : "CSV",
          "lang"          : "sparql",
          "query"         : query,
          "type"          : "tuples"
        }
        encoded_data = urllib.urlencode( params )
        request = urllib2.Request( url, encoded_data )

        base64_auth_string = base64.encodestring( '%s:%s' % (username, password) )[:-1]
        request.add_header( "Authorization", "Basic %s" % base64_auth_string )
        response = urllib2.urlopen( request )
        csv_response = response.read()
        for row in csv_response.split('\n'):
            if row != None and row != "\"s\"" and row.strip() != "":
                yield row

    @classmethod
    def get_pid(cls):
        """
            Query the Fedora system for a PID
        """
        url = app.config['FEDORA_PID_URL']

        # For some strange reason, the format needs to be on the URL even though this
        # is a POST request.  Could be a bug in Fedora 3.5.
        url += "?format=xml"

        params = { 
          "format"  : "xml"
        }
        encoded_data = urllib.urlencode( params )
        request = urllib2.Request( url, encoded_data )

        base64_auth_string = base64.encodestring( '%s:%s' % (username, password) )[:-1]
        request.add_header( "Authorization", "Basic %s" % base64_auth_string )
        response = urllib2.urlopen( request )
        element = ET.fromstring(response.read())
        return element.find('{http://www.fedora.info/definitions/1/0/management/}pid').text

    @classmethod
    def get_content_models(cls, pid):
        """
            Query the Fedora system for an objects XML and pull out the content model strings
        """
        url = app.config['FEDORA_OBJECT_PID_URL'].replace('{pid}', pid)
        url += "?format=xml"

        request = urllib2.Request( url )

        base64_auth_string = base64.encodestring( '%s:%s' % (username, password) )[:-1]
        request.add_header( "Authorization", "Basic %s" % base64_auth_string )
        response = urllib2.urlopen( request )

        element = ET.fromstring(response.read())
        access_ns = "http://www.fedora.info/definitions/1/0/access/"

        return [e.text for e in element.findall('{%s}objModels/{%s}model' % (access_ns, access_ns) )]
    