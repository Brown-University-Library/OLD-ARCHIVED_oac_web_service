import base64
import urllib2
from oac_web_service import fedora_settings as config
from xml.etree import ElementTree as ET


class Fedora(object):

    @classmethod
    def post_foxml(cls, **kwargs):
        """
            Post FOXML to the fedora repository, thus creating a new object
        """
        try:
            username = config.FEDORA_USER
            password = config.FEDORA_PASS
            url = config.FEDORA_INGEST_URL
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
                self._errors.append(e.read())
                return False

        except urllib2.URLError, e:
            self._errors.append(e.reason)
            return False

    @classmethod
    def get_pid(cls):
        """
            Query the Fedora system for a PID
        """
        username = config.FEDORA_USER
        password = config.FEDORA_PASS
        url = config.FEDORA_PID_URL

        request = urllib2.Request( url )

        base64_auth_string = base64.encodestring( '%s:%s' % (username, password) )[:-1]
        request.add_header( "Authorization", "Basic %s" % base64_auth_string )
        request.add_header( "Content-type", "text/xml" )
        response = urllib2.urlopen( request )
        element = ET.fromstring(response.read())
        return element.find('pid').text