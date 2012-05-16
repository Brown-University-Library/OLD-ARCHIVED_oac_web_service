import unittest
from oac_web_service.models.annotation import Annotation
import oac_web_service.fedora_settings as config
from xml.etree.ElementTree import dump

class FoxmlTest(unittest.TestCase):
    def setUp(self):
        self.annotation = Annotation(target_pid = 'target:1',
                                     body_xml = '<foxml />',
                                     target_uri = 'amazing:uri',
                                     dc_title = 'title'
                                    )

    def test_pid_creation(self):
        pid1 = int(self.annotation.get_pid().split(":")[-1])
        pid2 = int(self.annotation.get_pid().split(":")[-1])

        assert pid2 > pid1

