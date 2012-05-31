from oac_web_service import app
if app.config.get("SERVLET") is False:
    app.run(host='0.0.0.0', debug=True)