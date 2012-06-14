from flask import Flask
app = Flask(__name__)
app.config.from_object('oac_web_service.fedora_settings')
app.config.from_envvar('FEDORA_SETTINGS', silent=True)
 
# Create or persistant index
from com.hp.hpl.jena.tdb import TDBFactory
import os
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'OAC.tdb')
dataset = TDBFactory.createDataset(db_path)

import oac_web_service.views
import oac_web_service.models