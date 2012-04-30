from flask import Flask
app = Flask(__name__)
app.config.from_object('oac_web_service.fedora_settings')
app.config.from_envvar('FEDORA_SETTINGS', silent=True)
 
import oac_web_service.views