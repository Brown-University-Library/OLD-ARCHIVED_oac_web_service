from flask import Flask
app = Flask(__name__)
app.config.from_object('oac_web_service.fedora_settings')
app.config.from_envvar('FEDORA_SETTINGS', silent=True)
 
# Create path to persistant index
import os
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'OAC.tdb')

# Create persistant index if it does not exist
from com.hp.hpl.jena.tdb import TDBFactory
dataset = TDBFactory.createDataset(db_path)
dataset.close()


import oac_web_service.views
import oac_web_service.models