import oac_web_service.fedora_settings as config
from xml.etree import ElementTree as ET
import base64
import urllib2

class Annotation(object):
    def __init__(self, **kwargs):
        self._target_pid = kwargs.pop('target_pid')
        self._target_uri = kwargs.pop('target_uri')
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
                <oac:Body xmlns:oac="http://www.openannotation.org/ns/" rdf:resource="info:fedora/test:1000008762/datastreams/content/xml"></oac:Body>
                <oac:Annotates xmlns:oac="http://www.openannotation.org/ns/" rdf:resource="info:fedora/test:1000006063"></oac:Annotates>
            </rdf:Description>
        </rdf:RDF>
        """
        self._body_pid = get_pid()

        rdf = Foxml.get_rdf_body_element(pid=self._body_pid, target_pid=self._target_pid)
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
                <oac:hasBody xmlns:oac="http://www.openannotation.org/ns/" rdf:resource="info:fedora/test:1000008728/datastreams/content/xml"></oac:hasBody>
                <oac:hasTarget xmlns:oac="http://www.openannotation.org/ns/" rdf:resource="info:fedora/test:1000006063#xpointer(/TEI%5B1%5D/text%5B1%5D/front%5B1%5D/div%5B1%5D/lg%5B1%5D/lg%5B1%5D)"></oac:hasTarget>
                <oac:Annotation xmlns:oac="http://www.openannotation.org/ns/" rdf:resource="info:fedora/test:1000008729"></oac:Annotation>
            </rdf:Description>
        </rdf:RDF>
        """
        self._annotation_pid = get_pid()

        rdf = Foxml.get_rdf_annotation_element(pid=self._annotation_pid, body_pid=self._body_pid, target_uri=self._target_uri)
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
        return len(self._errors == 0)

    def submit(self):
        """
            Send body and annotate objects to Fedora
        """
        if self._body:
            response = post_foxml(element=self._body)

        if self._annotation:
            response = post_foxml(element=self._annotation)

    def post_foxml(self, **kwargs):
        """
            Post FOXML to the fedora repository, thus creating a new object
        """
        username = config.FEDORA_USER
        password = config.FEDORA_PASS
        url = config.FEDORA_INGEST_URL
        data = ET.tostring(kwargs.pop('element'))

        request = urllib2.Request( url, data )

        base64_auth_string = base64.encodestring( '%s:%s' % (username, password) )[:-1]
        request.add_header( "Authorization", "Basic %s" % base64_auth_string )
        request.add_header( "Content-type", "text/xml" )
        response = urllib2.urlopen( request ).read()
        return response

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