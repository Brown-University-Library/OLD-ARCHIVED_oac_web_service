from flask import Flask
app = Flask(__name__)
app.config.from_object('oac_web_service.fedora_settings')
app.config.from_envvar('FEDORA_SETTINGS', silent=True)

# Set a default Annotation content model if one was not set in the settings files
if app.config.get('DEFUALT_ANNOTATION_CONTENT_MODEL', None) is None:
    app.config['DEFUALT_ANNOTATION_CONTENT_MODEL'] = 'oac:oa-annotation'

import os

# Create path to persistant index
if app.config.get('STORE_LOCATION', None) is None:
    app.config['STORE_LOCATION'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

if not os.access(app.config['STORE_LOCATION'], os.W_OK | os.X_OK):
    raise IOError(0, "Can't write to STORE_LOCATION, check configuration: %s" % app.config['STORE_LOCATION'])

app.config['STORE_LOCATION'] = os.path.join(app.config['STORE_LOCATION'], 'OAC.tdb')

import oac_web_service.views
import oac_web_service.models