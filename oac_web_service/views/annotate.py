from flask import render_template
from oac_web_service import app

@app.route('/annotate', methods=['POST'])
def annotate():
    return True
