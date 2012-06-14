import unittest
from oac_web_service.models.annotation import Annotation
import oac_web_service.fedora_settings as config
from xml.etree.ElementTree import dump
from oac_web_service import app
import os
import shutil


class StoreTest(unittest.TestCase):
    def test_store_creation(self):

        from com.hp.hpl.jena.tdb import TDBFactory
        from java.io import ByteArrayInputStream
        from java.lang import String

        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'OAC.tdb')
        dataset = TDBFactory.createDataset(db_path)
        # Make sure the store was created
        assert os.path.isdir(db_path)

        # Make InputStream triples
        rdf_text = '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"><rdf:Description rdf:about="info:fedora/changeme:651"><rdf:type rdf:resource="oa:Annotation"></rdf:type><oa:hasBody xmlns:oa="http://www.w3.org/ns/openannotation/core/" rdf:resource="info:fedora/changeme:650"></oa:hasBody><oa:modelVersion xmlns:oa="http://www.w3.org/ns/openannotation/core/" rdf:resource="http://www.openannotation.org/spec/core/20120509.html"></oa:modelVersion><oa:generated xmlns:oa="http://www.w3.org/ns/openannotation/core/">2012-06-07T03:50:55.993000Z</oa:generated></rdf:Description><rdf:Description rdf:about="info:fedora/changeme:650"><rdf:type rdf:resource="oa:Body"></rdf:type><dc:format xmlns:dc="http://purl.org/dc/elements/1.1/">text/xml</dc:format></rdf:Description></rdf:RDF>'
        rdfxml = String(rdf_text)
        input_stream = ByteArrayInputStream(rdfxml.getBytes())

        model = dataset.getDefaultModel()
        model.begin()
        model.read(input_stream, None)
        model.commit()
        model.close()
        # Were all of the triples added?
        print model.size()
        assert model.size() == 6

        rdf_text2 = '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"><rdf:Description rdf:about="info:fedora/changeme:651"><rdf:type rdf:resource="oa:Annotation"></rdf:type><oa:hasBody xmlns:oa="http://www.w3.org/ns/openannotation/core/" rdf:resource="info:fedora/changeme:650"></oa:hasBody><oa:modelVersion xmlns:oa="http://www.w3.org/ns/openannotation/core/" rdf:resource="http://www.openannotation.org/spec/core/20120509.html"></oa:modelVersion><oa:generated xmlns:oa="http://www.w3.org/ns/openannotation/core/">2012-06-07T03:50:55.993000Z</oa:generated></rdf:Description><rdf:Description rdf:about="info:fedora/changeme:650"><rdf:type rdf:resource="oa:Body"></rdf:type><dc:format xmlns:dc="http://purl.org/dc/elements/1.1/">text/xml</dc:format></rdf:Description></rdf:RDF>'
        rdfxml2 = String(rdf_text2)
        input_stream2 = ByteArrayInputStream(rdfxml2.getBytes())
        model = dataset.getDefaultModel()
        model.begin()
        model.read(input_stream2, None)
        model.commit()
        model.close()
        # Were the triples appended to?
        print model.listStatements()
        assert model.size() == 12

        shutil.rmtree(db_path)
        # Was the store removed?
        assert not os.path.isdir(db_path)