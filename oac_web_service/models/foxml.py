from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element

class Foxml(object):

    FOXMLNS = "info:fedora/fedora-system:def/foxml#"
    ET._namespace_map[FOXMLNS] = 'foxml'

    RDFNS = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    ET._namespace_map[RDFNS] = 'rdf'
    
    OANS = "http://www.w3.org/ns/openannotation/core/"
    ET._namespace_map[OANS] = 'oa'

    OAI_DC_NS = "http://www.openarchives.org/OAI/2.0/oai_dc/"
    ET._namespace_map[OAI_DC_NS] = 'oai_dc'

    DC_NS = "http://purl.org/dc/elements/1.1/"
    ET._namespace_map[DC_NS] = 'dc'

    STATE_INFO_URI = "info:fedora/fedora-system:def/model#state"
    LABEL_INFO_URI = "info:fedora/fedora-system:def/model#label"
    OAIDC_INFO_URI = "http://www.openarchives.org/OAI/2.0/oai_dc/"
    RELSEXT_INFO_URI = "info:fedora/fedora-system:FedoraRELSExt-1.0";

    def __init__(self, **kwargs):
        self._doc = Element("{%s}digitalObject" % self.FOXMLNS)
        self._doc.set('VERSION', '1.1')
        self._doc.set('PID', kwargs.pop('pid'))
       
    def create_object_properties(self):
        self._doc.append(Foxml.get_object_properties())
    def create_dublin_core_datastream(self, **kwargs):
        self._doc.append(Foxml.get_dublin_core_datastream(**kwargs))
    def create_rels_ext_datastream(self, **kwargs):
        self._doc.append(Foxml.get_rels_ext_datastream(**kwargs))
    def get_foxml(self):
        return self._doc

    @classmethod
    def get_object_properties(cls):
        """
        <foxml:objectProperties>
            <foxml:property NAME="info:fedora/fedora-system:def/model#state" VALUE="A" />
            <foxml:property NAME="info:fedora/fedora-system:def/model#label" VALUE="OAC object" />
        </foxml:objectProperties>
        """
        stateProperty = Element("{%s}property" % cls.FOXMLNS);
        stateProperty.set("NAME", cls.STATE_INFO_URI);
        stateProperty.set("VALUE", "A");

        labelProperty = Element("{%s}property" % cls.FOXMLNS); 
        labelProperty.set("NAME", cls.LABEL_INFO_URI);
        labelProperty.set("VALUE", "OAC object");      
               
        objectProperties = Element("{%s}objectProperties" % cls.FOXMLNS) 
        objectProperties.append(stateProperty);
        objectProperties.append(labelProperty);
        
        return objectProperties;

    @classmethod
    def get_rdf_body_element(cls, **kwargs):
        """
        <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
            <rdf:Description rdf:about="info:fedora/test:1000008762">
                <oa:Body xmlns:oa="http://www.w3.org/ns/openannotation/core/" rdf:resource="info:fedora/test:1000008762/datastreams/content/xml"></oa:Body>
                <oa:Annotates xmlns:oa="http://www.w3.org/ns/openannotation/core/" rdf:resource="info:fedora/test:1000006063"></oa:Annotates>
            </rdf:Description>
        </rdf:RDF>
        """
        pid = kwargs.pop('pid')
        target_pid = kwargs.pop('target_pid')

        body = Element("{%s}Body" % cls.OANS)
        body.set("{%s}resource" % cls.RDFNS, "info:fedora/" + pid + "/datastreams/OAC_BODY/content")

        annotates = Element("{%s}Annotates" % cls.OANS)
        annotates.set("{%s}resource" % cls.RDFNS, "info:fedora/" + target_pid)

        descrip = Element("{%s}Description" % cls.RDFNS)
        descrip.set("{%s}about" % cls.RDFNS, "info:fedora/" + pid)
        descrip.append(body)
        descrip.append(annotates)

        rdf = Element("{%s}RDF" % cls.RDFNS)
        rdf.append(descrip)

        return rdf

    @classmethod
    def get_rdf_annotation_element(cls, **kwargs):
        """
        <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
            <rdf:Description rdf:about="info:fedora/test:1000008729">
                <oa:hasBody xmlns:oa="http://www.w3.org/ns/openannotation/core/" rdf:resource="info:fedora/test:1000008728/datastreams/content/xml"></oa:hasBody>
                <oa:hasTarget xmlns:oa="http://www.w3.org/ns/openannotation/core/" rdf:resource="info:fedora/test:1000006063#xpointer(/TEI%5B1%5D/text%5B1%5D/front%5B1%5D/div%5B1%5D/lg%5B1%5D/lg%5B1%5D)"></oa:hasTarget>
                <oa:Annotation xmlns:oa="http://www.w3.org/ns/openannotation/core/" rdf:resource="info:fedora/test:1000008729"></oa:Annotation>
            </rdf:Description>
        </rdf:RDF>
        """
        pid = kwargs.pop('pid')
        body_pid = kwargs.pop('body_pid')
        target_uri = kwargs.pop('target_uri')

        body = Element("{%s}hasBody" % cls.OANS)
        body.set("{%s}resource" % cls.RDFNS, "info:fedora/" + body_pid + "/datastreams/OAC_BODY/content")

        target = Element("{%s}hasTarget" % cls.OANS)
        target.set("{%s}resource" % cls.RDFNS, "info:fedora/" + target_uri)

        annotation = Element("{%s}Annotation" % cls.OANS)
        annotation.set("{%s}resource" % cls.RDFNS, "info:fedora/" + pid)

        descrip = Element("{%s}Description" % cls.RDFNS)
        descrip.set("{%s}about" % cls.RDFNS, "info:fedora/" + pid)
        descrip.append(body)
        descrip.append(target)
        descrip.append(annotation)

        rdf = Element("{%s}RDF" % cls.RDFNS)
        rdf.append(descrip)

        return rdf

    @classmethod
    def get_dublin_core_element(cls, **kwargs):
        """
        <oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/">
            <dc:title xmlns:dc="http://purl.org/dc/elements/1.1/">
                super!
            </dc:title>
            <dc:identifier xmlns:dc="http://purl.org/dc/elements/1.1/">
                1
            </dc:identifier>
        </oai_dc:dc>
        """
        title = Element("{%s}title" % cls.DC_NS)
        title.text = kwargs.pop('title')

        identifier = Element("{%s}identifier" % cls.DC_NS)
        identifier.text = kwargs.pop('pid')

        oai_dc = Element("{%s}dc" % cls.OAI_DC_NS)
        oai_dc.append(title)
        oai_dc.append(identifier)
        return oai_dc

    @classmethod
    def get_datastream_element(cls, **kwargs):
        datastream = Element("{%s}datastream" % cls.FOXMLNS)
        datastream.set("ID", kwargs.pop('id'))
        datastream.set("STATE", kwargs.pop('state'))
        datastream.set("CONTROL_GROUP", kwargs.pop('control_group'))    
        return datastream

    @classmethod
    def get_datastream_version_element(cls, **kwargs):
        """
        <foxml:datastreamVersion ID="RELS-EXT.0" LABEL="RDF Statements about this object" MIMETYPE="application/rdf+xml" xmlns:foxml="info:fedora/fedora-system:def/foxml#" />
        """
        datastreamVersion = Element("{%s}datastreamVersion" % cls.FOXMLNS)
        datastreamVersion.set("ID", kwargs.pop('id'));
        datastreamVersion.set("MIMETYPE", kwargs.pop('mime'));
        datastreamVersion.set("LABEL", kwargs.pop('label'));
        if kwargs.get('format_uri'):
            datastreamVersion.set("FORMAT_URI", kwargs.pop('format_uri'));
        return datastreamVersion

    @classmethod
    def get_xml_content_element(cls):
        """
        <foxml:xmlContent xmlns:foxml="info:fedora/fedora-system:def/foxml#" />
        """
        return Element("{%s}xmlContent" % cls.FOXMLNS)

    @classmethod
    def get_dublin_core_datastream(cls, **kwargs):
        xml_content = Foxml.get_xml_content_element()
        xml_content.append(kwargs.pop('dublin_core_element'))

        datastream_version = Foxml.get_datastream_version_element(format_uri=cls.OAIDC_INFO_URI, id="DC.0", mime="text/xml", label="Dublin Core Record for this object")
        datastream_version.append(xml_content)

        datastream = Foxml.get_datastream_element(id="DC", state="A", control_group="M")
        datastream.append(datastream_version)
        return datastream

    @classmethod
    def get_rels_ext_datastream(cls, **kwargs):
        xml_content = Foxml.get_xml_content_element()
        xml_content.append(kwargs.pop('rdf_element'))

        datastream_version = Foxml.get_datastream_version_element(format_uri=cls.RELSEXT_INFO_URI, id="RELS-EXT.0", mime="application/rdf+xml", label="RDF Statements about this object")
        datastream_version.append(xml_content)

        datastream = Foxml.get_datastream_element(id="RELS-EXT", state="A", control_group="M")
        datastream.append(datastream_version)
        return datastream