from flask import Flask
app = Flask(__name__)
app.config.from_object('oac_web_service.fedora_settings')
app.config.from_envvar('FEDORA_SETTINGS', silent=True)

# Set a default Annotation content model if one was not set in the settings files
if app.config.get('DEFUALT_ANNOTATION_CONTENT_MODEL', None) is None:
	app.config['DEFUALT_ANNOTATION_CONTENT_MODEL'] = 'oac:oa-annotation'

import os

# Logging
if not app.debug:
    import logging
    from logging import FileHandler
    logfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'oac.log')
    file_handler = FileHandler(logfile)
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)

# Create path to persistant index
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'OAC.tdb')

import oac_web_service.views
import oac_web_service.models