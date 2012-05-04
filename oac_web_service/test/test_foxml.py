import unittest
from oac_web_service.models.foxml import Foxml
from xml.etree.ElementTree import dump

class FoxmlTest(unittest.TestCase):
    def setUp(self):
        f = Foxml(pid='1')
        #dump(Foxml.get_object_properties())
        #dump(dc)
        #dump(Foxml.get_xml_content_element())
        #dump(Foxml.get_datastream_version_element(format_url=Foxml.RELSEXT_INFO_URI, id="RELS-EXT.0", mime="application/rdf+xml", label="RDF Statements about this object"))
        #dump(Foxml.get_rels_ext_datastream(rdf_element=rdf))
        #dump(Foxml.get_dublin_core_datastream(dublin_core_element=dc))

    def test_rdf_body_element(self):
        rdf = Foxml.get_rdf_body_element(pid='1', target_pid='2')

    def test_dublin_code_element(self):
        dc = Foxml.get_dublin_core_element(pid='1', title="super!")