import unittest
from oac_web_service.models.foxml import Foxml
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import dump, parse, fromstring, tostring

class FoxmlTest(unittest.TestCase):
    def test_object_properties(self):
        should_be = """
                    <foxml:objectProperties xmlns:foxml="info:fedora/fedora-system:def/foxml#">
                        <foxml:property NAME="info:fedora/fedora-system:def/model#state" VALUE="A" />
                        <foxml:property NAME="info:fedora/fedora-system:def/model#label" VALUE="OAC object" />
                    </foxml:objectProperties>
                    """
        op = Foxml.get_object_properties()

    def test_rdf_annotation_element(self):
        should_be = """ 
                    <rdf:RDF>
                        <rdf:Description rdf:about="info:fedora/1">
                            <rdf:type rdf:resource="oa:Annotation"/>
                            <oa:hasBody rdf:resource="body:2"/>
                            <oa:hasTarget rdf:resource="info:fedora/1/SpecificTarget"/>
                            <oa:modelVersion rdf:resource="http://www.openannotation.org/spec/core/20120509.html"/>
                        </rdf:Description>
                        <rdf:Description rdf:about="body:2">
                            <rdf:type rdf:resource="oa:Body"/>
                            <dc:format>text/xml</dc:format>
                        </rdf:Description>
                    </rdf:RDF>
                    """
        rdf = Foxml.get_annotation_rdf_element(pid='1', body_uri='body:2', body_mimetype='text/xml')


    def test_datastream_element(self):
        ds = Foxml.get_datastream_element(id="1", state="A", control_group="TXXVGA",fedora_uri="info:fedora/1/something")

    def test_get_xml_content_element(self):
        xmlc = Foxml.get_xml_content_element()

    def test_datastream_version_element(self):
        dsv = Foxml.get_datastream_version_element( id="1",
                                                    mime='application/rdf+xml', 
                                                    label="super element!",
                                                    format_uri="info:fedora/fedora-system:FedoraRELSExt-1.0")
    def test_dublin_core_datastream(self):
        should_be = """
                    <foxml:datastream ID="DC" FEDORA_URI="info:fedora/1/DC" STATE="A" CONTROL_GROUP="M">
                      <foxml:datastreamVersion ID="DC1.0" LABEL="Dublin Core Record for this object" MIMETYPE="text/xml" FORMAT_URI="http://www.openarchives.org/OAI/2.0/oai_dc/">
                        <foxml:xmlContent>
                          <oai_dc:dc xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/ http://www.openarchives.org/OAI/2.0/oai_dc.xsd">
                            <dc:identifier>1</dc:identifier>
                            <dc:title>super!</dc:title>
                          </oai_dc:dc>
                        </foxml:xmlContent>
                      </foxml:datastreamVersion>
                    </foxml:datastream>
                    """
        ele = Foxml.get_dublin_core_element(pid='1',
                                            title="super!")
        ds = Foxml.get_xml_datastream(element=ele,
                                      id="DC",
                                      version_id="DC1",
                                      mime="text/xml",
                                      label="Dublin Core Record for this object",
                                      fedora_uri="info:fedora/1/DC",
                                      format_uri="http://www.openarchives.org/OAI/2.0/oai_dc/")

    def test_annotation_datastream(self):
        should_be = """
                    <foxml:datastream ID="annotation" FEDORA_URI="info:fedora/1/annotation" STATE="A" CONTROL_GROUP="M">
                      <foxml:datastreamVersion ID="annotation.0" LABEL="" MIMETYPE="text/xml">
                        <foxml:xmlContent>
                          <rdf:RDF>
                            <rdf:Description rdf:about="info:fedora/1">
                              <rdf:type rdf:resource="oa:Annotation"/>
                              <oa:hasBody rdf:resource="body:1"/>
                              <oa:hasTarget rdf:resource="info:fedora/1/SpecificTarget"/>
                              <oa:modelVersion rdf:resource="http://www.openannotation.org/spec/core/20120509.html"/>
                              <oa:generated>{{datetime}}</oa:generated>
                              <oa:annotator>Mac</oa:annotator>
                              <oa:generator>Web</oa:generator>
                              <oa:annotated>{{datetime}}</oa:annotated>
                            </rdf:Description>
                            <rdf:Description rdf:about="1">
                              <rdf:type rdf:resource="oa:Body"/>
                              <dc:format>text/xml</dc:format>
                            </rdf:Description>
                          </rdf:RDF>
                        </foxml:xmlContent>
                      </foxml:datastreamVersion>
                    </foxml:datastream>
                    """
        ele = Foxml.get_annotation_rdf_element(pid='1',
                                               body_uri='body:1',
                                               oa_selector='/my/xpath',
                                               body_mimetype='text/xml',
                                               annotator='Mac',
                                               generator='Web')
        ds = Foxml.get_xml_datastream(element=ele,
                                      id="annotation",
                                      mime="application/rdf+xml",
                                      label="OAC annotation core",
                                      fedora_uri='info:fedora/1/annotation')

    def test_specific_target_datastream(self):
        should_be = """
                    <foxml:datastream ID="specifictarget" FEDORA_URI="info:fedora/1/specifictarget" STATE="A" CONTROL_GROUP="M">
                      <foxml:datastreamVersion ID="specifictarget.0" LABEL="SpecificTarget data for OAC annotation" MIMETYPE="application/rdf+xml">
                        <foxml:xmlContent>
                          <rdf:RDF>
                            <rdf:Description rdf:about="info:fedora/1/SpecificTarget">
                              <rdf:type rdf:resource="oa:SpecificResource"/>
                              <oa:hasSource rdf:resource="source:2"/>
                              <oax:hasStyle rdf:resource="style:3"/>
                              <oa:hasSelector rdf:resource="info:fedora/1/selector"/>
                            </rdf:Description>
                          </rdf:RDF>
                        </foxml:xmlContent>
                      </foxml:datastreamVersion>
                    </foxml:datastream>
                    """

        ele = Foxml.get_specific_target_rdf_element(pid='1',
                                                    source_uri='source:2',
                                                    oax_style_uri='style:3')
        ds = Foxml.get_xml_datastream(element=ele,
                                      id="specifictarget",
                                      mime="application/rdf+xml",
                                      label="SpecificTarget data for OAC annotation",
                                      fedora_uri='info:fedora/1/specifictarget')

    def test_selector_datastream(self):
        should_be = """
                    <foxml:datastream ID="selector" FEDORA_URI="info:fedora/1/selector" STATE="A" CONTROL_GROUP="M">
                      <foxml:datastreamVersion ID="selector.0" LABEL="Selector data for OAC annotation" MIMETYPE="application/rdf+xml">
                        <foxml:xmlContent>
                          <rdf:RDF>
                            <rdf:Description rdf:about="info:fedora/{{ANNO1_PID}}/selector">
                              <rdf:type rdf:resource="oa:FragmentSelector"/>
                              <rdf:value>/my/xpath/</rdf:value>
                            </rdf:Description>
                          </rdf:RDF>
                        </foxml:xmlContent>
                      </foxml:datastreamVersion>
                    </foxml:datastream>
                    """
        ele = Foxml.get_selector_rdf_element(pid='1',
                                             oa_selector='/my/xpath/',
                                             oa_selector_type_uri='oa:FragmentSelector')
        ds = Foxml.get_xml_datastream(element=ele,
                                      id="selector",
                                      mime="application/rdf+xml",
                                      label="Selector data for OAC annotation",
                                      fedora_uri='info:fedora/1/selector')
                                           
    def test_xml_body_content_datastream(self):
        body_string = "<TEI><body>Some TEI text goes here.</body></TEI>"
        body = Foxml.get_xml_datastream(element=body_string,
                                        id="OAC_BODY",
                                        label="OAC Body Content",
                                        mime='text/xml')

    def test_rels_ext_model_datastream(cls, **kwargs):
        should_be = """
                    <foxml:datastream ID="RELS-EXT" STATE="A" CONTROL_GROUP="X" VERSIONABLE="true">
                        <foxml:datastreamVersion ID="RELS-EXT.0" LABEL="RDF Statements about this object" MIMETYPE="application/rdf+xml" FORMAT_URI="info:fedora/fedora-system:FedoraRELSExt-1.0">
                            <foxml:xmlContent>
                                <rdf:RDF>
                                    <rdf:Description rdf:about="info:fedora/1">
                                        <fedora-model:hasModel rdf:resource="info:fedora/bdr-cmodel:tei-annotation"/>
                                    </rdf:Description>
                                </rdf:RDF>
                            </foxml:xmlContent>
                        </foxml:datastreamVersion>
                    </foxml:datastream>
                    """
        ele = Foxml.get_rels_ext_model_element(pid='1',
                                               models=['tei-annotation'])

        ds = Foxml.get_xml_datastream(element=ele,
                                      id="RELS-EXT",
                                      mime="application/rdf+xml",
                                      label="RDF Statements about this object",
                                      format_uri="info:fedora/fedora-system:FedoraRELSExt-1.0")