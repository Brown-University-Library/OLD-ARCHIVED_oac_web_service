import unittest
from oac_web_service.models.fedora import Fedora

class FedoraTest(unittest.TestCase):

    def test_pid_creation(self):
        pid1 = int(Fedora.get_pid().split(":")[-1])
        pid2 = int(Fedora.get_pid().split(":")[-1])
        assert pid2 > pid1