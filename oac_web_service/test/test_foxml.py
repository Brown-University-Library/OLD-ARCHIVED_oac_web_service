import unittest
from oac_web_service.models.foxml import Foxml
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import dump, parse, fromstring, tostring

class FoxmlTest(unittest.TestCase):
    def setUp(self):
        self.foxml = Foxml(pid='1')
        self.foxml.create_object_properties()
        self.targets = [{'pid' : 'test:1', 'uri' : "test:1#xpointer('/foo)"},
                        {'pid' : 'test:2', 'uri' : "test:2#xpointer('/bar)"}]
        # Object Properties
        
        # Dublin Core Datastream
        #f.create_dublin_core_datastream(dublin_core_element=dublin_core)
        # Rels Ext Datastream
        #f.create_rels_ext_datastream(rdf_element=rdf)

        #dump(Foxml.get_object_properties())
        #dump(Foxml.get_xml_content_element())
        #dump(Foxml.get_datastream_version_element(format_url=Foxml.RELSEXT_INFO_URI, id="RELS-EXT.0", mime="application/rdf+xml", label="RDF Statements about this object"))
        #dump(Foxml.get_rels_ext_datastream(rdf_element=rdf))
        #dump(Foxml.get_dublin_core_datastream(dublin_core_element=dc))

    def test_object_properties(self):
        should_be = """
                    <foxml:objectProperties xmlns:foxml="info:fedora/fedora-system:def/foxml#">
                        <foxml:property NAME="info:fedora/fedora-system:def/model#state" VALUE="A" />
                        <foxml:property NAME="info:fedora/fedora-system:def/model#label" VALUE="OAC object" />
                    </foxml:objectProperties>
                    """
        op = Foxml.get_object_properties()

    def test_rdf_body_element(self):
        rdf = Foxml.get_rdf_body_element(pid='1', targets=self.targets)

    def text_rdf_annotation_element(self):
        rdf = Foxml.get_rdf_annotation_element(pid='1', body_pid='body:2', targets=self.targets)

    def test_rels_ext_datastream(self):
        rdf = Foxml.get_rdf_body_element(pid='1', targets=self.targets)
        rxds = Foxml.get_rels_ext_datastream(rdf_element=rdf)

    def test_dublin_core_element(self):
        dc = Foxml.get_dublin_core_element(pid='1', title="super!")

    def test_dublin_core_datastream(self):
        dc = Foxml.get_dublin_core_element(pid='1', title="super!")
        dcds = Foxml.get_dublin_core_datastream(dublin_core_element=dc)

    def test_datastream_element(self):
        ds = Foxml.get_datastream_element(id="1", state="A", control_group="TXXVGA")

    def test_get_xml_content_element(self):
        xmlc = Foxml.get_xml_content_element()

    def test_datastream_version_element(self):
        dsv = Foxml.get_datastream_version_element( id="1",
                                                    mime='application/rdf+xml', 
                                                    label="super element!",
                                                    format_uri="info:fedora/fedora-system:FedoraRELSExt-1.0")