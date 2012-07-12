import unittest
from oac_web_service.models.fedora import Fedora
from oac_web_service.models.foxml import Foxml

class FedoraTest(unittest.TestCase):

    def test_pid_creation(self):
        pid1 = int(Fedora.get_pid().split(":")[-1])
        pid2 = int(Fedora.get_pid().split(":")[-1])
        assert pid2 > pid1

    def test_put(self):
        ele = Foxml.get_annotation_rdf_element(pid='changeme:9', body_uri='changeme:8', body_mimetype='text/xml')
        Fedora.put_datastream(pid='changeme:9', dsid='annotation', element=ele)

    def test_datastream_list(self):
        datastreams = Fedora.get_datastream_list('changeme:9')
        assert len(datastreams) == 5
        assert datastreams == ['DC', 'annotation', 'RELS-EXT', 'specifictarget', 'selector']