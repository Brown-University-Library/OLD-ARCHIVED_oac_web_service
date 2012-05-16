import oac_web_service.fedora_settings as config
from oac_web_service.models.foxml import Foxml
from xml.etree import ElementTree as ET
import base64
import urllib2

class Annotation(object):
    def __init__(self, **kwargs):
        self._targets = kwargs.pop('targets')
        self._body_xml = kwargs.pop('body_xml')
        self._dc_title = kwargs.pop('dc_title')
        # Completed by create_body
        self._body_pid = None
        self._body = None
        self._annotation = None
        self._errors = []

    def build_body(self):
        """
        <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
            <rdf:Description rdf:about="info:fedora/test:1000008762">
                <oa:Body xmlns:oa="http://www.w3.org/ns/openannotation/core/" rdf:resource="info:fedora/test:1000008762/datastreams/content/xml"></oa:Body>
                <oa:Annotates xmlns:oa="http://www.w3.org/ns/openannotation/core/" rdf:resource="info:fedora/test:1000006063"></oa:Annotates>
            </rdf:Description>
        </rdf:RDF>
        """
        self._body_pid = self.get_pid()

        rdf = Foxml.get_rdf_body_element(pid=self._body_pid, targets=self._targets)
        dublin_core = Foxml.get_dublin_core_element(pid=self._body_pid, title="Open Annotation Collaboration body object (B-1)")

        foxml = Foxml(pid=self._body_pid)
        # Object Properties
        foxml.create_object_properties()
        # Dublin Core Datastream
        foxml.create_dublin_core_datastream(dublin_core_element=dublin_core)
        # Rels Ext Datastream
        foxml.create_rels_ext_datastream(rdf_element=rdf)

        self._body = foxml.get_foxml()

    def build_annotation(self):
        """
        <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
            <rdf:Description rdf:about="info:fedora/test:1000008729">
                <oa:hasBody xmlns:oa="http://www.w3.org/ns/openannotation/core/" rdf:resource="info:fedora/test:1000008728/datastreams/content/xml"></oa:hasBody>
                <oa:hasTarget xmlns:oa="http://www.w3.org/ns/openannotation/core/" rdf:resource="info:fedora/test:1000006063#xpointer(/TEI%5B1%5D/text%5B1%5D/front%5B1%5D/div%5B1%5D/lg%5B1%5D/lg%5B1%5D)"></oa:hasTarget>
                <oa:Annotation xmlns:oa="http://www.w3.org/ns/openannotation/core/" rdf:resource="info:fedora/test:1000008729"></oa:Annotation>
            </rdf:Description>
        </rdf:RDF>
        """
        self._annotation_pid = self.get_pid()

        rdf = Foxml.get_rdf_annotation_element(pid=self._annotation_pid, body_pid=self._body_pid, targets=self._targets)
        dublin_core = Foxml.get_dublin_core_element(pid=self._annotation_pid, title=self._dc_title)

        foxml = Foxml(pid=self._annotation_pid)
        # Object Properties
        foxml.create_object_properties()
        # Dublin Core Datastream
        foxml.create_dublin_core_datastream(dublin_core_element=dublin_core)
        # Rels Ext Datastream
        foxml.create_rels_ext_datastream(rdf_element=rdf)

        self._annotation = foxml.get_foxml()
        

    def validate(self):
        """
            Validate that the body and annotation objects
            were created in Fedora correctly
        """
        if not len(self._errors) == 0:
            raise AnnotationError(" ".join(self._errors))
        else:
            return True

    def submit(self):
        """
            Send body and annotate objects to Fedora
        """
        if self._body:
            self._body_response = self.post_foxml(element=self._body)

        if self._annotation:
            self._annotation_response = self.post_foxml(element=self._annotation)

    def get_results(self):
        return  {
                    'errors'            : self._errors,
                    'body_pid'          : self._body_response,
                    'annotation_pid'    : self._annotation_response,
                    'targets'           : self._targets
                }
    results = property(get_results, None)

    def post_foxml(self, **kwargs):
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

    def get_pid(self):
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

class AnnotationError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)