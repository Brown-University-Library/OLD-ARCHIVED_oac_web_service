from flask import render_template
from oac_web_service import app

@app.route('/')
def index():
    return render_template('show_index.html')
