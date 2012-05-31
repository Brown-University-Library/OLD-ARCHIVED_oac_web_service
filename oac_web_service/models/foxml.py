from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element
from datetime import datetime
import pytz

class Foxml(object):

    FOXMLNS = "info:fedora/fedora-system:def/foxml#"
    ET._namespace_map[FOXMLNS] = 'foxml'

    RDFNS = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    ET._namespace_map[RDFNS] = 'rdf'
    
    OANS = "http://www.w3.org/ns/openannotation/core/"
    ET._namespace_map[OANS] = 'oa'

    OAXNS = "http://www.w3.org/ns/openannotation/extension/"
    ET._namespace_map[OANS] = 'oax'

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
        self._doc.set('PID', kwargs.get('pid'))
        self._doc.set('FEDORA_URI', "info:fedora/%s" % kwargs.get('pid'))
       
    def create_object_properties(self):
        self._doc.append(Foxml.get_object_properties())
    def create_dublin_core_datastream(self, **kwargs):
        self._doc.append(Foxml.get_dublin_core_datastream(**kwargs))
    def create_annotation_datastream(self, **kwargs):
        self._doc.append(Foxml.get_annotation_datastream(**kwargs))
    def create_rels_ext_datastream(self, **kwargs):
        self._doc.append(Foxml.get_rels_ext_datastream(**kwargs))
    def create_specific_target_datastream(self, **kwargs):
        self._doc.append(Foxml.get_specific_target_datastream(**kwargs))
    def create_selector_datastream(self, **kwargs):
        self._doc.append(Foxml.get_selector_datastream(**kwargs))
    def create_body_content_datastream(self, **kwargs):
        # TODO: We need to support content types other than XML here.
        self._doc.append(Foxml.get_xml_body_content_datastream(**kwargs))
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
    def get_annotation_rdf_element(cls, **kwargs):
        """
        <rdf:RDF>
          <rdf:Description rdf:about="info:fedora/{{ANNO1_PID}}">
            <rdf:type rdf:resource="oa:Annotation"/>
            <oa:hasBody rdf:resource="{{body_uri}}"/>
            <!-- if a oa_selector is passed as a parameter, include: -->
            <oa:hasTarget rdf:resource="info:fedora/{{ANNO1_PID}}/SpecificTarget"/>
            <!-- Always include: -->
            <oa:modelVersion rdf:resource="http://www.openannotation.org/spec/core/20120509.html"/>
          </rdf:Description>
          <rdf:Description rdf:about="info:fedora/{{ANNO1_PID}}">
            <rdf:type rdf:resource="oa:Body"/>
            <dc:format>{{body_content_mimetype}}</dc:format>
          </rdf:Description>
        </rdf:RDF>
        """
        # Required fields
        annotation_pid = kwargs.pop('pid')
        body_uri = kwargs.pop('body_uri')

        # Optional fields
        oa_selector = kwargs.pop('oa_selector', None)
        # TODO: If we didn't create a new BODY (B-1) object, how do we know the 
        # content type here?  We would need to query the existing BODY object before
        # calling this function
        body_content_mimetype = kwargs.pop('body_mimetype', None)

        # RDF oa:Annotation Description Element
        descrip_annotation = Element("{%s}Description" % cls.RDFNS)
        descrip_annotation.set("{%s}about" % cls.RDFNS, "info:fedora/" + annotation_pid)

        annotation_type = Element("{%s}type" % cls.RDFNS)
        annotation_type.set("{%s}resource" % cls.RDFNS, "oa:Annotation")
        descrip_annotation.append(annotation_type)

        body = Element("{%s}hasBody" % cls.OANS)
        body.set("{%s}resource" % cls.RDFNS, body_uri)
        descrip_annotation.append(body)

        mv = Element("{%s}modelVersion" % cls.OANS)
        mv.set("{%s}resource" % cls.RDFNS, "http://www.openannotation.org/spec/core/20120509.html")
        descrip_annotation.append(mv)

        if oa_selector is not None:
            t = Element("{%s}hasTarget" % cls.OANS)
            t.set("{%s}resource" % cls.RDFNS, "info:fedora/" + annotation_pid + "/SpecificTarget")
            descrip_annotation.append(t)

        # RDF oa:Body Description Element
        descrip_body = Element("{%s}Description" % cls.RDFNS)
        descrip_body.set("{%s}about" % cls.RDFNS, "info:fedora/" + annotation_pid)

        body_type = Element("{%s}type" % cls.RDFNS)
        body_type.set("{%s}resource" % cls.RDFNS, "oa:Body")
        descrip_body.append(body_type)

        if body_content_mimetype is not None:
            body_mime = Element("{%s}format" % cls.DC_NS)
            body_mime.text = body_content_mimetype
            descrip_body.append(body_mime)

        """
        nw = datetime.utcnow().replace(tzinfo=pytz.utc)
        generated = Element("{%s}generated" % cls.OANS)
        generated.set("{%s}resource" % cls.RDFNS, "info:fedora/" + annotation_pid)
        generated.text = nw.isoformat()
        descrip.append(generated)
        
        submitted = kwargs.pop('submitted')
        if submitted is not None:
            annotated = Element("{%s}annotated" % cls.OANS)
            annotated.set("{%s}resource" % cls.RDFNS, "info:fedora/" + annotation_pid)
            annotated.text = submitted.isoformat()
            descrip.append(annotated)

        annotator = kwargs.pop('annotator', None)
        if annotator is not None:
            anno = Element("{%s}annotator" % cls.OANS)
            anno.set("{%s}resource" % cls.RDFNS, "info:fedora/" + annotation_pid)
            anno.text = annotator
            descrip.append(anno)

        generator = kwargs.pop('generator', None)
        if generator is not None:
            gn = Element("{%s}generator" % cls.OANS)
            gn.set("{%s}resource" % cls.RDFNS, "info:fedora/" + annotation_pid)
            gn.text = generator
            descrip.append(gn)
        """

        rdf = Element("{%s}RDF" % cls.RDFNS)
        rdf.append(descrip_annotation)
        rdf.append(descrip_body)

        return rdf

    @classmethod
    def get_specific_target_rdf_element(cls, **kwargs):
        """
        <rdf:RDF>
          <rdf:Description rdf:about="info:fedora/{{ANNO1_PID}}/SpecificTarget">
            <rdf:type rdf:resource="oa:SpecificResource"/>
            <oa:hasSource rdf:resource="{{source_uri}}"/>
            <oax:hasStyle rdf:resource="{{oax_style_uri}}"/>
            <oa:hasSelector rdf:resource="info:fedora/{{ANNO1_PID}}/selector"/>
          </rdf:Description>
        </rdf:RDF>
        """
        annotation_pid = kwargs.pop('pid')
        source_uri = kwargs.pop('source_uri')
        oax_style_uri = kwargs.pop('oax_style_uri')

        descrip = Element("{%s}Description" % cls.RDFNS)
        descrip.set("{%s}about" % cls.RDFNS, "info:fedora/" + annotation_pid + "/SpecificTarget")

        typee = Element("{%s}type" % cls.RDFNS)
        typee.set("{%s}resource" % cls.RDFNS, "oa:SpecificResource")
        descrip.append(typee)

        source = Element("{%s}hasSource" % cls.OANS)
        source.set("{%s}resource" % cls.RDFNS, source_uri)
        descrip.append(source)

        selector = Element("{%s}hasSelector" % cls.OANS)
        selector.set("{%s}resource" % cls.RDFNS, "info:fedora/" + annotation_pid + "/selector")
        descrip.append(selector)

        if oax_style_uri is not None:
            style = Element("{%s}hasStyle" % cls.OAXNS)
            style.set("{%s}resource" % cls.RDFNS, oax_style_uri)
            descrip.append(style)

        rdf = Element("{%s}RDF" % cls.RDFNS)
        rdf.append(descrip)

        return rdf

    @classmethod
    def get_selector_rdf_element(cls, **kwargs):
        """
        <rdf:RDF>
          <rdf:Description rdf:about="info:fedora/test:1000010119/selector">
            <rdf:type rdf:resource="oa:FragmentSelector"/>
            <rdf:value>/my/xpath/</rdf:value>
          </rdf:Description>
        </rdf:RDF>
        """
        annotation_pid = kwargs.pop('pid')
        oa_selector = kwargs.pop('oa_selector')
        oa_selector_type_uri = kwargs.pop('oa_selector_type_uri')

        descrip = Element("{%s}Description" % cls.RDFNS)
        descrip.set("{%s}about" % cls.RDFNS, "info:fedora/" + annotation_pid + "/selector")

        typee = Element("{%s}type" % cls.RDFNS)
        typee.set("{%s}resource" % cls.RDFNS, oa_selector_type_uri)
        descrip.append(typee)

        value = Element("{%s}value" % cls.RDFNS)
        value.text = oa_selector
        descrip.append(value)

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
        """
        <foxml:datastream ID="DC" FEDORA_URI="info:fedora/{{ANNO1_PID}}/DC" STATE="A" CONTROL_GROUP="X" VERSIONABLE="true" />
        """
        datastream = Element("{%s}datastream" % cls.FOXMLNS)
        datastream.set("ID", kwargs.pop('id'))
        datastream.set("STATE", kwargs.pop('state'))
        datastream.set("CONTROL_GROUP", kwargs.pop('control_group'))
        if kwargs.get('fedora_uri'):
            datastream.set("FEDORA_URI", kwargs.pop('fedora_uri'))
        return datastream

    @classmethod
    def get_datastream_version_element(cls, **kwargs):
        """
        <foxml:datastreamVersion ID="DC1.0" LABEL="Dublin Core Record for this object" CREATED="2012-05-21T20:43:41.682Z" MIMETYPE="text/xml" FORMAT_URI="http://www.openarchives.org/OAI/2.0/oai_dc/" SIZE="344" />
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
        """
        <foxml:datastream ID="DC" FEDORA_URI="info:fedora/{{ANNO1_PID}}/DC" STATE="A" CONTROL_GROUP="X" VERSIONABLE="true">
          <foxml:datastreamVersion ID="DC1.0" LABEL="Dublin Core Record for this object" CREATED="2012-05-21T20:43:41.682Z" MIMETYPE="text/xml" FORMAT_URI="http://www.openarchives.org/OAI/2.0/oai_dc/" SIZE="344">
            <foxml:contentDigest TYPE="MD5" DIGEST="8d7ef20a1982db6a30dfc32170a27fc3"/>
            <foxml:xmlContent>
              <oai_dc:dc xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/ http://www.openarchives.org/OAI/2.0/oai_dc.xsd">
                <!-- This should be auto-generated by Fedora upon creation -->
                <dc:identifier>{{ANNO1_PID}}</dc:identifier>
                <dc:title>{{dc_title}}</dc:title>
              </oai_dc:dc>
            </foxml:xmlContent>
          </foxml:datastreamVersion>
        </foxml:datastream>
        """
        xml_content = Foxml.get_xml_content_element()
        xml_content.append(kwargs.pop('dublin_core_element'))

        datastream_version = Foxml.get_datastream_version_element(format_uri=cls.OAIDC_INFO_URI, id="DC1.0", mime="text/xml", label="Dublin Core Record for this object")
        datastream_version.append(xml_content)

        datastream = Foxml.get_datastream_element(id="DC", state="A", control_group="M", fedora_uri=kwargs.pop('fedora_uri', None))
        datastream.append(datastream_version)
        return datastream

    @classmethod
    def get_annotation_datastream(cls, **kwargs):
        """
        <foxml:datastream ID="annotation" FEDORA_URI="info:fedora/{{ANNO1_PID}}/annotation" STATE="A" CONTROL_GROUP="X" VERSIONABLE="true">
          <foxml:datastreamVersion ID="annotation.0" LABEL="" CREATED="2012-05-23T13:54:31.203Z" MIMETYPE="text/xml" SIZE="809">
            <foxml:contentDigest TYPE="MD5" DIGEST="48e7b0c1ecedfccb443f6f693a894dc6"/>
            <foxml:xmlContent>
              <rdf:RDF>
                <rdf:Description rdf:about="info:fedora/{{ANNO1_PID}}">
                  <rdf:type rdf:resource="oa:Annotation"/>
                  <!-- if a Fedora BODY object is created, use the format "info:fedora/{{BODY_PID}}": -->
                  <oa:hasBody rdf:resource="{{body_uri}}"/>
                  <!-- if a oa_selector is passed as a parameter, include: -->
                  <oa:hasTarget rdf:resource="info:fedora/{{ANNO1_PID}}/SpecificTarget"/>
                  <!-- Always include: -->
                  <oa:modelVersion rdf:resource="http://www.openannotation.org/spec/core/20120509.html"/>
                </rdf:Description>
                <rdf:Description rdf:about="{{ANNO1_PID}}">
                  <rdf:type rdf:resource="oa:Body"/>
                  <dc:format>{{body_content_mimetype}}</dc:format>
                </rdf:Description>
              </rdf:RDF>
            </foxml:xmlContent>
          </foxml:datastreamVersion>
        </foxml:datastream>
        """
        xml_content = Foxml.get_xml_content_element()
        xml_content.append(kwargs.pop('annotation_rdf_element'))

        datastream_version = Foxml.get_datastream_version_element(id="annotation.0", mime="text/xml", label="")
        datastream_version.append(xml_content)

        datastream = Foxml.get_datastream_element(id="annotation", state="A", control_group="M", fedora_uri=kwargs.pop('fedora_uri', None))
        datastream.append(datastream_version)
        return datastream

    @classmethod
    def get_specific_target_datastream(cls, **kwargs):
        """
        <foxml:datastream ID="specifictarget" FEDORA_URI="info:fedora/{{ANNO1_PID}}/specifictarget" STATE="A" CONTROL_GROUP="X" VERSIONABLE="true">
          <foxml:datastreamVersion ID="specifictarget.0" LABEL="SpecificTarget data for OAC annotation" CREATED="2012-05-23T13:58:54.925Z" MIMETYPE="application/rdf+xml" SIZE="696">
            <foxml:contentDigest TYPE="MD5" DIGEST="6f5253c77a8620c63d529f7a3728b914"/>
            <foxml:xmlContent>
              <rdf:RDF>
                <rdf:Description rdf:about="info:fedora/{{ANNO1_PID}}/SpecificTarget">
                  <rdf:type rdf:resource="oa:SpecificResource"/>
                  <oa:hasSource rdf:resource="{{source_uri}}"/>
                  <oax:hasStyle rdf:resource="{{oax_style_uri}}"/>
                  <oa:hasSelector rdf:resource="info:fedora/{{ANNO1_PID}}/selector"/>
                </rdf:Description>
              </rdf:RDF>
            </foxml:xmlContent>
          </foxml:datastreamVersion>
        </foxml:datastream>
        """
        xml_content = Foxml.get_xml_content_element()
        xml_content.append(kwargs.pop('specific_target_rdf_element'))

        datastream_version = Foxml.get_datastream_version_element(id="specifictarget.0", mime="application/rdf+xml", label="SpecificTarget data for OAC annotation")
        datastream_version.append(xml_content)

        datastream = Foxml.get_datastream_element(id="specifictarget", state="A", control_group="M", fedora_uri=kwargs.pop('fedora_uri', None))
        datastream.append(datastream_version)
        return datastream 

    @classmethod
    def get_selector_datastream(cls, **kwargs):
        """
        <foxml:datastream ID="selector" FEDORA_URI="info:fedora/{{ANNO1_PID}}/selector" STATE="A" CONTROL_GROUP="X" VERSIONABLE="true">
          <foxml:datastreamVersion ID="selector.0" LABEL="Selector data for OAC annotation" CREATED="2012-05-23T14:01:04.109Z" MIMETYPE="application/rdf+xml" SIZE="323">
            <foxml:contentDigest TYPE="MD5" DIGEST="4b79ce591314432405d46558502ee4ee"/>
            <foxml:xmlContent>
              <rdf:RDF>
                <rdf:Description rdf:about="info:fedora/{{ANNO1_PID}}/selector">
                  <rdf:type rdf:resource="oa:FragmentSelector"/>
                  <!-- If oa_selector_type is passed -->
                  <rdf:type rdf:resource="{{oa_selector_type_uri}}"/>
                  <rdf:value>{{oa_selector}}</rdf:value>
                </rdf:Description>
              </rdf:RDF>
            </foxml:xmlContent>
          </foxml:datastreamVersion>
        </foxml:datastream>
        """
        xml_content = Foxml.get_xml_content_element()
        xml_content.append(kwargs.pop('selector_rdf_element'))

        datastream_version = Foxml.get_datastream_version_element(id="selector.0", mime="application/rdf+xml", label="Selector data for OAC annotation")
        datastream_version.append(xml_content)

        datastream = Foxml.get_datastream_element(id="selector", state="A", control_group="M", fedora_uri=kwargs.pop('fedora_uri', None))
        datastream.append(datastream_version)
        return datastream 

    @classmethod
    def get_xml_body_content_datastream(cls, **kwargs):
        xml_content = Foxml.get_xml_content_element()

        body_xml = kwargs.pop('body_content')
        body_element = ET.fromstring(body_xml)
        xml_content.append(body_element)

        datastream_version = Foxml.get_datastream_version_element(id="OAC_BODY.0", mime=kwargs.pop('body_mimetype'), label="OAC Body Content")
        datastream_version.append(xml_content)

        datastream = Foxml.get_datastream_element(id="OAC_BODY", state="A", control_group="M")
        datastream.append(datastream_version)
        return datastream