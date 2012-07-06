from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element
from datetime import datetime
from oac_web_service.utils import *
import pytz

class Foxml(object):

    FOXMLNS = "info:fedora/fedora-system:def/foxml#"
    ET._namespace_map[FOXMLNS] = 'foxml'

    RDFNS = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    ET._namespace_map[RDFNS] = 'rdf'
    
    OANS = "http://www.w3.org/ns/openannotation/core/"
    ET._namespace_map[OANS] = 'oa'

    OAXNS = "http://www.w3.org/ns/openannotation/extension/"
    ET._namespace_map[OAXNS] = 'oax'

    OAI_DC_NS = "http://www.openarchives.org/OAI/2.0/oai_dc/"
    ET._namespace_map[OAI_DC_NS] = 'oai_dc'

    DC_NS = "http://purl.org/dc/elements/1.1/"
    ET._namespace_map[DC_NS] = 'dc'

    CNT_NS = "http://www.w3.org/2011/content#"
    ET._namespace_map[CNT_NS] = 'cnt'

    FEDORA_MODEL_NS = "info:fedora/fedora-system:def/model#"
    ET._namespace_map[FEDORA_MODEL_NS] = "fedora-model"

    STATE_INFO_URI = "%sstate" % FEDORA_MODEL_NS
    LABEL_INFO_URI = "%slabel" % FEDORA_MODEL_NS
    RELSEXT_INFO_URI = "info:fedora/fedora-system:FedoraRELSExt-1.0";

    def __init__(self, **kwargs):
        self._doc = Element("{%s}digitalObject" % self.FOXMLNS)
        self._doc.set('VERSION', '1.1')
        self._doc.set('PID', kwargs.get('pid'))
        self._doc.set('FEDORA_URI', "info:fedora/%s" % kwargs.get('pid'))
       
    def create_object_properties(self):
        self._doc.append(Foxml.get_object_properties())

    def create_xml_datastream(self, **kwargs):
        self._doc.append(Foxml.get_xml_datastream(**kwargs))

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
    def get_rels_ext_model_element(cls, **kwargs):
        """
        <rdf:RDF>
            <rdf:Description rdf:about="info:fedora/{{PID}}">
                <fedora-model:hasModel rdf:resource="info:fedora/{{MODEL}}"/>
            </rdf:Description>
        </rdf:RDF>
        """
        pid = kwargs.pop('pid')
        model = kwargs.pop('model')

        descrip = Element("{%s}Description" % cls.RDFNS)
        descrip.set("{%s}about" % cls.RDFNS, "info:fedora/" + pid)

        md = Element("{%s}hasModel" % cls.FEDORA_MODEL_NS)
        md.set("{%s}resource" % cls.RDFNS, "info:fedora/" + model)
        descrip.append(md)

        rdf = Element("{%s}RDF" % cls.RDFNS)
        rdf.append(descrip)

        return rdf


    @classmethod
    def get_annotation_rdf_element(cls, **kwargs):
        """
        <rdf:RDF>
          <rdf:Description rdf:about="info:fedora/{{ANNO1_PID}}">
            <rdf:type rdf:resource="oa:Annotation"/>
            <oa:hasBody rdf:resource="{{BODY_URI}}"/>
            <!-- if a oa_selector is passed as a parameter, include: -->
            <oa:hasTarget rdf:resource="info:fedora/{{ANNO1_PID}}/SpecificTarget"/>
            <!--Optional provenance parameters-->
            <oa:annotator>{{annotator}}</oa:annotator>
            <oa:generator>{{generator}}</oa:generator> 
            <!--POST only-->
            <oa:annotated>{{datetime}}</oa:annotated>
            <!--End optional provenance parameters -->
            <!-- Always include: -->
            <oa:modelVersion rdf:resource="http://www.openannotation.org/spec/core/20120509.html"/>
            <oa:annotated>{{datetime}}</oa:annotated>
          </rdf:Description>
          <rdf:Description rdf:about="{{BODY_URI}}">
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
        annotated = kwargs.pop('annotated', None)
        generator = kwargs.pop('generator', None)
        annotator = kwargs.pop('annotator', None)

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

        # Always update the "generated", POST or PUT
        gn = Element("{%s}generated" % cls.OANS)
        gn.text = "%sZ" % datetime.utcnow().isoformat()
        descrip_annotation.append(gn)

        if oa_selector is not None:
            t = Element("{%s}hasTarget" % cls.OANS)
            t.set("{%s}resource" % cls.RDFNS, "info:fedora/" + annotation_pid + "/SpecificTarget")
            descrip_annotation.append(t)

        # Optionals
        if annotated is not None:
            an = Element("{%s}annotated" % cls.OANS)
            an.text = "%sZ" % annotated.isoformat()
            descrip_annotation.append(an)
        if generator is not None:
            gnr = Element("{%s}generator" % cls.OANS)
            gnr.text = generator
            descrip_annotation.append(gnr)
        if annotator is not None:
            anr = Element("{%s}annotator" % cls.OANS)
            anr.text = annotator
            descrip_annotation.append(anr)


        # RDF oa:Body Description Element
        descrip_body = Element("{%s}Description" % cls.RDFNS)
        descrip_body.set("{%s}about" % cls.RDFNS, body_uri)

        body_type = Element("{%s}type" % cls.RDFNS)
        body_type.set("{%s}resource" % cls.RDFNS, "oa:Body")
        descrip_body.append(body_type)

        if body_content_mimetype is not None:
            body_mime = Element("{%s}format" % cls.DC_NS)
            body_mime.text = body_content_mimetype
            descrip_body.append(body_mime)


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
        fragment_type = kwargs.pop('fragment_type')

        descrip = Element("{%s}Description" % cls.RDFNS)
        descrip.set("{%s}about" % cls.RDFNS, "info:fedora/" + annotation_pid + "/selector")

        typee = Element("{%s}type" % cls.RDFNS)
        typee.set("{%s}resource" % cls.RDFNS, oa_selector_type_uri)
        descrip.append(typee)

        if fragment_type is not None:
            frag_type = Element("{%s}type" % cls.RDFNS)
            frag_type.set("{%s}resource" % cls.RDFNS, fragment_type)
            descrip.append(frag_type)

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
        datastreamVersion.set("ID", kwargs.pop('id') + ".0");
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
    def get_xml_datastream(cls, **kwargs):
        """
        <foxml:datastream ID="{{id}}.0" FEDORA_URI="{{fedora_uri}}" STATE="A" CONTROL_GROUP="M">
          <foxml:datastreamVersion ID="{{id}}" LABEL="{{label}}" MIMETYPE="{{mimetype}}" FORMAT_URI="{{format_uri}}">
            <foxml:xmlContent>
                {{ element }}
            </foxml:xmlContent>
          </foxml:datastreamVersion>
        </foxml:datastream>
        """
        xml_content = Foxml.get_xml_content_element()

        # Allow the passed in 'element' parameter to be a string
        ele = kwargs.get('element')
        if isinstance(ele, str) or isinstance(ele, unicode):
            xml_content.append(ET.fromstring(ele))
        else:
            xml_content.append(ele)     

        version_id = kwargs.get('version_id', kwargs.get('id'))
        datastream_version = Foxml.get_datastream_version_element(format_uri=kwargs.pop('format_uri', None), id=version_id, mime=kwargs.pop('mime'), label=kwargs.pop('label'))
        datastream_version.append(xml_content)

        datastream = Foxml.get_datastream_element(id=kwargs.pop('id'), state="A", control_group="M", fedora_uri=kwargs.pop('fedora_uri', None))
        datastream.append(datastream_version)
        return datastream

    @classmethod
    def get_rdf_descriptions(cls, element):
        return element.findall("{%s}Description" % cls.RDFNS)

    @classmethod
    def get_rdf_string_from_descriptions(cls, elements):

        rdf = Element("{%s}RDF" % cls.RDFNS)
        rdf.set('xmlns:oa', cls.OANS)
        rdf.set('xmlns:oax', cls.OAXNS)
        rdf.set('xmlns:cnt', cls.CNT_NS)
        rdf.set('xmlns:dc', cls.DC_NS)

        [rdf.append(d) for d in elements]
        #cleanup_namespaces(rdf,ET._namespace_map)
        indent(rdf)
        return ET.tostring(rdf)