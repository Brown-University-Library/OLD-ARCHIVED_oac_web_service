import unittest
from oac_web_service.models.fedora import Fedora
from oac_web_service.models.foxml import Foxml

class FedoraTest(unittest.TestCase):

    def test_pid_creation(self):
        pid1 = int(Fedora.get_pid().split(":")[-1])
        pid2 = int(Fedora.get_pid().split(":")[-1])
        assert pid2 > pid1

    def test_put(self):
        ele = Foxml.get_annotation_rdf_element(pid='changeme:350', body_uri='changeme:347', body_mimetype='text/xml')
        Fedora.put_datastream(pid='changeme:350', dsid='annotation', element=ele)

    def test_datastream_list(self):
        datastreams = Fedora.get_datastream_list('changeme:350')
        assert len(datastreams) == 4
        assert datastreams == ['DC', 'annotation', 'specifictarget', 'selector']